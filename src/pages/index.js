import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"
import Step from "../components/step"

import dropbox from "../images/dropbox.svg"
import styles from "../css/form.module.css"

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <Step>
      <a href="/" className="uppercase font-bold">
        <h2>
          Connect to <img alt="Dropbox" src={dropbox} className="h-8" />
        </h2>
      </a>
    </Step>
    <Step>
      <h2 className="uppercase font-bold mb-4">
        Enter your Pepperplate credentials
      </h2>
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
    </Step>
  </Layout>
)

export default IndexPage
