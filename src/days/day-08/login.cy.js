// Day 8 (QA) - Login page automation in Cypress
// Scenario: Test login page with happy path and negative cases

describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  describe('Happy Path', () => {
    it('should login with valid email and password, then show dashboard with user name', () => {
      const validEmail = 'user@example.com';
      const validPassword = 'password123';
      const userName = 'John Doe';

      // Arrange: Wait a bit for page to fully load
      cy.wait(500);

      // Act: Enter credentials
      cy.get('input[name="email"]')
        .type(validEmail);
      
      cy.get('input[name="password"]')
        .type(validPassword);
      
      cy.get('button[type="submit"]')
        .click();

      // Assert: Should navigate to dashboard
      cy.url().should('include', '/dashboard');
      
      // Assert: Should see user name on dashboard
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

      // Assert: Should show error message
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

      // Assert: Should show required field error
      cy.get('.field-error[data-field="email"]')
        .should('be.visible')
        .and('contain', 'Email is required');

      // Assert: Should stay on login page (form not submitted)
      cy.url().should('include', '/login');
    });
  });
});
