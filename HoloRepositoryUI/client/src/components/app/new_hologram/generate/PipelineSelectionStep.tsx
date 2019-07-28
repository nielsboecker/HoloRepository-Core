import React, { Component } from "react";
import { IPipeline } from "../../../../../../HoloRepositoryUI-Types";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import { Col, Row } from "antd";
import PipelineSpecificationCard from "./PipelineSpecificationCard";
import { PropsWithContext, withAppContext } from "../../../shared/AppState";

export interface IPipelineSelectionStepState {
  selectedPipeline?: IPipeline;
}

class PipelineSelectionStep extends Component<PropsWithContext, IPipelineSelectionStepState> {
  state = {
    selectedPipeline: undefined
  };

  render() {
    const choiceGroupOptions: IChoiceGroupOption[] = this._mapPipelinesToChoiceGroupOptions();

    return (
      <Row>
        <Col span={8}>
          <ChoiceGroup
            label="Select a pipeline"
            required
            options={choiceGroupOptions}
            onChange={this._handleChoiceGroupChange}
          />
        </Col>

        <Col span={14} offset={2}>
          <PipelineSpecificationCard pipeline={this.state.selectedPipeline} />
        </Col>
      </Row>
    );
  }

  private _mapPipelinesToChoiceGroupOptions(): IChoiceGroupOption[] {
    const { pipelines } = this.props.context!;
    return pipelines.map(pipeline => ({
      key: pipeline.plid,
      text: pipeline.title
    }));
  }

  private _handleChoiceGroupChange = (_: any, option?: IChoiceGroupOption): void => {
    const { pipelines } = this.props.context!;
    const selectedPipeline = pipelines.find(pipeline => pipeline.plid === option!.key);
    this.setState({ selectedPipeline });
  };
}

export default withAppContext(PipelineSelectionStep);
