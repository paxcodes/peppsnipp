export default {
   shouldAskForLoginCredentials: () => {
      cy.getTestElement("usernameField").should("be.visible");
      cy.getTestElement("passwordField").should("be.visible");
   },
   shouldDisplayLoadingGif: () => {
      cy.getTestElement("submitBtn").click();
      cy.getTestElement("loadingAnimation").should("be.visible");
      cy.getTestElement("submitBtn").should("be.disabled");
   },
   formShouldReset: () => {
      cy.server();
      cy.route("POST", "https://localhost:5000/pepperplate/session", {
         success: true
      }).as("loginToPepperplate");

      cy.getTestElement("submitBtn").click();
      cy.wait("@loginToPepperplate");
      cy.getTestElement("loadingAnimation").should("not.be.visible");
      cy.getTestElement("submitBtn").should("be.enabled");
   },
};
