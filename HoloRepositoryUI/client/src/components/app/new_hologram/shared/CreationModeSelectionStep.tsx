import React, { Component } from "react";
import CreationModeSelectionInput from "./inputs/CreationModeSelectionInput";
import { HologramCreationMode } from "../../../../types";

export interface IHologramCreationModeSelectionStepProps {
  selected: HologramCreationMode;
}

class CreationModeSelectionStep extends Component<IHologramCreationModeSelectionStepProps> {
  render() {
    return (
      <CreationModeSelectionInput selected={this.props.selected} name="creationMode" required />
    );
  }
}

export default CreationModeSelectionStep;
