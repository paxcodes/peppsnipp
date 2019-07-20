import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"
import Step from "../components/step"

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
  </Layout>
)

export default IndexPage
