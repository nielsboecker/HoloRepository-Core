import React, { Component } from "react";
import { IPipeline } from "../../../../../../types";
import { Col, Row } from "antd";
import PipelineSpecificationCard from "./PipelineSpecificationCard";
import { PropsWithContext, withAppContext } from "../../../shared/AppState";
import PipelineSelectionInput from "./inputs/PipelineSelectionInput";

export interface IPipelineSelectionStepState {
  selectedPipeline?: IPipeline;
}

class PipelineSelectionStep extends Component<PropsWithContext, IPipelineSelectionStepState> {
  state = {
    selectedPipeline: undefined
  };

  render() {
    const { pipelines } = this.props.context!;

    return (
      <Row>
        <Col span={8}>
          <PipelineSelectionInput
            name="plid"
            pipelines={pipelines}
            onPipelineChange={this._handlePipelineChange}
            required
          />
        </Col>

        <Col span={14} offset={2}>
          <PipelineSpecificationCard pipeline={this.state.selectedPipeline} />
        </Col>
      </Row>
    );
  }

  private _handlePipelineChange = (plid: string): void => {
    const { pipelines } = this.props.context!;
    const selectedPipeline = pipelines.find(pipeline => pipeline.plid === plid);
    this.setState({ selectedPipeline });
  };
}

export default withAppContext(PipelineSelectionStep);
