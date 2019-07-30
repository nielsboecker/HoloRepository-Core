import React, { Component } from "react";
import { Divider } from "antd";
import { IPipeline } from "../../../../../../types";
import { CommandBarButton, Icon, IconButton, Image, Modal } from "office-ui-fabric-react";

const style = { backgroundColor: "#eee", padding: "24px", marginTop: "31px" };

export interface IPipelineProfileCardProps {
  pipeline?: IPipeline;
}

export interface IPipelineProfileCardState {
  showSampleInputModal: boolean;
  showSampleOutputModal: boolean;
}

class PipelineSpecificationCard extends Component<
  IPipelineProfileCardProps,
  IPipelineProfileCardState
> {
  state = {
    showSampleInputModal: false,
    showSampleOutputModal: false
  };

  private _closeModal = (): void => {
    this.setState({ showSampleInputModal: false, showSampleOutputModal: false });
  };

  private _modalCloseButton = (
    <IconButton
      iconProps={{ iconName: "ChromeClose" }}
      title="Close"
      ariaLabel="Close"
      onClick={this._closeModal}
      style={{
        right: "0",
        top: "0",
        position: "absolute",
        zIndex: 1,
        margin: "12px",
        backgroundColor: "rgba(255, 255, 255, 0.7)"
      }}
    />
  );

  render() {
    if (this.props.pipeline) {
      const { pipeline } = this.props;

      return (
        <div style={style}>
          <h2>{pipeline.title}</h2>
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
              onClick={() => this.setState({ showSampleInputModal: true })}
              style={{ marginRight: "24px" }}
            />
            <Modal
              titleAriaId="Sample input"
              isOpen={this.state.showSampleInputModal}
              onDismiss={this._closeModal}
              isBlocking={false}
            >
              {this._modalCloseButton}
              <Image
                src={pipeline.inputExampleImageUrl}
                alt="Sample input"
                style={{ maxHeight: "75vh", padding: "12px" }}
              />
            </Modal>

            <CommandBarButton
              iconProps={{ iconName: "HealthSolid" }}
              text="Sample output"
              disabled={!pipeline.outputExampleImageUrl}
              onClick={() => this.setState({ showSampleOutputModal: true })}
            />
            <Modal
              titleAriaId="Sample output"
              isOpen={this.state.showSampleOutputModal}
              onDismiss={this._closeModal}
              isBlocking={false}
            >
              {this._modalCloseButton}
              <Image
                src={pipeline.outputExampleImageUrl}
                alt="Sample output"
                style={{ maxHeight: "75vh", padding: "12px" }}
              />
            </Modal>
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
