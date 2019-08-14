import React, { Component } from "react";
import { Icon, MessageBar, Spinner } from "office-ui-fabric-react";
import { navigate } from "@reach/router";

export interface IGenerationProcessingStepProps {
  onComponentDidMount: () => void;
}

export interface IGenerationProcessingStepState {
  finished: boolean;
  message: string;
}
class GenerationProcessingStep extends Component<
  IGenerationProcessingStepProps,
  IGenerationProcessingStepState
> {
  state = {
    finished: false,
    message: "Preprocessing image data..."
  };

  render() {
    if (!this.state.finished) {
      return (
        <>
          <div style={{ marginBottom: "24px" }}>
            <MessageBar>
              The pipeline has received your data and started processing. The next steps may take a
              few moments, you don't have to stay on this page.
            </MessageBar>
          </div>

          <div>
            <Spinner label={this.state.message} />
          </div>
        </>
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
    // Note: This is not ideal; using callback upon component render to start the upload
    this.props.onComponentDidMount();

    // Mock progress status for now
    setTimeout(() => this.setState({ message: "Generating hologram from imaging study..." }), 2500);
    setTimeout(() => this.setState({ message: "Sending data to HoloRepository..." }), 5000);
    setTimeout(() => this.setState({ finished: true }), 7500);
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

export default GenerationProcessingStep;
