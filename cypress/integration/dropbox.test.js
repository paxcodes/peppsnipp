describe("The 'Dropbox' step", () => {
  it('links to the dropbox/start API endpoint', () => {
    cy.visit("/");
    cy.get('[data-cy=dropbox-oauth]')
      .invoke('attr', 'href')
      .then(href => {
        expect(href).to.match(/https\:\/\/.+\/dropbox\/start$/);
      });
  });
  
  it('opens a new window when clicked', () => {
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win, 'open');
      }
    });
    
    cy.get('[data-cy=dropbox-oauth]').click();
    cy.window().its('open').should('be.called');
  });
});