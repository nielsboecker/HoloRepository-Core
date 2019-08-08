import React, { Component, ReactNode } from "react";
import { RouteComponentProps } from "@reach/router";
import PlainContentContainer from "../core/PlainContentContainer";
import BackendService from "../../../services/holoRepositoryServerService";
import CreationModeSelectionStep from "./shared/CreationModeSelectionStep";
import ImagingStudySelectionStep from "./generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "./generate/PipelineSelectionStep";
import DetailsDeclarationStep from "./shared/DetailsDeclarationStep";
import FileUploadStep from "./upload/FileUploadStep";
import UploadProcessingStep from "./upload/UploadProcessingStep";
import NewHologramControlsAndProgress from "./shared/NewHologramControlsAndProgress";
import GenerationProcessingStep from "./generate/GenerationProcessingStep";
import { HologramCreationMode } from "../../../types";
import { IHologramCreationRequest, IHologramCreationRequest_Upload } from "../../../../../types";
import { PropsWithContext, withAppContext } from "../../shared/AppState";

export interface IHologramCreationStep {
  title: string;
  content: ReactNode;
}

export interface IHologramCreationSteps {
  [HologramCreationMode.GENERATE_FROM_IMAGING_STUDY]: IHologramCreationStep[];
  [HologramCreationMode.UPLOAD_EXISTING_MODEL]: IHologramCreationStep[];
}

interface INewHologramPageInternalState {
  currentStep: number;
  creationMode: HologramCreationMode;
}

type INewHologramPageProps = RouteComponentProps & PropsWithContext;

type INewHologramPageState = INewHologramPageInternalState &
  Partial<IHologramCreationRequest> & { hologramFile?: File };

class NewHologramPage extends Component<INewHologramPageProps, INewHologramPageState> {
  state: INewHologramPageState = {
    currentStep: 0,
    creationMode:
      (this.props.location &&
        this.props.location.state &&
        (this.props.location.state.mode as HologramCreationMode)) ||
      HologramCreationMode.GENERATE_FROM_IMAGING_STUDY
  };

  private _handleModeChange = (creationMode: HologramCreationMode) => {
    this.setState({ creationMode });
  };

  private _handleHologramFileChange = (hologramFile: File) => {
    this.setState({ hologramFile });
  };

  private _handleSubmit_Upload = () => {
    const metaData = this._generatePostRequestMetaData_Upload();
    if (!metaData) {
      return this._logErrorAndReturnNull();
    }
    BackendService.uploadHologram(metaData).then(response => console.log(response)); // boolean
  };

  private _generatePostRequestMetaData_Upload = (): IHologramCreationRequest_Upload | null => {
    const { hologramFile, title, description, bodySite, dateOfImaging } = this.state;
    const { patients, selectedPatientId, practitioner } = this.props.context!;
    const patient = selectedPatientId && patients[selectedPatientId];

    if (!practitioner || !patient || !hologramFile) {
      return this._logErrorAndReturnNull();
    }

    const originalUploadData = {
      creationMode: HologramCreationMode.UPLOAD_EXISTING_MODEL,
      fileSizeInKb: (hologramFile.size / 1024).toFixed(0),
      creationDate: new Date().toISOString(),
      creationDescription: "Existing 3D model was uploaded via HoloRepository UI",
      contentType: "model/gltf-binary"
    };

    // @ts-ignore because of creationMode type definitions from different directories
    return {
      patient: patient,
      author: practitioner,
      hologramFile: hologramFile,
      title: title || "",
      description: description || "",
      bodySite: bodySite || "",
      dateOfImaging: dateOfImaging || "",
      ...originalUploadData
    };
  };

  private _logErrorAndReturnNull = (additionalMessage?: string): null => {
    // This should never happen
    console.error("Fatal error, aborting upload.", additionalMessage);
    return null;
  };

  private _steps: IHologramCreationSteps = {
    [HologramCreationMode.GENERATE_FROM_IMAGING_STUDY]: [
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
    [HologramCreationMode.UPLOAD_EXISTING_MODEL]: [
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
        content: <FileUploadStep onHologramFileChange={this._handleHologramFileChange} />
      },
      {
        title: "Enter details",
        content: <DetailsDeclarationStep />
      },
      {
        title: "Process",
        content: <UploadProcessingStep onComponentDidMount={this._handleSubmit_Upload} />
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
    this.setState((state: Readonly<INewHologramPageState>) => ({
      currentStep: state.currentStep + 1
    }));
  };

  private _prev = () => {
    this.setState((state: Readonly<INewHologramPageState>) => ({
      currentStep: state.currentStep - 1
    }));
  };
}

export default withAppContext(NewHologramPage);
