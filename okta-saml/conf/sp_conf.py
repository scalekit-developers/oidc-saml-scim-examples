import os
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NAMEID_FORMAT_PERSISTENT


# Base URL for the SP (can be overridden via env for different deploys)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8433")

# Resolve default local metadata path (conf/idp-metadata.xml)
BASE_DIR = os.path.dirname(__file__)
DEFAULT_LOCAL_METADATA = os.path.normpath(os.path.join(BASE_DIR, 'idp-metadata.xml'))

# Metadata configuration - prefer remote URL if provided
# Default to env-provided metadata URL, or fall back to a known Okta metadata
# metadata fetch. Override by setting `IDP_METADATA_URL` or `METADATA_URL`.
METADATA_URL = (
    os.environ.get('IDP_METADATA_URL')
    or os.environ.get('METADATA_URL')
)
# Allow overriding local metadata path via env
METADATA_LOCAL = os.environ.get('IDP_METADATA_LOCAL', DEFAULT_LOCAL_METADATA)
# If the local file exists, prefer it. Set FORCE_REMOTE=1 to force using METADATA_URL.
# Decide whether to use remote metadata. If FORCE_REMOTE is explicitly set
# to a truthy value we obey it. Otherwise, prefer remote when a METADATA_URL
# is available and the local metadata file is missing.
FORCE_REMOTE = os.environ.get('FORCE_REMOTE', '') in ('1', 'true', 'True')

if (not FORCE_REMOTE) and os.path.exists(METADATA_LOCAL):
    metadata_cfg = {'local': [METADATA_LOCAL]}
elif METADATA_URL:
    metadata_cfg = {'remote': [{'url': METADATA_URL}]}
else:
    metadata_cfg = {'local': [METADATA_LOCAL]}


CONFIG = {
    'entityid': BASE_URL + '/saml/metadata/',
    'service': {
        'sp': {
            'name': 'SaaS Sample App',
            "name_id_policy_format": "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
            'endpoints': {
                'assertion_consumer_service': [
                    (BASE_URL + '/saml/acs/', BINDING_HTTP_POST),
                ],
            },
            'allow_unsolicited': True,
            'authn_requests_signed': False,
            'want_assertions_signed': True,
            'want_response_signed': True,
        },
    },
    # Metadata source - either remote URL(s) or local file(s)
    'metadata': metadata_cfg,
}

