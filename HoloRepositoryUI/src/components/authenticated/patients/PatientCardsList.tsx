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
  isShowWithHologramsOnly: boolean;
  patients?: IPatient[];
}

export default class PatientCardsList extends Component<any, IPatientCardsListState> {
  allPatients = [...samplePatients, ...samplePatientsWithHolograms].sort((a, b) =>
    a.name.full.localeCompare(b.name.full)
  ) as IPatient[];

  state: IPatientCardsListState = {
    filterPatientNameText: "",
    isShowWithHologramsOnly: false,
    patients: this.allPatients
  };

  render(): JSX.Element {
    const { patients = [] } = this.state;

    return (
      <>
        <FocusZone direction={FocusZoneDirection.vertical} defaultActiveElement=".nameFilter">
          <div className="Filters" style={{ marginBottom: "24px" }}>
            <Row>
              <Col span={12} style={{ padding: "0 24px" }}>
                <TextField label="Filter by name" onChange={this._handleNameFilterChanged} />
              </Col>

              <Col span={12} style={{ padding: "0 24px" }}>
                <Toggle
                  label="Only patients with holograms"
                  checked={this.state.isShowWithHologramsOnly}
                  onChange={this._handleShowWithHologramsOnlyToggleChange}
                  onText="Showing only patients with existing holograms"
                  offText="Showing all patients"
                  style={{ margin: "0 30px 20px 0", maxWidth: "300px" }}
                />
              </Col>
            </Row>

            {patients.length !== this.allPatients.length && (
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

  componentDidUpdate(prevProps: Readonly<any>, prevState: Readonly<IPatientCardsListState>): void {
    if (
      prevState.filterPatientNameText !== this.state.filterPatientNameText ||
      prevState.isShowWithHologramsOnly !== this.state.isShowWithHologramsOnly
    ) {
      let patients = this.allPatients.slice();
      if (this.state.filterPatientNameText) {
        patients = patients.filter(
          patient =>
            patient.name.full
              .toLowerCase()
              .indexOf(this.state.filterPatientNameText!.toLowerCase()) >= 0
        );
      }

      if (this.state.isShowWithHologramsOnly) {
        patients = patients.filter(patient => patient.holograms && patient.holograms.length > 0);
      }

      this.setState({ patients });
    }
  }

  private _onRenderCell = (patient: IPatient | undefined): JSX.Element => {
    return <PatientCard patient={patient!} />;
  };

  private _handleNameFilterChanged = (_: any = null, text: string = ""): void => {
    this.setState({
      filterPatientNameText: text
    });
  };

  private _handleShowWithHologramsOnlyToggleChange = () => {
    this.setState(state => ({
      isShowWithHologramsOnly: !state.isShowWithHologramsOnly
    }));
  };
}
