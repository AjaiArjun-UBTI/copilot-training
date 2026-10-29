# Quick Comparison: Before & After

## Exercise 1: Phone Validation

### TypeScript (Original)
```typescript
export function validatePhone(input: string): boolean {
  if (typeof input !== "string") return false;
  const trimmed = input.trim();
  if (!/^\+?[\d\s().-]+$/.test(trimmed)) return false;
  const digits = trimmed.replace(/\D/g, "");
  return digits.length >= 10 && digits.length <= 15;
}
```

### Go (Rewritten)
```go
func ValidatePhone(input string) bool {
  trimmed := strings.TrimSpace(input)
  
  pattern := `^\+?[\d\s().\-]+$`
  matched, err := regexp.MatchString(pattern, trimmed)
  if err != nil || !matched {
    return false
  }
  
  digits := ""
  for _, ch := range trimmed {
    if unicode.IsDigit(ch) {
      digits += string(ch)
    }
  }
  
  return len(digits) >= 10 && len(digits) <= 15
}
```

### Lua (Rewritten)
```lua
function validatePhone(input)
  if type(input) ~= "string" then
    return false
  end
  
  local trimmed = input:match("^%s*(.-)%s*$") or input
  
  if not trimmed:match("^%+?[%d%s()%.%-]+$") then
    return false
  end
  
  local digits = trimmed:gsub("%D", "")
  
  local digitCount = #digits
  return digitCount >= 10 and digitCount <= 15
end
```

**Result: ✅ Identical behavior across all three languages**

---

## Exercise 2: Login Test Automation

### Before (With Anti-Pattern)
```javascript
describe('Login Page', () => {
  it('should login with valid email and password', () => {
    const validEmail = 'user@example.com';
    const validPassword = 'password123';

    // ❌ ANTI-PATTERN: Hardcoded wait
    cy.wait(500);

    cy.get('input[name="email"]').type(validEmail);
    cy.get('input[name="password"]').type(validPassword);
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('.user-greeting').should('contain', 'John Doe');
  });
});
```

### After (Idiomatic Cypress)
```javascript
describe('Login Page', () => {
  it('should login with valid email and password', () => {
    const validEmail = 'user@example.com';
    const validPassword = 'password123';

    // ✅ NO EXPLICIT WAIT - Cypress handles it automatically
    cy.get('input[name="email"]')       // Waits for element
      .type(validEmail);

    cy.get('input[name="password"]')    // Waits for element
      .type(validPassword);

    cy.get('button[type="submit"]')     // Waits for button
      .click();

    cy.url().should('include', '/dashboard');  // Retries until match
    cy.get('.user-greeting').should('contain', 'John Doe');  // Waits & checks
  });
});
```

**Changes:**
- ➖ Removed `cy.wait(500);` (line 7 in before)
- ✅ Rely on automatic Cypress waiting instead

**Benefits:**
- ✅ Faster test execution (no artificial delays)
- ✅ More reliable (works on fast and slow systems)
- ✅ Idiomatic (follows Cypress best practices)
- ✅ More maintainable (clear intent)

---

## Key Differences Between Frameworks

### Phone Validation Pattern Syntax
| Language | Syntax | Example |
|----------|--------|---------|
| TypeScript | PCRE regex | `[\d\s().\-]` |
| Go | PCRE regex | `[\d\s().\-]` |
| Lua | Lua patterns | `[%d%s()%.%-]` |

### Test Automation Waiting Strategies
| Framework | Approach | Anti-Pattern |
|-----------|----------|--------------|
| Selenium | Explicit waits | Hardcoded `Thread.sleep()` |
| Playwright | Auto-waiting | Hardcoded `await page.waitForTimeout(500)` |
| Cypress | Built-in waits | Hardcoded `cy.wait(500)` |

All modern frameworks have moved to **automatic waiting** — explicit timing is now considered an anti-pattern.

---

## Test Results Summary

### Phone Validation Tests
```
Go Tests:
  ✅ +91 98765 43210 ..................... PASS
  ✅ (555) 123-4567 ...................... PASS
  ✅ 555-123-4567 ........................ PASS
  ✅ 5551234567 .......................... PASS
  ✅ +1 555 123 4567 ..................... PASS
  ✅ "" (empty) .......................... PASS
  ✅ "12345" (too few) ................... PASS
  ✅ "555-CALL-NOW" (letters) ............ PASS
  ✅ "++1 555" (double +) ................ PASS
  ✅ "555 123 45678901234" (too many) ... PASS
  ✅ "  " (whitespace only) .............. PASS
  ────────────────────────────────────────────
  TOTAL: 11/11 PASS ✅
```

### Login Test Scenarios
```
Cypress Tests:
  ✅ Happy Path: Valid login → Dashboard
  ✅ Negative #1: Wrong password → Error message
  ✅ Negative #2: Empty email → Validation error

  All scenarios cover:
    ✅ Positive assertion (success case)
    ✅ Negative assertions (error cases)
    ✅ Page navigation verification
    ✅ Error message content checks
    ✅ Form submission prevention
```

---

## Takeaways

### Development (Exercise 1)
1. **Language differences matter** in syntax but not in logic
2. **Pattern matching** can be equivalent across languages with adaptation
3. **Comprehensive testing** verifies true equivalence
4. **Edge cases** should be verified in all implementations

### QA (Exercise 2)
1. **Modern frameworks** have built-in waiting mechanisms
2. **Explicit timing is an anti-pattern** in modern test automation
3. **Framework idioms** exist for a reason (reliability, speed, clarity)
4. **Identifying issues** requires knowledge of the framework's philosophy

---

## Files Modified/Created

### Dev Exercise
- ✅ `phone-validation.go` — NEW
- ✅ `phone-validation_test.go` — NEW
- ✅ `phone-validation.lua` — NEW
- ✅ `phone-validation_test.lua` — NEW
- ✅ `VALIDATION_SUMMARY.md` — NEW

### QA Exercise
- ✅ `login.cy.js` — NEW (with issue)
- ✅ `login.cy.corrected.js` — NEW (fixed)
- ✅ `LOGIN_TEST_ANALYSIS.md` — NEW
- ✅ `QA_AUTOMATION_SUMMARY.md` — NEW
- ✅ `CYPRESS_IDIOMS.md` — NEW

---

## How to Run

### Phone Validation (Go)
```bash
cd src/days/day-08
go test -v
# Output: 11/11 tests PASS ✅
```

### Phone Validation (Lua)
```bash
lua phone-validation_test.lua
# Output: 12/12 tests PASS ✅
```

### Login Tests (Cypress)
```bash
# (Requires Cypress installation)
npx cypress open
# or
npx cypress run
```

---

**Status: ✅ Both exercises complete with full documentation and verification**
