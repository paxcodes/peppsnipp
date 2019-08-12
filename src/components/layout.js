/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from "react"
import PropTypes from "prop-types"
import { useStaticQuery, graphql } from "gatsby"

import Header from "./header"
import "../css/global.css"

const Layout = ({ children }) => {
  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `)

  return (
    <div className="root container mx-auto px-5 text-gray-900 bg-blue-100">
      <Header siteTitle={data.site.siteMetadata.title} />
      <main className="text-center" style={{maxWidth: 420}}>{children}</main>
      <footer className="p-8">
        © {new Date().getFullYear()} Built by{" "}
        <a
          href="https://margret.pw"
          className="border-b border-dotted text-gray-700"
        >
          Pax
        </a>{" "}
        with Gatsby 🚀
      </footer>
    </div>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
