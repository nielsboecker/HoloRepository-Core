import React, { Component, ReactNode } from "react";
import { Steps, Button, message } from "antd";
import { RouteComponentProps } from "@reach/router";
import PlainContentContainer from "../core/PlainContentContainer";

import samplePatients from "../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../__tests__/samples/samplePatientsWithHolograms.json";
import { HologramCreationMode, IPatient } from "../../../types";
import CreationModeSelectionStep from "./CreationModeSelectionStep";
import ImagingStudySelectionStep from "./generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "./generate/PipelineSelectionStep";
import DetailsDeclarationStep from "./DetailsDeclarationStep";
import PipelineProcessingStep from "./generate/PipelineProcessingStep";
import FileUploadStep from "./upload/FileUploadStep";
import UploadProcessingStep from "./upload/UploadProcessingStep";

const { Step } = Steps;

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

  private allPatients = [...samplePatients, ...samplePatientsWithHolograms].sort((a, b) =>
    a.name.full.localeCompare(b.name.full)
  ) as IPatient[];

  _handleModeChange = (creationMode: HologramCreationMode) => {
    this.setState({ creationMode });
    console.log(creationMode, this.state);
  };

  private _allSteps: IHologramCreationSteps = {
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
        title: "Select processing pipeline",
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
    const steps = this._allSteps[this.state.creationMode];

    return (
      <PlainContentContainer>
        <h1>Create new hologram</h1>

        <div className="steps-content" style={{ minHeight: "500px" }}>
          {steps[current].content}
        </div>

        <Steps current={current}>
          {steps.map(item => (
            <Step key={item.title} title={item.title} />
          ))}
        </Steps>

        <div className="steps-action">
          {current < steps.length - 1 && (
            <Button type="primary" onClick={() => this.next()}>
              Next
            </Button>
          )}
          {current === steps.length - 1 && (
            <Button type="primary" onClick={() => message.success("Processing complete!")}>
              Done
            </Button>
          )}
          {current > 0 && (
            <Button style={{ marginLeft: 8 }} onClick={() => this.prev()}>
              Previous
            </Button>
          )}
        </div>
      </PlainContentContainer>
    );
  }

  next() {
    // TODO: use other setState
    const current: number = this.state.current + 1;
    this.setState({ current });
  }

  prev() {
    const current = this.state.current - 1;
    this.setState({ current });
  }
}

export default NewHologramPage;
