import React, { Component } from "react";
import { withFormsy } from "formsy-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { Dropdown, IDropdownOption } from "office-ui-fabric-react";

export interface PatientSelectionDropdownProps
  extends Partial<PassDownProps>,
    Partial<WrapperProps> {
  patients: any[];
}
class PatientSelectionDropdown extends Component<PatientSelectionDropdownProps> {
  _handleOptionChange = (_: any, option?: IDropdownOption): void => {
    this.props.setValue!(option!.key);
  };

  render() {
    const { patients, isRequired, isValid } = this.props;

    return (
      <Dropdown
        onChange={this._handleOptionChange}
        label="Corresponding patient"
        placeholder="Select a patient"
        options={patients}
        required={isRequired}
        errorMessage={isValid ? undefined : "Select a patient"}
        styles={{ dropdown: { width: 300 } }}
      />
    );
  }
}

export default withFormsy(PatientSelectionDropdown);
