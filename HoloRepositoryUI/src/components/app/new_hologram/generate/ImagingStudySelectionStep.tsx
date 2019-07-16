import React, { Component } from "react";
import { IImagingStudySeries, IPatient } from "../../../../types";
import { ChoiceGroup, Dropdown, IChoiceGroupOption, IDropdownOption } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import ImagingStudyDetailsCard from "./ImagingStudyDetailsCard";

import samplePatients from "../../../../__tests__/samples/samplePatients.json";
import samplePatientsWithImagingStudySeries from "../../../../__tests__/samples/samplePatientsWithImagingStudySeries.json";

const allPatients = [...samplePatients, ...samplePatientsWithImagingStudySeries].sort((a, b) =>
  a.name.full.localeCompare(b.name.full)
) as IPatient[];

export interface IImagingStudySelectionStepState {
  selectedPatient?: IPatient;
  selectedStudy?: IImagingStudySeries;
}

class ImagingStudySelectionStep extends Component<any, IImagingStudySelectionStepState> {
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
          this.state.selectedPatient.imagingStudySeries &&
          this.state.selectedPatient.imagingStudySeries.length >= 1 ? (
            <ChoiceGroup
              label="Select an imaging study series"
              required
              options={this._getImagingStudySeriesOptions()}
              onChange={this._handleImagingStudySeriesChange}
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
    return allPatients.map(patient => ({
      key: patient.pid,
      text: `${patient.name.full} (${ImagingStudySelectionStep._getNumberOfSeries(
        patient
      )} series)`,
      disabled: !patient.imagingStudySeries || patient.imagingStudySeries.length === 0
    }));
  };

  private _handlePatientDropdownChange = (_: any, option?: IDropdownOption) => {
    const selectedPatientId = option!.key;
    const selectedPatient = allPatients.find(patient => patient.pid === selectedPatientId);
    if (selectedPatient) {
      this.setState({ selectedPatient, selectedStudy: undefined });
    }
  };

  private _handleImagingStudySeriesChange = (_: any, option?: IChoiceGroupOption) => {
    if (!this.state.selectedPatient || !this.state.selectedPatient.imagingStudySeries) {
      return;
    }
    const selectedStudyId = option!.key;
    const selectedStudy = this.state.selectedPatient.imagingStudySeries.find(
      series => series.issid === selectedStudyId
    );
    if (selectedStudy) {
      this.setState({ selectedStudy });
    }
  };

  private _getImagingStudySeriesOptions = (): IChoiceGroupOption[] => {
    if (!this.state.selectedPatient || !this.state.selectedPatient.imagingStudySeries) {
      return [];
    }
    return this.state.selectedPatient.imagingStudySeries.map((series, index) => ({
      key: series.issid,
      text: `Imaging study ${index + 1} (${series.numberOfInstances} instances)`
    }));
  };

  private static _getNumberOfSeries(patient: IPatient) {
    return patient.imagingStudySeries ? patient.imagingStudySeries.length : 0;
  }
}

export default ImagingStudySelectionStep;
