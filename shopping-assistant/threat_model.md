# Threat Model: Shopping Assistant Agent

## 1. System Boundaries
The Shopping Assistant is a retail-focused AI agent built with the Google ADK.

- **Entry Points**:
  - User prompts via the `App` wrapper.
  - Tool executions: `redeem_discount_code`, `get_weather`, `get_current_time`.
- **Data Layers**:
  - In-memory Python dictionaries (`DISCOUNT_CODES`, `REDEEMED_BY`).
- **External Integrations**: Google Gemini LLM via Vertex AI.

## 2. STRIDE Assessment

### Spoofing
- **Threat**: A user can provide a fake `user_id` to the `redeem_discount_code` tool.
- **Impact**: Fraudulent redemption of discounts on behalf of other users.
- **Risk**: High

### Tampering
- **Threat**: Manipulation of in-memory state.
- **Impact**: Potential to reset "redeemed" flags if a tool with write access is introduced.
- **Risk**: Low

### Repudiation
- **Threat**: Lack of persistent logging for sensitive transactions.
- **Impact**: Inability to audit who redeemed which code after a service restart.
- **Risk**: Medium

### Information Disclosure
- **Threat**: Hardcoded API Key in `app/agent.py`.
- **Impact**: Unauthorized access to the Gemini API and potential billing/quota exhaustion.
- **Risk**: Critical

### Denial of Service
- **Threat**: No rate limiting on tool calls.
- **Impact**: Exhaustion of discount codes or API quotas via automated spamming.
- **Risk**: Low

### Elevation of Privilege
- **Threat**: Lack of tool-level authorization.
- **Impact**: Any user can trigger administrative-like functions (e.g., redeeming codes) without verified privileges.
- **Risk**: Medium

## 3. Remediation Plan
1. **Immediate**: Move `api_key` to an environment variable or Secret Manager.
2. **Short-term**: Implement a persistent database (e.g., Firestore) for discount tracking and audit logs.
3. **Medium-term**: Introduce an identity verification layer (OAuth2/JWT) to validate `user_id` before calling the redemption tool.
