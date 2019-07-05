import React, { Component } from "react";
import { FocusZone, FocusZoneDirection } from "office-ui-fabric-react/lib/FocusZone";
import { TextField } from "office-ui-fabric-react/lib/TextField";
import { Toggle } from "office-ui-fabric-react/lib-commonjs/Toggle";
import { MessageBar } from "office-ui-fabric-react/lib/MessageBar";
import { List } from "office-ui-fabric-react/lib/List";
import { Row, Col } from "antd";
import { IPatient } from "../../../types";
import PatientCard from "./PatientCard";

import samplePatients from "../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../__tests__/samples/samplePatientsWithHolograms.json";

export interface IPatientCardsListState {
  filterPatientNameText?: string;
  patients?: IPatient[];
}

export default class PatientCardsList extends Component<any, IPatientCardsListState> {
  allPatients = [...samplePatients, ...samplePatientsWithHolograms] as IPatient[];

  state = {
    filterPatientNameText: "",
    isShowWithHologramsOnly: false,
    patients: this.allPatients.sort((a, b) => a.name.full.localeCompare(b.name.full))
  };

  render(): JSX.Element {
    const { patients = [] } = this.state;

    return (
      <>
        <FocusZone direction={FocusZoneDirection.vertical} defaultActiveElement=".nameFilter">
          <h2>Search and filter</h2>

          <div className="Filters" style={{ marginBottom: "24px" }}>
            <Row>
              <Col span={12} style={{ padding: "0 24px" }}>
                <TextField label="Filter by name" onChange={this._onFilterChanged} />
              </Col>

              <Col span={12} style={{ padding: "0 24px" }}>
                <Toggle
                  label="Filter patients holograms"
                  checked={this.state.isShowWithHologramsOnly}
                  onChange={this._handleShowWithHologramsOnlyToggleChange}
                  onText="Showing only patients with existing holograms"
                  offText="Showing all patients"
                  style={{ margin: "0 30px 20px 0", maxWidth: "300px" }}
                />
              </Col>
            </Row>

            {this.state.patients != this.allPatients && (
              <MessageBar>
                {`Showing ${patients.length} of ${this.allPatients.length} patients.`}
              </MessageBar>
            )}
          </div>
        </FocusZone>

        <FocusZone direction={FocusZoneDirection.vertical}>
          <List items={patients} onRenderCell={this._onRenderCell} />
        </FocusZone>
      </>
    );
  }

  private _onFilterChanged = (_: any = null, text: string = ""): void => {
    this.setState({
      filterPatientNameText: text,
      patients: text
        ? this.allPatients.filter(
            patient => patient.name.full.toLowerCase().indexOf(text.toLowerCase()) >= 0
          )
        : this.allPatients
    });
  };

  private _onRenderCell = (patient: IPatient | undefined): JSX.Element => {
    return patient ? <PatientCard patient={patient} /> : <div />;
  };

  private _handleShowWithHologramsOnlyToggleChange = () => {
    this.state.isShowWithHologramsOnly = !this.state.isShowWithHologramsOnly;
    this.setState({
      patients: this.state.isShowWithHologramsOnly
        ? this.allPatients.filter(patient => patient.holograms && patient.holograms.length > 0)
        : this.allPatients
    });
  };
}
