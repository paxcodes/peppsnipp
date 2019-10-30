import React from "react";
import dropbox from "../images/dropbox.svg";

class DropboxStep extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         dropboxConnected: false,
         dropboxFail: false
      };
   }

   updateDropboxStep = e => {
      this.setState({
         dropboxConnected: e.data.success
      });
      this.popup.close();
   };

   openNewWindow = e => {
      e.preventDefault();
      this.popup = window.top.open(
         e.currentTarget.attributes.href.value,
         "DropboxOAuth",
         "width=670, height=825, location=0"
      );
      window.addEventListener("message", this.updateDropboxStep);
   };

   render() {
      return (
         <>
            {this.state.dropboxConnected ? (
               <h2
                  data-cy="dropbox-oauth-success"
                  className="uppercase font-bold mb-4"
               >
                  Connected to
                  <img
                     alt="Dropbox"
                     src={dropbox}
                     className="block mt-2 h-8 mx-auto"
                  />
               </h2>
            ) : (
               <a
                  href={`${process.env.API_URL}/dropbox/start`}
                  data-cy="dropbox-oauth"
                  className="block"
                  onClick={this.openNewWindow}
               >
                  <h2 className="uppercase font-bold mb-4">
                     Connect to{" "}
                     <img alt="Dropbox" src={dropbox} className="h-8 mx-auto" />
                  </h2>
               </a>
            )}
            <p>
               We will save screenshots of your recipes in your Dropbox account.
            </p>
         </>
      );
   }
}

export default DropboxStep;
