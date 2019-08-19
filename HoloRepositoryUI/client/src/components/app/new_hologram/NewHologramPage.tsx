import React, { Component, ReactNode } from "react";
import { navigate, RouteComponentProps } from "@reach/router";
import PlainContentContainer from "../core/PlainContentContainer";
import BackendServerService from "../../../services/BackendServerService";
import CreationModeSelectionStep from "./shared/CreationModeSelectionStep";
import ImagingStudySelectionStep from "./generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "./generate/PipelineSelectionStep";
import DetailsDeclarationStep from "./shared/DetailsDeclarationStep";
import FileUploadStep from "./upload/FileUploadStep";
import UploadProcessingStep from "./upload/UploadProcessingStep";
import NewHologramControlsAndProgress from "./shared/NewHologramControlsAndProgress";
import GenerationProcessingStep from "./generate/GenerationProcessingStep";
import { HologramCreationMode } from "../../../types";
import {
  IAuthor,
  IHologram,
  IHologramCreationRequest,
  IHologramCreationRequest_Generate,
  IHologramCreationRequest_Upload,
  IPractitioner
} from "../../../../../types";
import { PropsWithContext, withAppContext } from "../../shared/AppState";
import Formsy from "formsy-react";

export interface IHologramCreationStep {
  title: string;
  content: ReactNode;
}

export interface IHologramCreationSteps {
  [HologramCreationMode.GENERATE_FROM_IMAGING_STUDY]: IHologramCreationStep[];
  [HologramCreationMode.UPLOAD_EXISTING_MODEL]: IHologramCreationStep[];
}

type INewHologramPageProps = RouteComponentProps & PropsWithContext;

interface INewHologramPageInternalState {
  currentStep: number;
  currentStepIsValid: boolean;
  creationMode: HologramCreationMode;
}

interface IHologramCreationData_Upload {
  hologramFile: File;
}

interface IHologramCreationData_Generate {
  plid: string;
  imagingStudyEndpoint: string;
}

// Union with relecant partial interfaces to allow subsequent filling of the respective fields
type INewHologramPageState = INewHologramPageInternalState &
  Partial<IHologramCreationData_Upload> &
  Partial<IHologramCreationData_Generate> &
  Partial<IHologramCreationRequest>;

class NewHologramPage extends Component<INewHologramPageProps, INewHologramPageState> {
  state: INewHologramPageState = {
    currentStep: 0,
    currentStepIsValid: false,
    creationMode:
      (this.props.location &&
        this.props.location.state &&
        (this.props.location.state.mode as HologramCreationMode)) ||
      HologramCreationMode.GENERATE_FROM_IMAGING_STUDY
  };

  private _handleSubmit_Upload = () => {
    const metaData = this._getPostRequestMetaData_Upload();
    if (!metaData) {
      return this._logErrorAndReturnNull();
    }
    BackendServerService.uploadHologram(metaData).then(response => {
      if (response) {
        this._handleUploadHologram_Success(response);
      } else {
        this._handleUploadHologram_Failure();
      }
    });
  };

  private _handleUploadHologram_Success = (hologram: IHologram) => {
    // Update global state
    this.props.context!.handleHologramCreated(hologram);

    console.log("Upload successful");
    navigate("/app/holograms");
  };

  private _handleUploadHologram_Failure = () => {
    console.error("Something went wrong while creating the hologram, try refreshing the page.");

    // Note: Should have better error handling
    navigate("/app/holograms");
  };

  private _handleSubmit_Generate = () => {
    const metaData = this._getPostRequestMetaData_Generate();
    if (!metaData) {
      return this._logErrorAndReturnNull();
    }
    BackendServerService.generateHologram(metaData).then(response => console.log(response)); // boolean
  };

  private _generatePostRequestMetaData_Shared = (): IHologramCreationRequest | null => {
    const { title, description, bodySite, dateOfImaging } = this.state;
    const { patients, selectedPatientId, practitioner } = this.props.context!;
    const patient = selectedPatientId && patients[selectedPatientId];

    if (!practitioner || !patient) {
      return this._logErrorAndReturnNull();
    }

    return {
      patient: patient,
      author: this._transformPractitionerToAuthor(practitioner),
      title: title || "",
      description: description || "",
      bodySite: bodySite || "",
      dateOfImaging: dateOfImaging || ""
    };
  };

  private _getPostRequestMetaData_Upload = (): IHologramCreationRequest_Upload | null => {
    const { hologramFile } = this.state;
    const sharedMetaData = this._generatePostRequestMetaData_Shared();
    if (!hologramFile || !sharedMetaData) {
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
      hologramFile,
      ...sharedMetaData,
      ...originalUploadData
    };
  };

  private _getPostRequestMetaData_Generate = (): IHologramCreationRequest_Generate | null => {
    const { plid, imagingStudyEndpoint } = this.state;
    const medicalData = this._generatePostRequestMetaData_Shared();
    if (!plid || !imagingStudyEndpoint || !medicalData) {
      return this._logErrorAndReturnNull();
    }

    return {
      plid,
      imagingStudyEndpoint,
      medicalData
    };
  };

  private _transformPractitionerToAuthor = (practitioner: IPractitioner): IAuthor => {
    const result: any = Object.assign({}, practitioner);
    result["aid"] = result["pid"];
    delete result["pid"];
    return result;
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
        content: <CreationModeSelectionStep selected={this.state.creationMode} />
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
        content: <DetailsDeclarationStep enablePatientSelection={false} />
      },
      {
        title: "Process",
        content: <GenerationProcessingStep onComponentDidMount={this._handleSubmit_Generate} />
      }
    ],
    [HologramCreationMode.UPLOAD_EXISTING_MODEL]: [
      {
        title: "Select mode",
        content: <CreationModeSelectionStep selected={this.state.creationMode} />
      },
      {
        title: "Upload file",
        content: <FileUploadStep />
      },
      {
        title: "Enter details",
        content: <DetailsDeclarationStep enablePatientSelection={true} />
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

        <Formsy
          onSubmit={this._handleCurrentStepSubmit}
          onValid={() => this.setState({ currentStepIsValid: true })}
          onInvalid={() => this.setState({ currentStepIsValid: false })}
        >
          <div className="steps-content" style={{ minHeight: "500px" }}>
            {steps[currentStep].content}
          </div>

          <NewHologramControlsAndProgress
            current={currentStep}
            currentStepIsValid={this.state.currentStepIsValid}
            steps={steps}
            onGoToPrevious={this._goToPreviousStep}
          />
        </Formsy>
      </PlainContentContainer>
    );
  }

  private _handleCurrentStepSubmit = (formData: Record<string, any>) => {
    console.log("Submitted data: ", formData);
    // @ts-ignore and manually guarantee that the formData keys match this.state
    this.setState({
      ...formData
    });
    this._goToNextStep();
  };

  private _goToNextStep = () => {
    this.setState((state: Readonly<INewHologramPageState>) => ({
      currentStep: state.currentStep + 1
    }));
  };

  private _goToPreviousStep = () => {
    this.setState((state: Readonly<INewHologramPageState>) => ({
      currentStep: state.currentStep - 1
    }));
  };
}

export default withAppContext(NewHologramPage);
