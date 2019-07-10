import React, { Component } from "react";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react/lib-commonjs/ChoiceGroup";
import ExtendedChoiceGroupLabel from "./ExtendedChoiceGroupLabel";
import { HologramCreationMode } from "../../../types";

const choiceGroupOptions: IChoiceGroupOption[] = [
  {
    key: HologramCreationMode.generateFromImagingStudy,
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
    key: HologramCreationMode.uploadExistingModel,
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

export interface IHologramCreationModeSelectionStepProps {
  handleModeChange: (creationMode: HologramCreationMode) => void;
}

class CreationModeSelectionStep extends Component<IHologramCreationModeSelectionStepProps> {
  render() {
    return (
      <ChoiceGroup
        options={choiceGroupOptions}
        defaultSelectedKey={HologramCreationMode.generateFromImagingStudy}
        onChange={this._handleChoiceGroupChange}
        label="Select the mode for creating a new hologram"
      />
    );
  }

  private _handleChoiceGroupChange = (_: any, option?: IChoiceGroupOption): void => {
    this.props.handleModeChange(option!.key as HologramCreationMode);
  };
}

export default CreationModeSelectionStep;
