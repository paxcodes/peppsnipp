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
  
  context("When visiting the oAuth redirect link directly", () => {
    specify("it will cause an error message to print", () => {
      cy.visit("/dropbox-finish");
      cy.getTestElement("errorText").should('be.visible');
    });  
  });
  
  context("When Dropbox redirects back to our app", () => {
    specify("the app calls the api to finish the oAuth process", () => {
      const expectedParams = new URLSearchParams({
        'state': 'sojhqf2nGunEIxI-MdePeg==',
        'code': 'pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI'
      });
      
      cy.server();
      cy.route(`https://localhost:5000/dropbox/finish?state=*&code=*`).as('finishOAuthFlow');
      
      cy.visit("/dropbox-finish?" + expectedParams.toString(), {
        onBeforeLoad(win) {
          win.opener = win;
        }
      });
      
      cy.wait('@finishOAuthFlow').then((xhr) => {
        const actualURL = new URL(xhr.url);
        const actualParams = new URLSearchParams(actualURL.search);
        expect(actualParams.get("state")).to.equal(expectedParams.get("state"));
        expect(actualParams.get("code")).to.equal(expectedParams.get("code"));
      });
    });
  })
});