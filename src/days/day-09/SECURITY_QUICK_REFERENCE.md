# Day 9 Security Review - Quick Reference

## Findings at a Glance

| # | Severity | File | Lines | Issue | Fix |
|---|----------|------|-------|-------|-----|
| 1 | 🔴 CRITICAL | output-2.js | 8 | Plaintext password comparison | Use `bcrypt.compare()` |
| 2 | 🟠 HIGH | output-2.js | 2 | Hardcoded JWT secret | Use environment variable |
| 3 | 🟠 HIGH | output-3.js | 3-5 | MD5 password hashing (broken) | Use bcrypt |
| 4 | 🟠 HIGH | output-4.js | 11-12 | PII logged to console | Redact sensitive fields |

## Checklist Results

✅ **CLEAN:**
- output-1.js (pagination)
- output-5.js (template renderer)

⚠️ **VULNERABLE:**
- output-2.js (auth) — 2 issues
- output-3.js (password hashing) — 1 issue  
- output-4.js (test with PII) — 1 issue

---

## One-Minute Summary

### Finding #1: Plaintext Passwords (CRITICAL)
```javascript
// ❌ BAD: Plaintext comparison
if (user && user.password === password)

// ✅ GOOD: Use bcrypt
if (user && await bcrypt.compare(password, user.passwordHash))
```

### Finding #2: Hardcoded JWT Secret (HIGH)
```javascript
// ❌ BAD: In source code
const JWT_SECRET = "FAKE-jwt-signing-key-...";

// ✅ GOOD: Environment variable
const JWT_SECRET = process.env.JWT_SECRET;
```

### Finding #3: MD5 Password Hashing (HIGH)
```javascript
// ❌ BAD: Cryptographically broken
crypto.createHash("md5")

// ✅ GOOD: Use bcrypt
bcrypt.hashSync(password, 10)
```

### Finding #4: PII in Logs (HIGH)
```javascript
// ❌ BAD: Logs full object with card, email, phone
console.log("Customer:", JSON.stringify(customer));

// ✅ GOOD: Log only safe fields
console.log("Customer:", customer.name);
```

---

## Risk Assessment

| Issue | Risk | Impact | Fix Time |
|-------|------|--------|----------|
| Plaintext passwords | Account compromise | User data breach | 15 min |
| Hardcoded secrets | Token forgery | Session hijacking | 5 min |
| MD5 hashing | Rapid cracking | Credential theft | 20 min |
| PII in logs | Data exposure | GDPR violation | 10 min |

**Total Fix Time: ~50 minutes**

---

## Implementation Checklist

- [ ] Install bcrypt: `npm install bcrypt`
- [ ] Fix output-2.js: Replace plaintext comparison
- [ ] Fix output-2.js: Move JWT_SECRET to env var
- [ ] Fix output-3.js: Replace MD5 with bcrypt
- [ ] Fix output-4.js: Redact PII from logs
- [ ] Test all authentication flows
- [ ] Verify no credentials in code
- [ ] Code review security changes
- [ ] Deploy fixes

---

## Key Takeaways

1. **Never hardcode secrets** — Always use environment variables
2. **Never hash passwords with MD5** — Use bcrypt/scrypt/Argon2
3. **Never compare passwords in plaintext** — Always use verified hashing libraries
4. **Never log PII** — Redact or omit sensitive data

---

## Resources

- Bcrypt: https://www.npmjs.com/package/bcrypt
- OWASP Password Storage: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- NIST Cryptographic Standards: https://csrc.nist.gov/publications/detail/sp/800-132/final
- PCI DSS Compliance: https://www.pcisecuritystandards.org/
