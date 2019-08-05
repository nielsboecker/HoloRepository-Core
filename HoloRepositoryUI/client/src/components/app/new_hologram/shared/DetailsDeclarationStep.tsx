import React, { Component } from "react";
import {
  DatePicker,
  DayOfWeek,
  Dropdown,
  IStackProps,
  Stack,
  TextField
} from "office-ui-fabric-react";
import { PidToPatientsMap, PropsWithContext, withAppContext } from "../../../shared/AppState";

const columnProps: Partial<IStackProps> = {
  tokens: { childrenGap: 15 },
  styles: { root: { width: 300 } }
};

class DetailsDeclarationStep extends Component<PropsWithContext> {
  render() {
    return (
      <div>
        <Stack horizontal tokens={{ childrenGap: 50 }} styles={{ root: { width: 650 } }}>
          <Stack {...columnProps}>
            <Dropdown
              label="Corresponding patient"
              placeholder="Select a patient"
              options={this._mapPatientsToDropdownOptions(this.props.context!.patients)}
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
              label="Date of imaging"
              ariaLabel="Date of imaging"
              placeholder="Pick a date"
              firstDayOfWeek={DayOfWeek.Monday}
              maxDate={new Date()}
            />
          </Stack>
        </Stack>
      </div>
    );
  }

  private _mapPatientsToDropdownOptions = (patients: PidToPatientsMap) => {
    return Object.entries(patients).map(([pid, patient]) => ({
      key: pid,
      text: patient.name.full
    }));
  };
}

export default withAppContext(DetailsDeclarationStep);
