import React, { Component } from "react";
import { IImagingStudy, IPatient } from "../../../../../../types";
import { Dropdown, IChoiceGroupOption, IDropdownOption } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import ImagingStudyDetailsCard from "./ImagingStudyDetailsCard";
import { PropsWithContext, withAppContext } from "../../../shared/AppState";
import ImagingStudySelectionInput from "./inputs/ImagingStudySelectionInput";

export interface IImagingStudySelectionStepProps extends PropsWithContext {}

export interface IImagingStudySelectionStepState {
  selectedPatient?: IPatient;
  selectedStudy?: IImagingStudy;
}

export interface IExtendedChoiceGroupOption extends IChoiceGroupOption {
  endpoint: string;
}

class ImagingStudySelectionStep extends Component<
  IImagingStudySelectionStepProps,
  IImagingStudySelectionStepState
> {
  state: IImagingStudySelectionStepState = {};

  render() {
    return (
      <Row>
        <Col span={8}>
          <Dropdown
            label="Patient"
            placeholder="Select a patient"
            options={this._mapPatientsToDropdownOptions()}
            onChange={this._handlePatientDropdownChange}
            required={true}
          />

          <Divider />

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
          <ImagingStudyDetailsCard study={this.state.selectedStudy} />
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

  private _handlePatientDropdownChange = (_: any, option?: IDropdownOption) => {
    const { patients } = this.props.context!;

    const selectedPatientId = option!.key;
    this.setState({ selectedPatient: patients[selectedPatientId], selectedStudy: undefined });
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
