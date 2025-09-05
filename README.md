<p align="left">
  <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <img src="https://cdn.scalekit.cloud/v1/scalekit-logo-dark.svg" height="64">
    </picture>
  </a>
  <br/>
</p>

# OIDC, SAML & SCIM Examples

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SAML](https://img.shields.io/badge/SAML-2.0-green?style=flat-square)](https://saml.xml.org/)
[![OIDC](https://img.shields.io/badge/OIDC-1.0-blue?style=flat-square)](https://openid.net/connect/)

Comprehensive examples demonstrating <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">Scalekit</a>'s **auth stack for AI apps** with various identity providers and protocols. Learn how to implement enterprise authentication flows including OIDC, SAML, and SCIM provisioning.

## 🔐 Authentication Examples

This repository contains practical implementations for:

### **OIDC (OpenID Connect)**
- **Google OIDC**: Complete Python implementation for Google Workspace SSO
- **Microsoft Entra ID**: Azure AD authentication flows
- **Generic OIDC**: Configurable OIDC provider integration

### **SAML (Security Assertion Markup Language)**  
- **Okta SAML**: Enterprise Okta SAML integration
- **PingIdentity SAML**: PingFederate/PingOne authentication
- **Azure AD SAML**: Microsoft Azure SAML flows

### **SCIM (System for Cross-domain Identity Management)**
- **User Provisioning**: Automated user creation and management
- **Group Sync**: Organization and role synchronization
- **Deprovisioning**: Secure user lifecycle management

## 🤖 What You'll Learn

- **Agent-First Architecture**: How MCP integrates with enterprise identity
- **Human Authentication**: Traditional SSO flows for web applications
- **Token Management**: Secure token storage and rotation with Scalekit's Token Vault
- **Audit & Compliance**: Immutable audit trails for enterprise requirements
- **Multi-tenant Setup**: Organization-level authentication policies

## 🚀 Quick Start

### Prerequisites

1. [Sign up](https://scalekit.com) for a Scalekit account
2. Configure your identity provider (Google, Okta, Azure AD, etc.)
3. Python 3.8+ installed on your system

### Setup

```bash
# Clone the repository
git clone https://github.com/scalekit-developers/oidc-saml-scim-examples.git
cd oidc-saml-scim-examples

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
```

### Configuration

Update `.env` with your Scalekit and identity provider credentials:

```bash
# Scalekit Configuration
SCALEKIT_ENV_URL=your_env_url
SCALEKIT_CLIENT_ID=your_client_id
SCALEKIT_CLIENT_SECRET=your_client_secret

# Identity Provider Specific
GOOGLE_CLIENT_ID=your_google_client_id
OKTA_DOMAIN=your_okta_domain
AZURE_TENANT_ID=your_azure_tenant_id
```

## 📁 Example Structure

```
├── google-oidc/          # Google Workspace OIDC integration
├── okta-saml/           # Okta SAML authentication
├── azure-oidc/          # Microsoft Azure AD OIDC
├── azure-saml/          # Microsoft Azure AD SAML
├── scim-provisioning/   # User provisioning examples
├── shared/              # Common utilities and helpers
└── docs/               # Detailed implementation guides
```

## 🔧 Available Examples

| Example | Protocol | Description | Status |
|---------|----------|-------------|--------|
| **Google OIDC** | OIDC | Google Workspace SSO integration | ✅ Ready |
| **Okta SAML** | SAML | Okta enterprise authentication | ✅ Ready |
| **Azure OIDC** | OIDC | Microsoft Entra ID OIDC flows | 🚧 Coming Soon |
| **PingIdentity SAML** | SAML | PingFederate integration | 🚧 Coming Soon |
| **SCIM Provisioning** | SCIM | Automated user management | ✅ Ready |

## 🔗 Helpful Links

### 📖 Quickstart Guides
- [**SSO Integration**](https://docs.scalekit.com/sso/quickstart/) - Implement enterprise Single Sign-on
- [**Full Stack Auth**](https://docs.scalekit.com/fsa/quickstart/) - Complete authentication solution
- [**SCIM Provisioning**](https://docs.scalekit.com/directory/) - User lifecycle management
- [**Social Logins**](https://docs.scalekit.com/social-logins/quickstart/) - Popular social identity providers

### 📚 Documentation & Reference
- [**API Reference**](https://docs.scalekit.com/apis) - Complete API documentation
- [**Developer Kit**](https://docs.scalekit.com/dev-kit/) - Tools and utilities
- [**API Authentication Guide**](https://docs.scalekit.com/guides/authenticate-scalekit-api/) - Secure API access

### 🛠️ Additional Resources
- [**Setup Guide**](https://docs.scalekit.com/guides/setup-scalekit/) - Initial platform configuration
- [**Code Examples**](https://docs.scalekit.com/directory/code-examples/) - Ready-to-use code snippets
- [**Admin Portal Guide**](https://docs.scalekit.com/directory/guides/admin-portal/) - Administrative interface

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.