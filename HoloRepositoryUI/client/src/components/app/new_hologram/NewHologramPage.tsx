import React, { Component, ReactNode } from "react";
import { RouteComponentProps } from "@reach/router";
import PlainContentContainer from "../core/PlainContentContainer";

import CreationModeSelectionStep from "./shared/CreationModeSelectionStep";
import ImagingStudySelectionStep from "./generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "./generate/PipelineSelectionStep";
import DetailsDeclarationStep from "./shared/DetailsDeclarationStep";
import FileUploadStep from "./upload/FileUploadStep";
import UploadProcessingStep from "./upload/UploadProcessingStep";
import NewHologramControlsAndProgress from "./shared/NewHologramControlsAndProgress";
import GenerationProcessingStep from "./generate/GenerationProcessingStep";
import { HologramCreationMode } from "../../../types";

export interface IHologramCreationStep {
  title: string;
  content: ReactNode;
}

export interface IHologramCreationSteps {
  [HologramCreationMode.generateFromImagingStudy]: IHologramCreationStep[];
  [HologramCreationMode.uploadExistingModel]: IHologramCreationStep[];
}

interface IAddHologramPageState {
  currentStep: number;
  creationMode: HologramCreationMode;
}

class NewHologramPage extends Component<RouteComponentProps, IAddHologramPageState> {
  state = {
    currentStep: 0,
    creationMode:
      (this.props.location &&
        this.props.location.state &&
        (this.props.location.state.mode as HologramCreationMode)) ||
      HologramCreationMode.generateFromImagingStudy
  };

  private _handleModeChange = (creationMode: HologramCreationMode) => {
    this.setState({ creationMode });
  };

  private _steps: IHologramCreationSteps = {
    [HologramCreationMode.generateFromImagingStudy]: [
      {
        title: "Select mode",
        content: (
          <CreationModeSelectionStep
            selected={this.state.creationMode}
            handleModeChange={this._handleModeChange}
          />
        )
      },
      {
        title: "Select pipeline",
        content: <PipelineSelectionStep />
      },
      {
        title: "Select input data",
        content: <ImagingStudySelectionStep />
      },
      {
        title: "Enter details",
        content: <DetailsDeclarationStep />
      },
      {
        title: "Process",
        content: <GenerationProcessingStep />
      }
    ],
    [HologramCreationMode.uploadExistingModel]: [
      {
        title: "Select mode",
        content: (
          <CreationModeSelectionStep
            selected={this.state.creationMode}
            handleModeChange={this._handleModeChange}
          />
        )
      },
      {
        title: "Upload file",
        content: <FileUploadStep />
      },
      {
        title: "Enter details",
        content: <DetailsDeclarationStep />
      },
      {
        title: "Process",
        content: <UploadProcessingStep />
      }
    ]
  };

  render() {
    const { currentStep } = this.state;
    const steps = this._steps[this.state.creationMode];

    return (
      <PlainContentContainer>
        <h1>Create new hologram</h1>

        <div className="steps-content" style={{ minHeight: "500px" }}>
          {steps[currentStep].content}
        </div>

        <NewHologramControlsAndProgress
          current={currentStep}
          steps={steps}
          handlePrevious={this._prev}
          handleNext={this._next}
        />
      </PlainContentContainer>
    );
  }

  private _next = () => {
    this.setState((state: Readonly<IAddHologramPageState>) => ({
      currentStep: state.currentStep + 1
    }));
  };

  private _prev = () => {
    this.setState((state: Readonly<IAddHologramPageState>) => ({
      currentStep: state.currentStep - 1
    }));
  };
}

export default NewHologramPage;
