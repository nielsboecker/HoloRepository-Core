import React, { Component } from "react";
import { Dropdown, IDropdownOption } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";
import { PropsWithContext, withAppContext } from "../../../../shared/AppState";

interface Props extends PropsWithContext, Partial<PassDownProps>, Partial<WrapperProps> {
  patientOptions: IDropdownOption[];
  onPatientChange: (pid: string) => void;
}

class PatientForImagingStudySelectionInput extends Component<Props> {
  _handleChange = (pid: string): void => {
    // Notify Formsy about new value
    this.props.setValue!(pid);

    // Update details panel in parent component
    this.props.onPatientChange(pid);

    // Adjust global app state
    this.props.context!.handleSelectedPatientIdChange(pid);
  };

  render() {
    const { selectedPatientId } = this.props.context!;

    return (
      <Dropdown
        label="Patient"
        placeholder="Select a patient"
        options={this.props.patientOptions}
        onChange={this._handlePatientDropdownChange}
        defaultSelectedKey={selectedPatientId}
        required={this.props.isRequired}
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

  private _handlePatientDropdownChange = (_: any, option?: IDropdownOption) => {
    this._handleChange(option!.key as string);
  };
}

export default withAppContext(withFormsy(PatientForImagingStudySelectionInput));
