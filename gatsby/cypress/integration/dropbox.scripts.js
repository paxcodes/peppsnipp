export const stubOpenAuthWindow = win => {
   win.top.open = cy
      .stub()
      .as("openAuthWindow")
      .callsFake(function(url, target, features, replace) {
         return {
            close: function() {}
         };
      });
};

export default {
   linkShouldBeDropboxStart: () => {
      cy.get("[data-cy=dropbox-oauth]")
         .invoke("attr", "href")
         .then(href => {
            expect(href).to.match(/https\:\/\/.+\/dropbox\/start$/);
         });
   },
   clickingLinkShouldOpenNewWindow: () => {
      cy.get("[data-cy=dropbox-oauth]").click();
      cy.get("@openAuthWindow").should("be.called");
   },
   appShouldPrintErrorMessage: () => {
      cy.visit("/dropbox-finish");
      cy.getTestElement("errorText").should("be.visible");
   },
   appShouldCallTheAPI: () => {
      const expectedParams = new URLSearchParams({
         state: "sojhqf2nGunEIxI-MdePeg==",
         code: "pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI"
      });

      cy.server();
      cy.route(`https://localhost:5000/dropbox/finish?state=*&code=*`).as(
         "finishOAuthFlow"
      );

      cy.visit("/dropbox-finish?" + expectedParams.toString(), {
         onBeforeLoad(win) {
            win.opener = win;
         }
      });

      cy.wait("@finishOAuthFlow").then(xhr => {
         const actualURL = new URL(xhr.url);
         const actualParams = new URLSearchParams(actualURL.search);
         expect(actualParams.get("state")).to.equal(
            expectedParams.get("state")
         );
         expect(actualParams.get("code")).to.equal(expectedParams.get("code"));
      });
   },
   popupShouldNotifyMainWindowOfSuccess: () => {
      const expectedParams = new URLSearchParams({
         state: "sojhqf2nGunEIxI-MdePeg==",
         code: "pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI"
      });

      const stubbedResponse = { success: true };

      cy.server();
      cy.route(
         `https://localhost:5000/dropbox/finish?state=*&code=*`,
         stubbedResponse
      ).as("finishOAuthFlow");

      cy.visit("/dropbox-finish?" + expectedParams.toString(), {
         onBeforeLoad(win) {
            win.opener = win;
            cy.stub(win.opener, "postMessage");
         }
      });

      cy.window()
         .its("opener.postMessage")
         .should("be.calledWith", stubbedResponse);
   },
   popupShouldNotifyMainWindowOfFailure: () => {
      const expectedParams = new URLSearchParams({
         state: "sojhqf2nGunEIxI-MdePeg==",
         code: "pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI"
      });

      const stubbedResponse = { success: false };

      cy.server();
      cy.route({
         url: `https://localhost:5000/dropbox/finish?state=*&code=*`,
         response: stubbedResponse,
         status: 400
      }).as("finishOAuthFlow");

      cy.visit("/dropbox-finish?" + expectedParams.toString(), {
         onBeforeLoad(win) {
            win.opener = win;
            cy.stub(win.opener, "postMessage");
         }
      });

      cy.window()
         .its("opener.postMessage")
         .should("be.calledWith", stubbedResponse);
   },
   mainWindowShouldClosePopup: () => {
      cy.visit("/");

      cy.get("[data-cy=dropbox-oauth]").click();
      cy.get("@openAuthWindow")
         .should("be.called")
         .then(function(spy) {
            const popup = spy.returnValues[0];
            cy.spy(popup, "close").as("closePopup");
         });

      cy.window().trigger("message", { data: { success: true } });
      cy.get("@closePopup").should("be.called");
   },
   boxShouldPrintSuccessMessage: () => {
      cy.visit("/");
      cy.get("[data-cy=dropbox-oauth]").click();
      cy.window().trigger("message", { data: { success: true } });

      cy.get("[data-cy=dropbox-oauth]").should("not.be.visible");
      cy.get("[data-cy=dropbox-oauth-success]").should("be.visible");
   },
   boxShouldPrintErrorMessage: () => {
      cy.fixture("oauth400").then(oauth400Data => {
         cy.visit("/");
         cy.get("[data-cy=dropbox-oauth]").click();
         cy.get("@openAuthWindow")
            .should("be.called")
            .then(function(mock) {
               const popup = mock.returnValues[0];
               cy.stub(popup, "close").as("closePopup");
            });
         cy.window().trigger("message", oauth400Data);
      });

      cy.get("[data-cy=dropbox-oauth]").should("be.visible");
      cy.get("[data-cy=dropbox-oauth-success]").should("not.be.visible");
      cy.get("[data-cy=dropbox-oauth-fail]").should("be.visible");
   }
};
