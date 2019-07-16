import React, { Component } from "react";
import "./ContentContainer.scss";

class PlainContentContainer extends Component {
  render() {
    return (
      <div className="ContentContainer">
        <div>{this.props.children}</div>
      </div>
    );
  }
}

export default PlainContentContainer;
