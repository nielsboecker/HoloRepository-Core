import React, { Component, ReactNode } from "react";
import { RouteComponentProps } from "@reach/router";
import PlainContentContainer from "../core/PlainContentContainer";

import { HologramCreationMode } from "../../../types";
import CreationModeSelectionStep from "./CreationModeSelectionStep";
import ImagingStudySelectionStep from "./generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "./generate/PipelineSelectionStep";
import DetailsDeclarationStep from "./DetailsDeclarationStep";
import PipelineProcessingStep from "./generate/PipelineProcessingStep";
import FileUploadStep from "./upload/FileUploadStep";
import UploadProcessingStep from "./upload/UploadProcessingStep";
import NewHologramControlsAndProgress from "./NewHologramControlsAndProgress";

export interface IHologramCreationStep {
  title: string;
  content: ReactNode;
}

export interface IHologramCreationSteps {
  [HologramCreationMode.generateFromImagingStudy]: IHologramCreationStep[];
  [HologramCreationMode.uploadExistingModel]: IHologramCreationStep[];
}

interface IAddHologramPageState {
  current: number;
  creationMode: HologramCreationMode;
  //steps: IHologramCreationStep[];
}

class NewHologramPage extends Component<RouteComponentProps, IAddHologramPageState> {
  state = {
    current: 0,
    creationMode: HologramCreationMode.generateFromImagingStudy
    //steps: allSteps[HologramCreationMode.generateFromImagingStudy]
  };

  private _handleModeChange = (creationMode: HologramCreationMode) => {
    this.setState({ creationMode });
    console.log(creationMode, this.state);
  };

  private _steps: IHologramCreationSteps = {
    [HologramCreationMode.generateFromImagingStudy]: [
      {
        title: "Select mode",
        content: <CreationModeSelectionStep handleModeChange={this._handleModeChange} />
      },
      {
        title: "Select input data",
        content: <ImagingStudySelectionStep />
      },
      {
        title: "Select pipeline",
        content: <PipelineSelectionStep />
      },
      {
        title: "Enter details",
        content: <DetailsDeclarationStep />
      },
      {
        title: "Process",
        content: <PipelineProcessingStep />
      }
    ],
    [HologramCreationMode.uploadExistingModel]: [
      {
        title: "Select mode",
        content: <CreationModeSelectionStep handleModeChange={this._handleModeChange} />
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
    const { current } = this.state;
    const steps = this._steps[this.state.creationMode];

    return (
      <PlainContentContainer>
        <h1>Create new hologram</h1>

        <div className="steps-content" style={{ minHeight: "500px" }}>
          {steps[current].content}
        </div>

        <NewHologramControlsAndProgress
          current={current}
          steps={steps}
          handlePrevious={this._prev}
          handleNext={this._next}
        />
      </PlainContentContainer>
    );
  }

  private _next = () => {
    // TODO: use other setState
    const current: number = this.state.current + 1;
    this.setState({ current });
  };

  private _prev = () => {
    const current = this.state.current - 1;
    this.setState({ current });
  };
}

export default NewHologramPage;
