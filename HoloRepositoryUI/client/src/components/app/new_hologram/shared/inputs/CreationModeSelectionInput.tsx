import React, { Component } from "react";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import ExtendedChoiceGroupLabel from "./../ExtendedChoiceGroupLabel";
import { HologramCreationMode } from "../../../../../types";
import { withFormsy } from "formsy-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";

const choiceGroupOptions: IChoiceGroupOption[] = [
  {
    key: HologramCreationMode.GENERATE_FROM_IMAGING_STUDY,
    text: "Generate from an imaging study",
    onRenderLabel: () => (
      <ExtendedChoiceGroupLabel
        title="Generate from an imaging study"
        description="Choose an imaging study from a patient, such as a CT scan of the lung.
                This will then be used as input for a processing pipeline to generate a 3D model."
        iconName="Blur"
      />
    )
  } as IChoiceGroupOption,
  {
    key: HologramCreationMode.UPLOAD_EXISTING_MODEL,
    text: "Upload an existing 3D model",
    onRenderLabel: () => (
      <ExtendedChoiceGroupLabel
        title="Upload an existing 3D model"
        description="Choose an existing 3D model from your disk. It will be linked to a
                patient and uploaded directly."
        iconName="Upload"
      />
    )
  }
];

export interface IHologramCreationModeSelectionStepProps
  extends Partial<PassDownProps>,
    Partial<WrapperProps> {
  selected: HologramCreationMode;
}

class CreationModeSelectionStep extends Component<IHologramCreationModeSelectionStepProps> {
  _handleChange = (value: HologramCreationMode): void => {
    this.props.setValue!(value);
  };

  render() {
    return (
      <ChoiceGroup
        options={choiceGroupOptions}
        defaultSelectedKey={this.props.selected}
        onChange={this._handleChoiceGroupChange}
        label="Select the mode for creating a new hologram"
      />
    );
  }

  componentDidMount(): void {
    // Make Formsy aware of the default selected option
    this._handleChange(this.props.selected);
  }

  private _handleChoiceGroupChange = (_: any, option?: IChoiceGroupOption): void => {
    this._handleChange(option!.key as HologramCreationMode);
  };
}

export default withFormsy(CreationModeSelectionStep);
