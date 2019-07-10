import React, { Component } from "react";
import { IPatient } from "../../../types";

import samplePatients from "../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../__tests__/samples/samplePatientsWithHolograms.json";
import {
  DatePicker,
  DayOfWeek,
  Dropdown,
  IDatePickerStrings,
  IStackProps,
  Stack,
  TextField
} from "office-ui-fabric-react";

const columnProps: Partial<IStackProps> = {
  tokens: { childrenGap: 15 },
  styles: { root: { width: 300 } }
};

const DayPickerStrings: IDatePickerStrings = {
  months: [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ],

  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],

  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],

  shortDays: ["S", "M", "T", "W", "T", "F", "S"],

  goToToday: "Go to today",
  prevMonthAriaLabel: "Go to previous month",
  nextMonthAriaLabel: "Go to next month",
  prevYearAriaLabel: "Go to previous year",
  nextYearAriaLabel: "Go to next year",
  closeButtonAriaLabel: "Close date picker"
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
              placeholder="Select an option"
              label="Patient"
              options={this._mapPatientsToDropdownOptions(this._allPatients)}
              required={true}
              styles={{ dropdown: { width: 300 } }}
            />

            <TextField label="Hologram title" required />

            <TextField label="Description" multiline autoAdjustHeight />
          </Stack>

          <Stack {...columnProps}>
            <TextField label="Body site" />

            <DatePicker
              strings={DayPickerStrings}
              label="Date of original encounter"
              ariaLabel="Date of original encounter"
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
