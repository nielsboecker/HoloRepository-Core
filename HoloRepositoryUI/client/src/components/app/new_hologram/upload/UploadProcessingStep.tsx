import React, { Component } from "react";
import { Icon, Spinner } from "office-ui-fabric-react";
import { navigate } from "@reach/router";

class UploadProcessingStep extends Component<any, { finished: boolean }> {
  state = {
    finished: false
  };

  render() {
    //<ProgressIndicator label="Example title" description="Example description" />
    if (!this.state.finished) {
      return (
        <div>
          <Spinner label="Sending data to HoloRepository..." />
        </div>
      );
    } else {
      return (
        <div>
          <Icon iconName="Accept" />
          <strong>All done!</strong>
          <p>Your hologram is now stored in the HoloRepository.</p>
        </div>
      );
    }
  }

  componentDidMount(): void {
    setTimeout(() => this.setState({ finished: true }), 2500);
  }

  componentDidUpdate(
    prevProps: Readonly<any>,
    prevState: Readonly<{ finished: boolean }>,
    snapshot?: any
  ): void {
    if (!prevState.finished && this.state.finished) {
      setTimeout(() => {
        navigate("/app/holograms");
      }, 2500);
    }
  }
}

export default UploadProcessingStep;
