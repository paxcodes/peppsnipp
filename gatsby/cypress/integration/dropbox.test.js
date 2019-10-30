Cypress.on("window:before:load", win => {
   win.top.open = cy
      .stub()
      .as("openAuthWindow")
      .callsFake(function(url, target, features, replace) {
         return {
            close: function() {}
         };
      });
});

describe("The 'Dropbox' step", () => {
   it("links to the dropbox/start API endpoint", () => {
      cy.visit("/");
      cy.get("[data-cy=dropbox-oauth]")
         .invoke("attr", "href")
         .then(href => {
            expect(href).to.match(/https\:\/\/.+\/dropbox\/start$/);
         });
   });

   it("opens a new window when clicked", () => {
      cy.visit("/");
      cy.get("[data-cy=dropbox-oauth]").click();

      cy.window()
         .its("top.open")
         .should("be.called");
   });

   context("When visiting the oAuth redirect link directly", () => {
      specify("it will cause an error message to print", () => {
         cy.visit("/dropbox-finish");
         cy.getTestElement("errorText").should("be.visible");
      });
   });
});

context("When Dropbox redirects back to our app", () => {
   specify("the app calls the api to finish the oAuth process", () => {
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
   });
});

context("When the API finishes the oAuth process", () => {
   specify(
      "the popup should notify parent window the successful response",
      () => {
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
      }
   );

   specify("the popup should notify parent window the failed response", () => {
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
   });

   specify("the parent window should close the popup", () => {
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
   });

   specify(
      "the Dropbox step should be updated (authentication successful)",
      () => {
         cy.visit("/");
         cy.get("[data-cy=dropbox-oauth]").click();
         cy.window().trigger("message", { data: { success: true } });

         cy.get("[data-cy=dropbox-oauth]").should("not.be.visible");
         cy.get("[data-cy=dropbox-oauth-success]").should("be.visible");
      }
   );

   specify("the Dropbox step should be updated (oauth fail)", () => {
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
   });
});
