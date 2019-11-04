import tests from "./pepperplate.scripts.js";

describe("The Pepperplate Step", () => {
   before(() => cy.visit("/"));

   it(
      "asks for Pepperplate's login credentials",
      tests.shouldAskForLoginCredentials
   );
   it(
      "displays a `loading gif` when submitting the form",
      tests.shouldDisplayLoadingGif
   );

   context("When api request to login to Pepperplate has completed", () => {
   it(
      "displays an error message when one of the fields are missing",
         "removes spinner and enables the submit button",
         tests.formShouldReset
      );
   });

      tests.missingFieldShouldDisplayErrorMessage
   );
   it(
      "displays an error message when credentials are incorrect",
      tests.incorrectCredentialsShouldDisplayAnErrorMessage
   );
});

context("When login is successful", () => {
   it("notifies user when login is successful");
   it("removes the login form and describes the next process");
});
