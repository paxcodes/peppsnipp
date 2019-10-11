import React from "react"
import dropbox from "../images/dropbox.svg"

const DropboxStep = () => {
  let popup;
  function openNewWindow(e) {
    e.preventDefault();
    popup = window.top.open(e.currentTarget.attributes.href.value, "DropboxOAuth", "width=670, height=825, location=0");
    window.addEventListener('message', updateDropboxStep)
  }
  
  function updateDropboxStep(e) {
    
    popup.close()
  }
  
  return (
    <>
      <a href={`${process.env.API_URL}/dropbox/start`} data-cy="dropbox-oauth" className="block" onClick={openNewWindow}>
        <h2 className="uppercase font-bold mb-4">
          Connect to <img alt="Dropbox" src={dropbox} className="h-8 mx-auto" />
        </h2>
      </a>
      <p>We will save screenshots of your recipes in your Dropbox account.</p>
    </>
  )
}

export default DropboxStep