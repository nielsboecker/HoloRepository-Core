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
import FilterStatusMessageBar from "../core/FilterStatusMessageBar";
import { PidToPatientsMap, PropsWithContext, withAppContext } from "../../shared/AppState";

export interface IPatientCardsListState {
  filterPatientNameText?: string;
  isShowWithHologramsOnly: boolean;
}

class PatientCardsList extends Component<PropsWithContext, IPatientCardsListState> {
  state: IPatientCardsListState = {
    filterPatientNameText: "",
    isShowWithHologramsOnly: false
  };

  render(): JSX.Element {
    const { isShowWithHologramsOnly } = this.state;

    const { allPatients, displayedPatients } = this._updateDisplayedPatients();

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
              totalCount={Object.keys(allPatients).length}
              filteredCount={Object.keys(displayedPatients).length}
              itemEntityName="patient"
            />
          </div>
        </FocusZone>

        <FocusZone direction={FocusZoneDirection.vertical}>
          <List items={Object.values(displayedPatients)} onRenderCell={this._onRenderCell} />
        </FocusZone>
      </>
    );
  }

  private _updateDisplayedPatients() {
    const { patients: allPatients } = this.props.context!;

    const displayedPatients: PidToPatientsMap = { ...allPatients };
    for (const pid in allPatients) {
      const patient = allPatients[pid];

      if (this._filterItem_noHolograms(patient) || this._filterItem_patientName(patient)) {
        delete displayedPatients[pid];
      }
    }
    return { allPatients, displayedPatients };
  }

  private _filterItem_noHolograms(patient: IPatient): boolean {
    return (
      this.state.isShowWithHologramsOnly && (!patient.holograms || patient.holograms.length === 0)
    );
  }

  private _filterItem_patientName(patient: IPatient): boolean {
    return (
      this.state.filterPatientNameText !== undefined &&
      this.state.filterPatientNameText !== "" &&
      patient.name.full.toLowerCase().indexOf(this.state.filterPatientNameText.toLowerCase()) < 0
    );
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

export default withAppContext(PatientCardsList);
