import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

import logo from "../images/camera.svg"
import styles from "../css/header.module.css"

const Header = ({ siteTitle }) => (
  <header>
    <h1 className={`text-4xl p-8 ${styles.header}`}>
      <Link to="/">
        <img alt="" src={logo} className={`rounded-full mb-8 ${styles.logo}`} />
      </Link>
      <Link to="/">{siteTitle}</Link>
    </h1>
  </header>
)

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
