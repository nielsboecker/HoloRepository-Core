import React, { Component } from "react";

import "./ContentContainer.scss";

class ContentContainer extends Component {
  render() {
    return <div className="ContentContainer">{this.props.children}</div>;
  }
}

export default ContentContainer;
