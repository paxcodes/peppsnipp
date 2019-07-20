import React from "react"

import styles from "../css/form.module.css"

const Form = () => (
  <form className={styles.form}>
    <label className="text-gray-700">Username</label>
    <input
      type="text"
      className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
    />
    <label className="text-gray-700">Password</label>
    <input
      type="password"
      className="shadow border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-inner"
    />
    <button
      className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${styles.button}`}
    >
      Start snipping my recipes!
    </button>
  </form>
)

export default Form
