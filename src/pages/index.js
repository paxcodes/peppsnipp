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
    <Step className="max-w-lg">
      <h2 className="uppercase font-bold mb-4">
        Let the App Download Your Recipes
      </h2>
      <p>
        The app will take a screenshot of your recipes and upload them to your
        Dropbox account
      </p>
    </Step>
  </Layout>
)

export default IndexPage
