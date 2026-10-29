# Cypress Test: Common Anti-Pattern Highlighted

## The Issue: Hardcoded Wait

### ❌ WRONG (Non-Idiomatic)
```javascript
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  it('should login with valid credentials', () => {
    const validEmail = 'user@example.com';
    const validPassword = 'password123';
    const userName = 'John Doe';

    // ❌ ANTI-PATTERN: Hardcoded wait
    cy.wait(500);

    // Now type credentials
    cy.get('input[name="email"]').type(validEmail);
    cy.get('input[name="password"]').type(validPassword);
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('.user-greeting').should('contain', userName);
  });
});
```

**Problems:**
- 500ms might not be enough if app is slow
- 500ms is wasted time if app is fast
- No guarantee page is actually ready
- Anti-pattern that Cypress was designed to eliminate
- Makes tests slower and more flaky

---

### ✅ CORRECT (Idiomatic Cypress)
```javascript
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  it('should login with valid credentials', () => {
    const validEmail = 'user@example.com';
    const validPassword = 'password123';
    const userName = 'John Doe';

    // ✅ NO EXPLICIT WAIT - Cypress handles it automatically
    cy.get('input[name="email"]')      // Waits for email input to be ready
      .type(validEmail);

    cy.get('input[name="password"]')   // Waits for password input to be ready
      .type(validPassword);

    cy.get('button[type="submit"]')    // Waits for button to be clickable
      .click();

    // Waits for URL to change with automatic retries
    cy.url().should('include', '/dashboard');

    // Waits for element and checks content
    cy.get('.user-greeting').should('contain', userName);
  });
});
```

**Advantages:**
- ✅ Automatic waiting on every command
- ✅ Automatic retries on assertions
- ✅ No artificial delays
- ✅ Works on fast and slow systems
- ✅ Truly deterministic
- ✅ Follows Cypress idioms

---

## Understanding Cypress's Automatic Waiting

### When Cypress Commands Wait

| Command | Waits For | Default Timeout |
|---------|-----------|-----------------|
| `cy.get()` | Element to exist in DOM | 4s |
| `.type()` | Element to be interactive | 4s |
| `.click()` | Element to be clickable | 4s |
| `.should()` | Assertion to pass (with retries) | 4s |
| `cy.url()` | Waits for navigation | 4s |
| `cy.visit()` | Page to load | 60s |

### Example: Waiting Chain
```javascript
cy.visit('http://localhost:3000/login');  // Waits for page load
  // ↓ Page loads

cy.get('input[name="email"]');            // Waits for input to exist
  // ↓ Input found

.type('user@example.com');                // Waits for input to be interactive
  // ↓ Input ready

cy.get('button[type="submit"]').click();  // Waits for button to be clickable
  // ↓ Button clicked, form submitted

cy.url().should('include', '/dashboard'); // Waits and retries until URL matches
  // ↓ Navigation complete, assertion passes
```

**Bottom line:** Every Cypress command and assertion is built for waiting. Explicit `cy.wait()` should almost never be used for page loads—only for waiting on API responses with `cy.intercept()`.

---

## Correct Use of `cy.wait()`

The only legitimate use case for `cy.wait()` in Cypress is for API responses:

```javascript
// ✅ CORRECT: Wait for API response
cy.intercept('POST', '/api/login').as('loginRequest');

cy.get('input[name="email"]').type(validEmail);
cy.get('input[name="password"]').type(validPassword);
cy.get('button[type="submit"]').click();

// Wait for the API call to complete
cy.wait('@loginRequest').then((interception) => {
  expect(interception.response.statusCode).to.equal(200);
});

// Now wait for navigation
cy.url().should('include', '/dashboard');
```

**Not like this:**
```javascript
// ❌ WRONG: Using cy.wait() for timing
cy.wait(2000);  // Don't do this!
cy.get('.user-greeting').should('contain', 'John');
```

---

## Summary

| Aspect | Anti-Pattern | Idiomatic |
|--------|--------------|-----------|
| **Waiting** | `cy.wait(500)` | Built-in via `cy.get()`, `.should()` |
| **Reliability** | Flaky, timing-dependent | Deterministic, retries |
| **Performance** | Slow (adds latency) | Fast (exact wait needed) |
| **Maintainability** | Breaks in CI/CD | Works everywhere |
| **Intent** | Unclear why waiting | Clear what we're waiting for |

The key insight: **Cypress is built specifically to eliminate arbitrary waits.** Use it correctly! 🎯
