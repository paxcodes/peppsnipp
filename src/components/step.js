import React from "react"
import PropTypes from "prop-types"

import arrow from "../images/downarrow.svg"
import styles from "../css/step.module.css"

const Step = ({ children }) => (
  <div className={styles.step}>
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full">
      {children}
    </div>
    <img src={arrow} alt="next step" className="my-10 h-6" />
  </div>
)

Step.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Step
