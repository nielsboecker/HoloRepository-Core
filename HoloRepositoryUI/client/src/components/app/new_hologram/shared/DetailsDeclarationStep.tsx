import React, { Component } from "react";
import { IStackProps, Stack } from "office-ui-fabric-react";
import { PidToPatientsMap, PropsWithContext, withAppContext } from "../../../shared/AppState";
import PatientSelectionInput from "./inputs/PatientSelectionInput";
import HologramTitleInput from "./inputs/TitleInput";
import DescriptionInput from "./inputs/DescriptionInput";
import BodySiteInput from "./inputs/BodySiteInput";
import DateOfImagingInput from "./inputs/DateOfImagingInput";

const columnProps: Partial<IStackProps> = {
  tokens: { childrenGap: 15 },
  styles: { root: { width: 300 } }
};

export interface IDetailsDeclarationStepProps extends PropsWithContext {
  enablePatientSelection: boolean;
}

class DetailsDeclarationStep extends Component<IDetailsDeclarationStepProps> {
  render() {
    return (
      <div>
        <Stack horizontal tokens={{ childrenGap: 50 }} styles={{ root: { width: 650 } }}>
          <Stack {...columnProps}>
            <PatientSelectionInput
              name="patient"
              patients={this._mapPatientsToDropdownOptions(this.props.context!.patients)}
              disabled={!this.props.enablePatientSelection}
              required
            />

            <HologramTitleInput name="title" required />

            <DescriptionInput name="description" />
          </Stack>

          <Stack {...columnProps}>
            <BodySiteInput name="bodySite" />

            <DateOfImagingInput name="dateOfImaging" />
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
