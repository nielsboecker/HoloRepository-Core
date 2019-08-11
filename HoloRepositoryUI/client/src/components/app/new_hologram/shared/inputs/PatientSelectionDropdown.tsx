import React, { Component } from "react";
import { withFormsy } from "formsy-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { Dropdown, IDropdownOption } from "office-ui-fabric-react";
import { PropsWithContext, withAppContext } from "../../../../shared/AppState";

export interface PatientSelectionDropdownProps
  extends PropsWithContext,
    Partial<PassDownProps>,
    Partial<WrapperProps> {
  patients: IDropdownOption[];
}
class PatientSelectionDropdown extends Component<PatientSelectionDropdownProps> {
  _handleChange = (pid: string): void => {
    this.props.setValue!(pid);
  };

  _handleOptionChange = (_: any, option?: IDropdownOption): void => {
    this._handleChange(option!.key as string);
  };

  render() {
    const { patients, isRequired, isValid } = this.props;
    const { selectedPatientId } = this.props.context!;

    return (
      <Dropdown
        onChange={this._handleOptionChange}
        label="Corresponding patient"
        placeholder="Select a patient"
        options={patients}
        required={isRequired}
        defaultSelectedKey={selectedPatientId}
        errorMessage={isValid ? undefined : "Select a patient"}
        styles={{ dropdown: { width: 300 } }}
      />
    );
  }

  componentDidMount(): void {
    // Make Formsy aware of the default selected option
    const { selectedPatientId } = this.props.context!;
    if (selectedPatientId) {
      this._handleChange(selectedPatientId);
    }
  }
}

export default withAppContext(withFormsy(PatientSelectionDropdown));
