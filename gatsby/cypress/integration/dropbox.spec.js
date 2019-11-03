import { stubOpenAuthWindow } from "./dropbox.scripts";
import tests from "./dropbox.scripts";

Cypress.on("window:before:load", win => stubOpenAuthWindow(win));

describe("The 'Dropbox' step", () => {
   it(
      "links to the dropbox/start API endpoint",
      tests.linkShouldBeDropboxStart
   );
   it("opens a new window when clicked", tests.clickingLinkShouldOpenNewWindow);
});

describe("When visiting the oAuth redirect link directly", () => {
   it("will cause an error message to print", tests.appShouldPrintErrorMessage);
});

context("When Dropbox redirects back to our app", () => {
   specify(
      "the app calls the api to finish the oAuth process",
      tests.appShouldCallTheAPI
   );
});

context("When the API finishes the oAuth process", () => {
   specify(
      "popup should notify main window of the successful response",
      tests.popupShouldNotifyMainWindowOfSuccess
   );
   specify(
      "the popup should notify main window the failed response",
      tests.popupShouldNotifyMainWindowOfFailure
   );
   specify(
      "the main window should close the popup",
      tests.mainWindowShouldClosePopup
   );
   specify(
      "the Dropbox step should print message saying authentication is successful",
      tests.boxShouldPrintSuccessMessage
   );
   specify(
      "the Dropbox step should be updated (oauth fail)",
      tests.boxShouldPrintErrorMessage
   );
});
