import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"

import dropbox from "../images/dropbox.svg"
import arrow from "../images/downarrow.svg"

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <a href="/" className="uppercase font-bold">
      Connect to <img alt="Dropbox" src={dropbox} className="h-8" />
    </a>
  </Layout>
)

export default IndexPage
