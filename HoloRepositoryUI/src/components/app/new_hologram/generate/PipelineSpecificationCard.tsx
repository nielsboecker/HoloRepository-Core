import React, { Component } from "react";
import { Divider } from "antd";
import { IPipeline } from "../../../../types";
import { CommandBarButton, Icon } from "office-ui-fabric-react";

const style = { backgroundColor: "#eee", padding: "24px", marginTop: "31px" };

export interface IPipelineProfileCardProps {
  pipeline?: IPipeline;
}

class PipelineSpecificationCard extends Component<IPipelineProfileCardProps> {
  render() {
    if (this.props.pipeline) {
      const { pipeline } = this.props;

      return (
        <div style={style}>
          <h2>{pipeline.name}</h2>
          <p>{pipeline.description}</p>

          <Divider />

          <h3>Input constraints</h3>
          <ul>
            {pipeline.inputConstraints.map((contraints, index) => (
              <li key={index}>
                {contraints[0]}: <i>{contraints[1]}</i>
              </li>
            ))}
          </ul>

          <h3>Examples</h3>
          <div style={{ display: "flex", alignItems: "stretch", height: "40px" }}>
            <CommandBarButton
              iconProps={{ iconName: "Stack" }}
              text="Sample input"
              disabled={!pipeline.inputExampleImageUrl}
              style={{ marginRight: "24px" }}
            />
            <CommandBarButton
              iconProps={{ iconName: "HealthSolid" }}
              text="Sample output"
              disabled={!pipeline.outputExampleImageUrl}
            />
          </div>
        </div>
      );
    } else {
      return (
        <div style={style}>
          <Icon iconName="Info" style={{ marginRight: "12px" }} />
          Select a pipeline to see the specifications.
        </div>
      );
    }
  }
}

export default PipelineSpecificationCard;
