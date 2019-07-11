import React, { Component } from "react";

import samplePipelines from "../../../../__tests__/samples/samplePipelines.json";
import { IPipeline } from "../../../../types";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import { Col, Row } from "antd";
import PipelineSpecificationCard from "./PipelineSpecificationCard";

const pipelines = samplePipelines as IPipeline[];

const choiceGroupOptions: IChoiceGroupOption[] = pipelines.map(pipeline => ({
  key: pipeline.id,
  text: pipeline.name
}));

export interface IPipelineSelectionStepState {
  selectedPipeline?: IPipeline;
}

class PipelineSelectionStep extends Component<any, IPipelineSelectionStepState> {
  state = {
    selectedPipeline: undefined
  };

  render() {
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

  private _handleChoiceGroupChange = (_: any, option?: IChoiceGroupOption): void => {
    const selectedPipeline = pipelines.find(pipeline => pipeline.id === option!.key);
    this.setState({ selectedPipeline });
  };
}

export default PipelineSelectionStep;
