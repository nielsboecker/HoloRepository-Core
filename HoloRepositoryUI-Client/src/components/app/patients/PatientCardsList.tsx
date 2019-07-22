import React, { Component } from "react";
import {
  FocusZone,
  FocusZoneDirection,
  getId,
  Label,
  List,
  SearchBox,
  Toggle
} from "office-ui-fabric-react";
import { Col, Row } from "antd";
import { IPatient } from "../../../../../HoloRepositoryUI-Types";
import PatientCard from "./PatientCard";

import samplePatients from "../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../__tests__/samples/samplePatientsWithHolograms.json";
import FilterStatusMessageBar from "../core/FilterStatusMessageBar";

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
    const { patients = [], isShowWithHologramsOnly } = this.state;

    // Ensure that the ID is unique on the page.
    const filterNameId = getId("filterName");

    return (
      <>
        <FocusZone direction={FocusZoneDirection.vertical} defaultActiveElement=".nameFilter">
          <div className="Filters" style={{ marginBottom: "24px" }}>
            <Row>
              <Col span={12} style={{ padding: "0 24px" }}>
                <Label htmlFor={filterNameId}>Filter by name</Label>
                <SearchBox
                  id={filterNameId}
                  placeholder="Filter patients..."
                  onChange={this._handleNameFilterChanged}
                  iconProps={{ iconName: "Filter" }}
                />
              </Col>

              <Col span={12} style={{ padding: "0 24px" }}>
                <Toggle
                  label="Filter patients with holograms"
                  checked={isShowWithHologramsOnly}
                  onChange={this._handleShowWithHologramsOnlyToggleChange}
                  onText="Only patients with existing holograms"
                  offText="All patients"
                  style={{ margin: "0 30px 20px 0", maxWidth: "300px" }}
                />
              </Col>
            </Row>

            <FilterStatusMessageBar
              totalCount={this.allPatients.length}
              filteredCount={patients.length}
              itemEntityName="patient"
            />
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
