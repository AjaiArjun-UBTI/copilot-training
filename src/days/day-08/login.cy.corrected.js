// Day 8 (QA) - Login page automation in Cypress (CORRECTED VERSION)
// Scenario: Test login page with happy path and negative cases
// NOTE: Removed hardcoded cy.wait(500) - Cypress handles waiting automatically

describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  describe('Happy Path', () => {
    it('should login with valid email and password, then show dashboard with user name', () => {
      const validEmail = 'user@example.com';
      const validPassword = 'password123';
      const userName = 'John Doe';

      // Cypress automatically waits for elements to be ready via cy.get()
      // No need for explicit cy.wait(500)
      cy.get('input[name="email"]')
        .type(validEmail);
      
      cy.get('input[name="password"]')
        .type(validPassword);
      
      cy.get('button[type="submit"]')
        .click();

      // url().should() automatically retries until condition is met
      cy.url().should('include', '/dashboard');
      
      // get().should() waits for element and content
      cy.get('.user-greeting')
        .should('contain', userName);
    });
  });

  describe('Negative Cases', () => {
    it('should show error message with wrong password and stay on login page', () => {
      const validEmail = 'user@example.com';
      const wrongPassword = 'wrongpassword';

      cy.get('input[name="email"]')
        .type(validEmail);
      
      cy.get('input[name="password"]')
        .type(wrongPassword);
      
      cy.get('button[type="submit"]')
        .click();

      // Assert: Should stay on login page
      cy.url().should('include', '/login');

      // Assert: Should show error message (waits for visibility)
      cy.get('.error-message')
        .should('be.visible')
        .and('contain', 'Invalid email or password');
    });

    it('should show required field error when email is empty', () => {
      const validPassword = 'password123';

      // Leave email empty, only fill password
      cy.get('input[name="password"]')
        .type(validPassword);
      
      cy.get('button[type="submit"]')
        .click();

      // Assert: Should show required field error (waits for element)
      cy.get('.field-error[data-field="email"]')
        .should('be.visible')
        .and('contain', 'Email is required');

      // Assert: Should stay on login page (form not submitted)
      cy.url().should('include', '/login');
    });
  });
});
