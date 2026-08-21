# Authentication & Authorization Architecture

## 1. Password Hashing
- Algorithm: **Bcrypt** with **cost factor 12** ($2^{12}$ internal key expansion rounds).
- Timing-safe hash comparison via `bcrypt.checkpw()`.
- Explicit rejection of malformed hashes and empty strings.

## 2. JWT Access Tokens (PyJWT)
- **Algorithm**: `HS256` explicitly enforced (blocks `none` algorithm confusion).
- **Mandatory Claims**:
  - `sub`: User UUID
  - `email`: User email
  - `role`: `student`, `medical_reviewer`, `admin`
  - `iss`: `neetpg-pro-auth`
  - `aud`: `neetpg-pro-app`
  - `exp`: Expiration timestamp
  - `iat`: Issued-at timestamp
  - `nbf`: Not-before timestamp

## 3. Server-Authoritative Role Gates (RBAC)
- `get_current_user`: Base dependency extracting authenticated `User`.
- `get_current_student`: Requires active student role.
- `get_current_reviewer_user`: Restricted to `medical_reviewer` and `admin`.
- `get_current_admin_user`: Strictly restricted to `admin`.

## 4. Rate Limiting
- Applied to `/auth/register` (max 10 req/min), `/auth/login` (max 15 req/min), `/tests/start` (max 20 req/min), `/questions/{id}/report` (max 10 req/min).
