import React from "react"

import "../css/global.css"

class DropboxFinishPage extends React.Component {
  constructor() {
    super()
    this.state = { 
      isFinal: false,
      isError: false,
      finalMessage: "",
    }
  }
  
  componentDidMount() {
    if (window.opener === null) {
      this.setState({ 
        isFinal: true,
        isError: true,
        finalMessage: "You are not supposed to visit this URL directly, sire!"
      });
    }
  }
  
  render() {
    return (
      <>
        { !this.state.isFinal && 
          <p>Finishing up oAuth flow...</p>
        }
        
        { this.state.isError &&
          <>
            <p data-cy="errorText">{this.state.finalMessage}</p>
            <p>Go <a href="/" className="text-blue-900">Home</a></p>
          </>
        }
      </>
    )
  }
}

export default DropboxFinishPage