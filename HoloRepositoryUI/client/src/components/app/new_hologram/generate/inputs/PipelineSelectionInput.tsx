import React, { Component } from "react";
import { IPipeline } from "../../../../../../../types";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {
  pipelines: IPipeline[];
  onPipelineChange: (plid: string) => void;
}

class PipelineSelectionInput extends Component<Props> {
  _handleChange = (plid: string): void => {
    // Notify Formsy about new value
    this.props.setValue!(plid);

    // Update details panel in parent component
    this.props.onPipelineChange(plid);
  };

  render() {
    const choiceGroupOptions: IChoiceGroupOption[] = this._mapPipelinesToChoiceGroupOptions();

    return (
      <ChoiceGroup
        label="Select a pipeline"
        required
        options={choiceGroupOptions}
        onChange={this._handleChoiceGroupChange}
      />
    );
  }

  private _mapPipelinesToChoiceGroupOptions(): IChoiceGroupOption[] {
    return this.props.pipelines.map(pipeline => ({
      key: pipeline.plid,
      text: pipeline.title
    }));
  }

  private _handleChoiceGroupChange = (_: any, option?: IChoiceGroupOption): void => {
    this._handleChange(option!.key);
  };
}

export default withFormsy(PipelineSelectionInput);
