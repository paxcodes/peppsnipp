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
  </form>
)

export default Form
