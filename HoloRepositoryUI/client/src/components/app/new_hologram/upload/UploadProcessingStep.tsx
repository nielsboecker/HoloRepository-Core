import React, { Component } from "react";
import { Spinner } from "office-ui-fabric-react";

export interface IUploadProcessingStepProps {
  onComponentDidMount: () => void;
}

class UploadProcessingStep extends Component<IUploadProcessingStepProps> {
  render() {
    return (
      <div>
        <Spinner label="Sending data to HoloRepository..." />
      </div>
    );
  }

  componentDidMount(): void {
    // Note: This is not ideal; using callback upon component render to start the upload
    this.props.onComponentDidMount();
  }
}

export default UploadProcessingStep;
