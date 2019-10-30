import React from "react";
import dropbox from "../images/dropbox.svg";

class DropboxStep extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         dropboxConnected: false,
         dropboxFail: false,
         errorMessage: ""
      };
   }

   updateDropboxStep = e => {
      this.setState({
         dropboxConnected: e.data.success,
         errorMessage: e.data.msg
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
                  <p className="px-2 py-4 bg-green-200 mb-8 text-green-900 font-bold text-sm">
                     Success!{" "}
                     <span role="img" aria-label="celebrate!">
                        🎉
                     </span>
                  </p>
                  Connected to
                  <img
                     alt="Dropbox"
                     src={dropbox}
                     className="block mt-2 h-8 mx-auto"
                  />
               </h2>
            ) : (
               <>
                  <ErrorMessage msg={this.state.errorMessage} />
                  <a
                     href={`${process.env.API_URL}/dropbox/start`}
                     data-cy="dropbox-oauth"
                     className="block"
                     onClick={this.openNewWindow}
                  >
                     <h2 className="uppercase font-bold mb-4">
                        Connect to{" "}
                        <img
                           alt="Dropbox"
                           src={dropbox}
                           className="h-8 mx-auto"
                        />
                     </h2>
                  </a>
               </>
            )}
            <p>
               We will save screenshots of your recipes in your Dropbox account.
            </p>
         </>
      );
   }
}

export default DropboxStep;

function ErrorMessage(props) {
   if (props.msg === "") {
      return null;
   }

   return (
      <p
         data-cy="dropbox-oauth-fail"
         className="px-2 py-4 bg-red-200 mb-8 text-red-900 font-bold text-sm"
      >
         {props.msg}
      </p>
   );
}
