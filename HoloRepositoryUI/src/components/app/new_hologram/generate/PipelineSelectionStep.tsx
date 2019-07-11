import React, { Component } from "react";

import samplePipelines from "../../../../__tests__/samples/samplePipelines.json";
import { IPipeline } from "../../../../types";
import { ChoiceGroup, IChoiceGroupOption } from "office-ui-fabric-react";
import ExtendedChoiceGroupLabel from "../shared/ExtendedChoiceGroupLabel";

const pipelines = samplePipelines as IPipeline[];

const choiceGroupOptions: IChoiceGroupOption[] = pipelines.map(pipeline => ({
  key: pipeline.id,
  text: pipeline.name,
  onRenderLabel: () => (
    <ExtendedChoiceGroupLabel
      title={pipeline.name}
      description={pipeline.description}
      iconName="Blur"
    />
  )
}));

class PipelineSelectionStep extends Component {
  render() {
    return (
      <div>
        <ChoiceGroup options={choiceGroupOptions} label="Select a pipeline" />
      </div>
    );
  }
}

export default PipelineSelectionStep;
