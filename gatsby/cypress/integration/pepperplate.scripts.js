export default {
   shouldAskForLoginCredentials: () => {
      cy.getTestElement("usernameField").should("be.visible");
      cy.getTestElement("passwordField").should("be.visible");
   },
   shouldDisplayLoadingGif: () => {
      cy.getTestElement("submitBtn").click();
      cy.getTestElement("loadingAnimation").should("be.visible");
      cy.getTestElement("submitBtn").should("be.disabled");
   }
};
