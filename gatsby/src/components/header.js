import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

import logo from "../images/camera.svg"
import styles from "../css/header.module.css"

const Header = ({ siteTitle }) => (
  <header>
    <Link to="/">
      <h1 className={`text-4xl p-8 ${styles.header}`}>
        <img alt="" src={logo} className={`rounded-full mb-8 ${styles.logo}`} />
        <span>{siteTitle}</span>
      </h1>
    </Link>
  </header>
)

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
