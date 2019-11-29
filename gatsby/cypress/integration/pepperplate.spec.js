import tests from "./pepperplate.scripts.js";

describe("The Pepperplate Step", () => {
   before(() => cy.visit("/"));

   it(
      "asks for Pepperplate's login credentials",
      tests.shouldAskForLoginCredentials
   );

   context("when submitting the form", () => {
      it(
         "displays a progress bar with initial status",
         tests.shouldDisplayProgressBarWithInitialStatus
      );
      // Submit button is not visible
      // Progress bar is visible
      // Progress bar value is 0
      // Label says "Initiating login process.."

      it("updates the progress bar when the browser starts");
      // Value is updated to "1"
      // Label is updated to "Login Progress Initiated..."

      it("updates the progress bar when login page is loaded");
      // Value is updates to "2"
      // Label is updated...
      // ? Assert whether the label has changed
   });

   context("When api request to login to Pepperplate has completed", () => {
      it(
         "displays an error message when one of the fields are missing",
         tests.missingFieldShouldDisplayErrorMessage
      );

      it(
         "removes spinner and enables the submit button",
         tests.formShouldReset
      );
   });

   it(
      "displays an error message when credentials are incorrect",
      tests.incorrectCredentialsShouldDisplayAnErrorMessage
   );
});

context("When login is successful", () => {
   specify("the progress bar should be updated");
   // Value is updated to "3"
   // Label is updated to "Logged In!"

   specify("the progress bar should be removed after a delay");

   specify("the recipe count should be displayed");

   specify("the next step should be focused");
});
