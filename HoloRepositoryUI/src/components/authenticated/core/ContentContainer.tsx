import React, { Component } from "react";
import "./ContentContainer.scss";
import { Divider } from "antd";

interface IContentContainerProps {
  title: string;
  description: string[];
}

class ContentContainer extends Component<IContentContainerProps> {
  render() {
    return (
      <div className="ContentContainer">
        <h1>{this.props.title}</h1>

        {this.props.description.map(description => (
          <p>{description}</p>
        ))}

        <Divider />

        <div>{this.props.children}</div>
      </div>
    );
  }
}

export default ContentContainer;
