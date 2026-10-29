# Bug Report: Password Reset Email Not Delivered for SSO Gmail Users

## Severity
🔴 **HIGH** — Users cannot recover their accounts; affects a specific user cohort (SSO-created Gmail accounts).

## Environment
- **Test Environment**: Staging
- **Test Run**: 2026-10-29T10:12:03Z
- **Affected User Type**: Gmail users created via SSO
- **Unaffected User Type**: Password-created users (email delivery works)

## Observed Behavior
Password reset email never arrives for users with Gmail addresses created through SSO. After requesting a reset and waiting 5 minutes, no email is received.

## Expected Behavior
Every valid password reset request should deliver a confirmation email within 2 minutes.

## Steps to Reproduce
1. Create or use an existing user account with a Gmail address via SSO
2. Request a password reset for that email address
3. Wait 5 minutes
4. **Result**: No reset email arrives in the Gmail inbox

## Test Evidence
From staging test run (password-reset suite):

| Test Case | Result | Notes |
|-----------|--------|-------|
| request reset for a registered email | ✅ PASS | Flow completes without error |
| reset link opens the reset form | ✅ PASS | Email link is valid when received |
| set a new password with a valid token | ✅ PASS | Token processing works |
| **reset email arrives within 2 minutes (SSO-created Gmail user)** | ❌ **FAIL** | **No email after 5 minutes** |
| reset email arrives within 2 minutes (password-created user) | ✅ PASS | Email delivery works for non-SSO users |
| unknown email returns a generic message | ✅ PASS | Error handling correct |
| reset link opens the reset form | ✅ PASS | — |

**Finding**: Email delivery succeeds for password-created users but fails **only** for SSO-created Gmail users.

## Suspected Root Cause
**Email delivery service / SSO user sync**
- SSO user records may not have correct email metadata
- Email service may be rejecting SSO-created Gmail addresses due to domain/verification mismatch
- Possible: SSO users are stored without email verification flag, blocking delivery

## Impact
- Users cannot self-serve password recovery
- Support escalations required for account recovery
- Affects unknown % of user base (SSO-created users specifically)

## Recommended Investigation
1. Check email service logs for delivery failures to SSO Gmail addresses
2. Compare email field values between SSO-created users vs. password-created users
3. Verify SSO user records include verified email flags
4. Check for domain whitelist/blacklist in email provider configuration
