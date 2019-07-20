import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"
import Step from "../components/step"
import Form from "../components/form"

import dropbox from "../images/dropbox.svg"

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
      <Form />
    </Step>
  </Layout>
)

export default IndexPage
