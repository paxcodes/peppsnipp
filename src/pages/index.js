import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"

import logo from "../images/camera.svg"

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <h1>Pepperplate Snipper</h1>
    <img src={logo} alt="Logo" />

    <a href="/">Connect to Dropbox</a>
  </Layout>
)

export default IndexPage
