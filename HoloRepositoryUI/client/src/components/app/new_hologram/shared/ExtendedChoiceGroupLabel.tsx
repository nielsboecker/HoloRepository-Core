import React, { Component } from "react";
import { Icon } from "office-ui-fabric-react";

export interface ExtendedChoiceGroupLabelProps {
  title: string;
  description: string;
  iconName: string;
}
class ExtendedChoiceGroupLabel extends Component<ExtendedChoiceGroupLabelProps> {
  render() {
    return (
      <div style={{ paddingLeft: "26px" }}>
        <h3>
          <Icon iconName={this.props.iconName} style={{ marginRight: "6px" }} />
          {this.props.title}
        </h3>
        <p>{this.props.description}</p>
      </div>
    );
  }
}

export default ExtendedChoiceGroupLabel;
