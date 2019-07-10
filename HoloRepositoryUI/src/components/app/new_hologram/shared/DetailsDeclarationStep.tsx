import React, { Component } from "react";
import { IPatient } from "../../../../types";

import samplePatients from "../../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../../__tests__/samples/samplePatientsWithHolograms.json";
import {
  DatePicker,
  DayOfWeek,
  Dropdown,
  IStackProps,
  Stack,
  TextField
} from "office-ui-fabric-react";

const columnProps: Partial<IStackProps> = {
  tokens: { childrenGap: 15 },
  styles: { root: { width: 300 } }
};

class DetailsDeclarationStep extends Component {
  private _allPatients = [...samplePatients, ...samplePatientsWithHolograms].sort((a, b) =>
    a.name.full.localeCompare(b.name.full)
  ) as IPatient[];

  render() {
    return (
      <div>
        <Stack horizontal tokens={{ childrenGap: 50 }} styles={{ root: { width: 650 } }}>
          <Stack {...columnProps}>
            <Dropdown
              label="Corresponding patient"
              placeholder="Select a patient"
              options={this._mapPatientsToDropdownOptions(this._allPatients)}
              required={true}
              styles={{ dropdown: { width: 300 } }}
            />

            <TextField
              label="Hologram title"
              placeholder={`For example, "Renal tumour"`}
              required
            />

            <TextField
              label="Description"
              placeholder={"Add a short description"}
              multiline
              autoAdjustHeight
            />
          </Stack>

          <Stack {...columnProps}>
            <TextField label="Body site" placeholder={`For example, "Right kidney"`} />

            <DatePicker
              label="Date of original encounter"
              ariaLabel="Date of original encounter"
              placeholder="Pick a date"
              firstDayOfWeek={DayOfWeek.Monday}
              maxDate={new Date()}
            />
          </Stack>
        </Stack>
      </div>
    );
  }

  private _mapPatientsToDropdownOptions = (patients: IPatient[]) => {
    return patients.map(patient => ({ key: patient.id, text: patient.name.full }));
  };
}

export default DetailsDeclarationStep;
