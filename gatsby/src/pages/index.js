import React from "react"
import Layout from "../components/layout"
import SEO from "../components/seo"
import Step from "../components/step"
import Form from "../components/form"
import DropboxStep from "../components/dropbox-step"


const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <Step>
      <DropboxStep />
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
