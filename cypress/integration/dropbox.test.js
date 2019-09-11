describe("When I click on Dropbox", () => {
  it('it links to the dropbox/start API endpoint', () => {
    cy.visit("/");
    cy.get('[data-cy=dropbox-oauth]')
      .invoke('attr', 'href')
      .then(href => {
        expect(href).to.match(/https\:\/\/.+\/dropbox\/start$/);
      });
  })
})