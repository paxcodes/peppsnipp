import React from "react";

import styles from "../css/form.module.css";
import spinner from "../images/spinner.svg";

class Form extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         startLoginProcess: false
      };
   }

   loginToPepperplate = e => {
      e.preventDefault();
      this.setState({ startLoginProcess: true });
   };

   render() {
      return (
         <form className={styles.form}>
            <label id="username" className="text-gray-700">
               Username
            </label>
            <input
               data-cy="usernameField"
               aria-labelledby="username"
               type="text"
               className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
            />
            <label id="password" className="text-gray-700">
               Password
            </label>
            <input
               data-cy="passwordField"
               aria-labelledby="password"
               type="password"
               className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
            />
            <div className={`${styles.buttonContainer} relative`}>
               <button
                  data-cy="submitBtn"
                  className={`bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full`}
                  onClick={this.loginToPepperplate}
                  disabled={this.state.startLoginProcess}
               >
                  Start snipping my recipes!
               </button>
               <LoadingAnimation show={this.state.startLoginProcess} />
            </div>
         </form>
      );
   }
}

export default Form;

function LoadingAnimation(props) {
   if (!props.show) {
      return null;
   }

   return (
      <img
         className="absolute top-0 w-full"
         style={{ height: 40 + "px" }}
         src={spinner}
         alt="logging in..."
         data-cy="loadingAnimation"
      />
   );
}
