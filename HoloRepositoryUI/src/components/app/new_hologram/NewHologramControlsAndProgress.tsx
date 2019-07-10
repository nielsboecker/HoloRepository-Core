import React, { Component } from "react";
import { Button, Steps } from "antd";
import { IHologramCreationStep } from "./NewHologramPage";

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
        <Steps current={current}>
          {steps.map(step => (
            <Step key={step.title} title={step.title} />
          ))}
        </Steps>

        <div className="steps-action" style={{ marginTop: "24px" }}>
          {current > 0 && (
            <div style={{ float: "left" }}>
              <Button style={{ marginLeft: 8 }} onClick={() => handlePrevious()}>
                Previous
              </Button>
            </div>
          )}

          {current < steps.length - 1 && (
            <div style={{ float: "right" }}>
              <Button type="primary" onClick={() => handleNext()}>
                Next
              </Button>
            </div>
          )}
        </div>
      </>
    );
  }
}

export default NewHologramControlsAndProgress;
