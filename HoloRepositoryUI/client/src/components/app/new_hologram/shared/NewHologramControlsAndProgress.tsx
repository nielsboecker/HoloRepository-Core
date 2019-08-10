import React, { Component } from "react";
import { DefaultButton, PrimaryButton } from "office-ui-fabric-react";
import { Steps } from "antd";
import { IHologramCreationStep } from "../NewHologramPage";

const { Step } = Steps;

export interface INewHologramControlsAndProgressProps {
  current: number;
  steps: IHologramCreationStep[];
  currentStepIsValid: boolean;
  onGoToPrevious: () => void;
}

class NewHologramControlsAndProgress extends Component<INewHologramControlsAndProgressProps> {
  render() {
    const { current, steps, currentStepIsValid, onGoToPrevious } = this.props;

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
              <DefaultButton text="Previous" onClick={() => onGoToPrevious()} />
            </div>
          )}

          {current < steps.length - 1 && (
            // Note: Conceptually, redirection to the next step should happen here. However, for
            // some reason the button behaves strange when it has type="submit" and an onClick
            // listener (which would be needed to redirect to the next step). As a workaround,
            // the redirection is provided in the onSubmit callback in the parent component.
            <div style={{ float: "right" }}>
              <PrimaryButton text="Next" type="submit" disabled={!currentStepIsValid} />
            </div>
          )}
        </div>
      </>
    );
  }
}

export default NewHologramControlsAndProgress;
