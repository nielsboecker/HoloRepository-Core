import React, { Component } from "react";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {
  imagingStudyOptions: IChoiceGroupOption[];
  onImagingStudyChange: (isid: string) => void;
}

class ImagingStudySelectionInput extends Component<Props> {
  _handleChange = (imagingStudyId: string, imagingStudyEndpoint: string): void => {
    // Notify Formsy about new value
    this.props.setValue!(imagingStudyEndpoint);

    // Update details panel in parent component
    this.props.onImagingStudyChange(imagingStudyId);
  };

  render() {
    return (
      <ChoiceGroup
        label="Select an imaging study"
        required
        options={this.props.imagingStudyOptions}
        onChange={this._handleImagingStudyChange}
      />
    );
  }

  private _handleImagingStudyChange = (_: any, option?: any) => {
    const imagingStudyId = option!.key;
    const imagingStudyEndpoint = option!.endpoint;
    this._handleChange(imagingStudyId, imagingStudyEndpoint);
  };
}

export default withFormsy(ImagingStudySelectionInput);
