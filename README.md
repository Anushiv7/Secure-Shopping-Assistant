# Secure Shopping Assistant 🛍️🛡️

An AI-powered shopping assistant built using the Google Agent Development Kit (ADK), designed with a focus on security and reliability.

## 🌟 Overview

The **Secure Shopping Assistant** is a ReAct-based agent that helps users navigate shopping tasks while maintaining a strong security posture. Unlike generic assistants, this project includes a comprehensive threat model to identify and mitigate potential vulnerabilities in agent-tool interactions.

## 📂 Project Structure

```
.
├── LICENSE                 # MIT License
├── README.md               # Project overview
└── shopping-assistant/     # Core project implementation
    ├── app/                # Agent logic and tools
    ├── tests/              # Unit and integration tests
    ├── threat_model.md     # Security analysis and risk assessment
    ├── GEMINI.md           # AI-assisted development guide
    └── pyproject.toml      # Dependencies and project config
```

## 🛡️ Security First

Security is a core pillar of this project. We have documented a detailed **Threat Model** which analyzes the system using the STRIDE framework:
- **Spoofing**: Validation of user identities.
- **Tampering**: Integrity of in-memory state.
- **Repudiation**: Audit logging for sensitive transactions.
- **Information Disclosure**: Secure management of API keys.
- **Denial of Service**: Rate limiting and quota management.
- **Elevation of Privilege**: Tool-level authorization.

Detailed analysis can be found in [`shopping-assistant/threat_model.md`](shopping-assistant/threat_model.md).

## 🚀 Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- `google-agents-cli` (`uv tool install google-agents-cli`)

### Installation & Setup
1. Navigate to the project directory:
   ```bash
   cd shopping-assistant
   ```
2. Install dependencies:
   ```bash
   agents-cli install
   ```
3. Launch the local playground:
   ```bash
   agents-cli playground
   ```

## 🛠️ Development

For detailed development instructions, including the evaluation loop and deployment guides, please refer to the [`shopping-assistant/GEMINI.md`](shopping-assistant/GEMINI.md) file.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
