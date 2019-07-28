import React, { Component } from "react";
import { DefaultButton, PrimaryButton } from "office-ui-fabric-react";
import { Steps } from "antd";
import { IHologramCreationStep } from "../NewHologramPage";

const { Step } = Steps;

export interface INewHologramControlsAndProgressProps {
  current: number;
  steps: IHologramCreationStep[];
  handlePrevious: () => void;
  handleNext: () => void;
}

class NewHologramControlsAndProgress extends Component<INewHologramControlsAndProgressProps> {
  render() {
    const { current, steps, handlePrevious, handleNext } = this.props;

    return (
      <>
        <Steps current={current} progressDot>
          {steps.map(step => (
            <Step key={step.title} title={step.title} />
          ))}
        </Steps>

        <div className="steps-action" style={{ marginTop: "24px" }}>
          {current > 0 && (
            <div style={{ float: "left" }}>
              <DefaultButton text="Previous" onClick={() => handlePrevious()} />
            </div>
          )}

          {current < steps.length - 1 && (
            <div style={{ float: "right" }}>
              <PrimaryButton text="Next" onClick={() => handleNext()} />
            </div>
          )}
        </div>
      </>
    );
  }
}

export default NewHologramControlsAndProgress;
