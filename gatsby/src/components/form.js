import React from "react";

import styles from "../css/form.module.css";

class Form extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         startLoginProcess: false
      };
   }

   loginToPepperplate = e => {
      e.preventDefault();
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
            <button
               data-cy="submitBtn"
               className={`bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${styles.button}`}
               onClick={this.loginToPepperplate}
            >
               Start snipping my recipes!
            </button>
         </form>
      );
   }
}

export default Form;
