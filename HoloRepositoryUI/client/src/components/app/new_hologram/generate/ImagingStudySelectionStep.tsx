import React, { Component } from "react";
import { IImagingStudy, IPatient } from "../../../../../../types";
import { IChoiceGroupOption, IDropdownOption, MessageBar, MessageBarType } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import ImagingStudyDetailsCard from "./ImagingStudyDetailsCard";
import { PropsWithContext, withAppContext } from "../../../shared/AppState";
import ImagingStudySelectionInput from "./inputs/ImagingStudySelectionInput";
import PatientForImagingStudySelectionInput from "./inputs/PatientForImagingStudySelectionInput";

export interface IImagingStudySelectionStepProps extends PropsWithContext {
}

export interface IImagingStudySelectionStepState {
  selectedPatient?: IPatient;
  selectedStudy?: IImagingStudy;
}

export interface IExtendedChoiceGroupOption extends IChoiceGroupOption {
  endpoint: string;
}

class ImagingStudySelectionStep extends Component<IImagingStudySelectionStepProps,
  IImagingStudySelectionStepState> {
  state: IImagingStudySelectionStepState = {};

  render() {
    return (
      <Row>
        <Col span={8}>
          <PatientForImagingStudySelectionInput
            patientOptions={this._mapPatientsToDropdownOptions()}
            onPatientChange={this._handlePatientChange}
            name="pid"
            required
          />

          <Divider/>

          <MessageBar messageBarType={MessageBarType.warning} style={{ marginBottom: "10px" }}>
            The system is currently not performing any input validation on the selected imaging
            studies. Please ensure that the selected study depicts the correct body site for the
            selected pipeline.
          </MessageBar>

          {this.state.selectedPatient &&
          this.state.selectedPatient.imagingStudies &&
          this.state.selectedPatient.imagingStudies.length >= 1 ? (
            <ImagingStudySelectionInput
              imagingStudyOptions={this._getImagingStudyOptions()}
              onImagingStudyChange={this._handleImagingStudyChange}
              name="imagingStudyEndpoint"
              required
            />
          ) : (
            <p>Select a patient with existing imaging studies.</p>
          )}
        </Col>

        <Col span={14} offset={2}>
          <ImagingStudyDetailsCard study={this.state.selectedStudy}/>
        </Col>
      </Row>
    );
  }

  private _mapPatientsToDropdownOptions = (): IDropdownOption[] => {
    const { patients } = this.props.context!;

    return Object.entries(patients).map(([pid, patient]) => ({
      key: pid,
      text: `${patient.name.full} (${ImagingStudySelectionStep._getNumberOfStudies(
        patient
      )} studies)`,
      disabled: !patient.imagingStudies || patient.imagingStudies.length === 0
    }));
  };

  private _handlePatientChange = (pid: string) => {
    const { patients } = this.props.context!;
    this.setState({ selectedPatient: patients[pid], selectedStudy: undefined });
  };

  // Note: Not ideal. Should be refactored.
  private _handleImagingStudyChange = (isid: string) => {
    if (!this.state.selectedPatient || !this.state.selectedPatient.imagingStudies) {
      return;
    }
    const selectedStudy = this.state.selectedPatient.imagingStudies.find(is => is.isid === isid);
    if (selectedStudy) {
      this.setState({ selectedStudy });
    }
  };

  private _getImagingStudyOptions = (): IExtendedChoiceGroupOption[] => {
    if (!this.state.selectedPatient || !this.state.selectedPatient.imagingStudies) {
      return [];
    }
    return this.state.selectedPatient.imagingStudies.map((is, index) => ({
      key: is.isid,
      text: `Imaging study ${index + 1} (${is.numberOfInstances} instances)`,
      endpoint: is.endpoint
    }));
  };

  private static _getNumberOfStudies(patient: IPatient) {
    return patient.imagingStudies ? patient.imagingStudies.length : 0;
  }
}

export default withAppContext(ImagingStudySelectionStep);
