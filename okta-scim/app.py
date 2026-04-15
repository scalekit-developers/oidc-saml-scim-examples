from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
import uuid
import logging
import os
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

SCIM_BASE_PATH = '/scim/v2'

SCIM_TOKEN = os.environ.get('SCIM_TOKEN', 'your-secret-token-here')

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class User(db.Model, Serializer):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userName = db.Column(db.String, unique=True, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


    def serialize(self):
        d = Serializer.serialize(self)
        return d

def authenticate():
    return jsonify({"error": "Authentication required"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

def requires_token_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid or missing token"}), 401
        token = auth_header.split(' ')[1]
        if token != SCIM_TOKEN:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route(f'{SCIM_BASE_PATH}/Users', methods=['GET'])
@requires_token_auth
def list_users():
    # Get pagination parameters from the query string
    start_index = int(request.args.get('startIndex', 1))
    count = int(request.args.get('count', 100))  # Default to 100 users if not specified

    # Calculate the start and end indices for slicing the query results
    start = start_index - 1  # SCIM uses 1-based indexing
    end = start + count

    # Query the database and serialize the results
    users = User.query.slice(start, end).all()
    total_results = User.query.count()

    # Prepare the response following SCIM format
    response = {
        'schemas': ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        'totalResults': total_results,
        'startIndex': start_index,
        'itemsPerPage': len(users),
        'Resources': User.serialize_list(users)
    }
    
    return jsonify(response), 200


@app.route(f'{SCIM_BASE_PATH}/Users', methods=['POST'])
@requires_token_auth
def create_user():
    data = request.json
    new_user = User(
        userName=data['userName'],
        firstName=data['name']['givenName'],
        lastName=data['name']['familyName'],
        email=data['emails'][0]['value'],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route(f'{SCIM_BASE_PATH}/Users/<string:user_id>', methods=['GET'])
@requires_token_auth
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize()), 200

@app.route(f'{SCIM_BASE_PATH}/Users/<string:user_id>', methods=['PUT'])
@requires_token_auth
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.userName=data['userName'],
    user.firstName=data['name']['givenName'],
    user.lastName=data['name']['familyName'],
    user.email=data['emails'][0]['value'],
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route(f'{SCIM_BASE_PATH}/Users/<string:user_id>', methods=['DELETE'])
@requires_token_auth
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.before_request
def log_request_info():
    # Log request method and URL
    logging.info(f'Request URL: {request.url}')
    
    # Log headers
    logging.info(f'Headers: {request.headers}')
    
    # Log payload if it's a POST or PUT request
    if request.method in ['POST', 'PUT']:
        logging.info(f'Payload: {request.get_data(as_text=True)}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)