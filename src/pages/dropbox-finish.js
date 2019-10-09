import React from "react"
import axios from "axios"

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
    else {
      this.origin = this.props.location.protocol + "//" + this.props.location.hostname + ":" +
      this.props.location.port;
      const query = window.location.search.substring(1);
      axios.get(`${process.env.API_URL}/dropbox/finish?${query}`, {
        withCredentials: true
      })
        .then(response => {
          window.opener.postMessage(response.data, this.origin)
        })
        .catch(error => {
          window.opener.postMessage(error.response.data, this.origin)
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