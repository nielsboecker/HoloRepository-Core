import React, { Component } from "react";
import { IImagingStudy } from "../../../../../../types";
import { CommandBarButton, Icon, IconButton, Image, Modal } from "office-ui-fabric-react";
import { Divider } from "antd";

// Note:  Component should be refactored and combined with PipelineSpecificationCard

const style = { backgroundColor: "#eee", padding: "24px", marginTop: "31px" };

export interface IImagingStudyDetailsCardProps {
  study?: IImagingStudy;
}

export interface IImagingStudyDetailsCardState {
  showPreviewModal: boolean;
}

class ImagingStudyDetailsCard extends Component<
  IImagingStudyDetailsCardProps,
  IImagingStudyDetailsCardState
> {
  state = {
    showPreviewModal: false
  };

  private _modalCloseButton = (
    <IconButton
      iconProps={{ iconName: "ChromeClose" }}
      title="Close"
      ariaLabel="Close"
      onClick={() => this.setState({ showPreviewModal: false })}
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
    if (this.props.study) {
      const { study } = this.props;

      return (
        <div style={style}>
          <h2>Imaging study</h2>
          <ul>
            <li>Number of instances: {study.numberOfInstances}</li>
            <li>Body site: {study.bodySite || "Unknown"}</li>
            <li>Modality: {study.modality || "Unknown"}</li>
            <li>Date: {study.date ? new Date(study.date).toDateString() : "Unknown"}</li>
          </ul>

          <Divider />

          <h3>Preview</h3>
          <div style={{ display: "flex", alignItems: "stretch", height: "40px" }}>
            <CommandBarButton
              iconProps={{ iconName: "Stack" }}
              text="Show preview"
              disabled={!study.previewPictureUrl}
              onClick={() => this.setState({ showPreviewModal: true })}
              style={{ marginRight: "24px" }}
            />
            <Modal
              titleAriaId="Imaging study preview"
              isOpen={this.state.showPreviewModal}
              onDismiss={() => this.setState({ showPreviewModal: false })}
              isBlocking={false}
            >
              {this._modalCloseButton}
              <Image
                src={study.previewPictureUrl}
                alt="Imaging study preview"
                style={{ minHeight: "35vh", maxHeight: "75vh", padding: "12px" }}
              />
            </Modal>
          </div>
        </div>
      );
    } else {
      return (
        <div style={style}>
          <Icon iconName="Info" style={{ marginRight: "12px" }} />
          Select an imaging study to see more details.
        </div>
      );
    }
  }
}

export default ImagingStudyDetailsCard;
