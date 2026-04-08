# SRS: Auth Service

## Overview

### Purpose

Provide a reusable authentication and authorization system for all future services.

### Scope

- User authentication (login/signup/logout)
- Token-based auth (JWT + refresh)
- Role-based access control (RBAC)
- Account lifecycle management

### Out of Scope (for sanity)

- OAuth (Google, GitHub) → later
- SSO → later
- MFA → optional extension

## System Goals

- Stateless authentication (JWT-based)
- Secure by default (no "we'll fix later" nonsense)
- Easily pluggable into other services
- Framework-agnostic design (same logic in Go + Django)

## Functional Requirements

### User Registration

User can register with:

- Email
- Password

Requirements:

- Email must be unique
- Password must be hashed

### User Login

- Accept email + password
- Validate credentials
- Return:
  - Access token (short-lived)
  - Refresh token (long-lived)

### Token System

#### Access Token

- JWT
- Contains:
  - user_id
  - roles
  - expiry

#### Refresh Token

- Stored in DB
- Used to issue new access tokens
- Can be revoked

### Logout

- Invalidate refresh token
- (Optional) blacklist access token

### Password Management

- Forgot password (email-based reset)
- Reset token with expiry
- Password update

### Email Verification

- Send verification email
- Activate account on confirmation

### Authorization (RBAC)

- Roles:
  - admin
  - user (default)
- Permissions mapped to roles

### Middleware / Guards

- Validate JWT
- Attach user context to request
- Reject unauthorized access

## Non-Functional Requirements

### Security

- Password hashing: bcrypt / argon2
- HTTPS assumed
- Token expiry enforced
- No sensitive data in JWT

### Performance

- Login < 200ms
- Token validation lightweight

### Scalability

- Stateless access tokens
- Refresh tokens DB-backed

### Reliability

- Token revocation support
- Retry-safe operations

## System Architecture

```
Client
  ↓
API Layer (Go/Django)
  ↓
Auth Service
  ├── Token Manager
  ├── User Manager
  ├── RBAC Engine
  ↓
Database (Postgres)
  ↓
Redis (optional: token blacklist / caching)
```

## Data Models

### User

- id (UUID)
- email
- password_hash
- is_active
- is_verified
- created_at

### RefreshToken

- id
- user_id
- token
- expires_at
- revoked (bool)

### Role

- id
- name (admin/user)

### UserRole

- user_id
- role_id

## API Design

### Auth APIs

#### Register

- **Method:** POST
- **Endpoint:** /auth/register

#### Login

- **Method:** POST
- **Endpoint:** /auth/login

#### Refresh Token

- **Method:** POST
- **Endpoint:** /auth/refresh

#### Logout

- **Method:** POST
- **Endpoint:** /auth/logout

### Password APIs

#### Forgot Password

- **Method:** POST
- **Endpoint:** /auth/forgot-password

#### Reset Password

- **Method:** POST
- **Endpoint:** /auth/reset-password

### User APIs

#### Get Current User

- **Method:** GET
- **Endpoint:** /auth/me

## Token Flow

### Login Flow

1. User logs in
2. Server validates credentials
3. Issues:
   - Access token (15 min)
   - Refresh token (7–30 days)

### Refresh Flow

1. Client sends refresh token
2. Server validates
3. Issues new access token

### Logout Flow

1. Client sends refresh token
2. Server marks it revoked

## Edge Cases

- Duplicate email registration
- Expired tokens
- Revoked refresh token reuse
- Password reset token reuse
- User deleted but token still valid
- Concurrent logins

## Failure Handling

- Invalid credentials → 401
- Expired token → 401 with message
- Revoked token → force re-login
- DB failure → safe error (no leaks)

## Security Considerations (read twice, seriously)

- Never store plain passwords
- Never trust client-side role data
- Always validate tokens server-side
- Use HTTP-only cookies if needed
- Protect against:
  - Brute force (rate limit)
  - Token theft
  - Replay attacks

## Extensions (Future Upgrades)

- OAuth login (Google, GitHub)
- Multi-factor authentication (MFA)
- Device/session tracking
- Fine-grained permissions (beyond RBAC)
