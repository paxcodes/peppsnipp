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
      <a href={`${process.env.API_URL}/dropbox/start`} data-cy="dropbox-oauth" className="block">
        <h2 className="uppercase font-bold mb-4">
          Connect to <img alt="Dropbox" src={dropbox} className="h-8 mx-auto" />
        </h2>
      </a>
      <p>We will save screenshots of your recipes in your Dropbox account.</p>
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
