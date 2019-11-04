const expectedApiDropboxFinishParams = new URLSearchParams({
   state: "sojhqf2nGunEIxI-MdePeg==",
   code: "pQbO_7SMV2AAAAAAAAAAL_Tpd0uws8RpRTO2OBQAXwI"
});

const stubOauthFinishApiEndpoint = (
   stubbedResponse = { success: true },
   statusCode = 200
) => {
   cy.server();
   cy.route({
      url: `https://localhost:5000/dropbox/finish?state=*&code=*`,
      response: stubbedResponse,
      status: statusCode
   }).as("finishOAuthFlow");
};

const visitOauthRedirectUrl = () => {
   cy.visit("/dropbox-finish?" + expectedApiDropboxFinishParams.toString(), {
      onBeforeLoad(win) {
         // todo is this necessary?
         win.opener = win;
         cy.stub(win.opener, "postMessage");
      }
   });
};

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
      cy.getTestElement("dropbox-oauth")
         .invoke("attr", "href")
         .then(href => {
            expect(href).to.match(/https\:\/\/.+\/dropbox\/start$/);
         });
   },
   clickingLinkShouldOpenNewWindow: () => {
      cy.getTestElement("dropbox-oauth").click();
      cy.window()
         .its("top.open")
         .should("be.called");
   },
   appShouldPrintErrorMessage: () => {
      cy.visit("/dropbox-finish");
      cy.getTestElement("errorText").should("be.visible");
   },
   appShouldCallTheAPI: () => {
      stubOauthFinishApiEndpoint();
      visitOauthRedirectUrl();

      cy.wait("@finishOAuthFlow").then(xhr => {
         const actualURL = new URL(xhr.url);
         const actualParams = new URLSearchParams(actualURL.search);
         expect(actualParams.get("state")).to.equal(
            expectedApiDropboxFinishParams.get("state")
         );
         expect(actualParams.get("code")).to.equal(
            expectedApiDropboxFinishParams.get("code")
         );
      });
   },
   popupShouldNotifyMainWindowOfSuccess: () => {
      stubOauthFinishApiEndpoint({ success: true });
      visitOauthRedirectUrl();
      cy.window()
         .its("opener.postMessage")
         .should("be.calledWith", { success: true });
   },
   popupShouldNotifyMainWindowOfFailure: () => {
      stubOauthFinishApiEndpoint({ success: false }, 400);
      visitOauthRedirectUrl();
      cy.window()
         .its("opener.postMessage")
         .should("be.calledWith", { success: false });
   },
   mainWindowShouldClosePopup: () => {
      cy.visit("/");

      cy.getTestElement("dropbox-oauth").click();
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
      cy.getTestElement("dropbox-oauth").click();
      cy.window().trigger("message", { data: { success: true } });

      cy.getTestElement("dropbox-oauth").should("not.be.visible");
      cy.getTestElement("dropbox-oauth-success").should("be.visible");
   },
   boxShouldPrintErrorMessage: () => {
      cy.fixture("oauth400").then(oauth400Data => {
         cy.visit("/");
         cy.getTestElement("dropbox-oauth").click();
         cy.get("@openAuthWindow")
            .should("be.called")
            .then(function(mock) {
               const popup = mock.returnValues[0];
               cy.stub(popup, "close").as("closePopup");
            });
         cy.window().trigger("message", oauth400Data);
      });

      cy.getTestElement("dropbox-oauth").should("be.visible");
      cy.getTestElement("dropbox-oauth-success").should("not.be.visible");
      cy.getTestElement("dropbox-oauth-fail").should("be.visible");
   }
};
