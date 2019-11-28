import React from "react";
import axios from "axios";

import styles from "../css/form.module.css";
import spinner from "../images/spinner.svg";

class Form extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         email: "",
         password: "",
         startLoginProcess: false
      };
   }

   loginToPepperplate = e => {
      e.preventDefault();
      this.setState({ startLoginProcess: true });
      axios
         .post(`${process.env.API_URL}/pepperplate/session`, {
            email: this.state.email,
            password: this.state.password
         })
         .then(response => {})
         .catch(error => {})
         .finally(() => {
            this.setState({ startLoginProcess: false });
         });
   };

   handleChange = event => {
      const target = event.target;
      const value = target.value;
      const name = target.name;
      this.setState({
         [name]: value
      });
   };

   render() {
      return (
         <form className={styles.form}>
            <label id="email" className="text-gray-700">
               Email
            </label>
            <input
               data-cy="emailField"
               name="email"
               aria-labelledby="email"
               type="text"
               className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
               value={this.state.email}
               onChange={this.handleChange}
            />
            <label id="password" className="text-gray-700">
               Password
            </label>
            <input
               data-cy="passwordField"
               name="password"
               aria-labelledby="password"
               type="password"
               className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
               value={this.state.password}
               onChange={this.handleChange}
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
