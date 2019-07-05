import React, { Component } from "react";
import samplePatients from "../../../__tests__/samples/samplePatients.json";
import { IPatient } from "../../../types";
import { getRTL } from "office-ui-fabric-react/lib/Utilities";
import {
  FocusZone,
  FocusZoneDirection
} from "office-ui-fabric-react/lib/FocusZone";
import { TextField } from "office-ui-fabric-react/lib/TextField";
import { Image, ImageFit } from "office-ui-fabric-react/lib/Image";
import { Icon } from "office-ui-fabric-react/lib/Icon";
import { List } from "office-ui-fabric-react/lib/List";
import PatientCard from "./PatientCard";

// export interface IPatientCardsListProps {
//   items: PatientCard[];
// }

export interface IPatientCardsListState {
  filterText?: string;
  patients?: IPatient[];
}

export default class PatientCardsList extends Component<
  any,
  IPatientCardsListState
> {
  allPatients = samplePatients as IPatient[];
  state = {
    filterText: "",
    patients: this.allPatients
  };

  render(): JSX.Element {
    const { patients = [] } = this.state;
    const resultCountText =
      patients.length === this.allPatients.length
        ? ""
        : ` (${patients.length} of ${this.allPatients.length} patients shown)`;

    return (
      <FocusZone direction={FocusZoneDirection.vertical}>
        <div className="Filters" style={{ marginBottom: "24px" }}>
          <TextField
            label={"Filter by name" + resultCountText}
            onChange={this._onFilterChanged}
          />
        </div>
        <List items={patients} onRenderCell={this._onRenderCell} />
      </FocusZone>
    );
  }

  private _onFilterChanged = (_: any = null, text: string = ""): void => {
    this.setState({
      filterText: text,
      patients: text
        ? this.allPatients.filter(
            patient =>
              patient.name.full.toLowerCase().indexOf(text.toLowerCase()) >= 0
          )
        : this.allPatients
    });
  };

  private _onRenderCell = (patient: IPatient | undefined): JSX.Element => {
    return patient ? <PatientCard patient={patient} /> : <div>No</div>;
  };
}
