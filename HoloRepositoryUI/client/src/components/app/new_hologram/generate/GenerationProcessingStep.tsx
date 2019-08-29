import React, { Component } from "react";
import { Icon, MessageBar, Spinner } from "office-ui-fabric-react";
import { navigate } from "@reach/router";
import JobLogTerminal from "./JobLogTerminal";
import BackendServerService from "../../../../services/BackendServerService";
import { IHologramCreationRequest_Generate, IJobStateResponse } from "../../../../../../types";

const stateRefreshInterval = 2500;
const waitTimeAfterFinishBeforeRedirect = 3000;

export interface IGenerationProcessingStepProps {
  generateMetaData: () => IHologramCreationRequest_Generate | null;
  onError: () => void;
  onGenerationSuccess: () => void;
  onGenerationFailure: () => void;
}

export interface IGenerationProcessingStepState {
  jobId?: string;
  jobState?: string;
  message: string;
  finished: boolean;
  intervalHandle?: any;
}

class GenerationProcessingStep extends Component<
  IGenerationProcessingStepProps,
  IGenerationProcessingStepState
> {
  state = {
    jobId: undefined,
    finished: false,
    message: "Connecting...",
    jobState: "",
    intervalHandle: undefined
  };

  intervalId: any = undefined;

  render() {
    if (!this.state.finished) {
      return (
        <>
          <div style={{ marginBottom: "24px" }}>
            <MessageBar>
              The pipeline has received your data and started processing. The next steps may take a
              few moments, you don't have to stay on this page.
            </MessageBar>
          </div>

          <div>
            <Spinner label={this.state.message} style={{ marginBottom: "35px" }} />
          </div>

          {this.state.jobId && (
            // @ts-ignore because it looks to TS like state.jobId would always be undefined
            <JobLogTerminal jobId={this.state.jobId} jobState={this.state.jobState} />
          )}
        </>
      );
    } else {
      return (
        <div>
          <Icon iconName="Accept" />
          <strong>All done!</strong>
          <p>Your hologram is now stored in the HoloRepository.</p>
        </div>
      );
    }
  }

  private _handleSubmit_Generate = () => {
    // Note: This method should be in NewHologramPage. Due to a design flaw (the way the separate
    // pages are stored in the _steps variable), updates in the parent component do not propagate
    // to children. Future refactoring should clean this up; but it works for now.
    const metaData = this.props.generateMetaData();
    if (!metaData) {
      return this.props.onError();
    }
    BackendServerService.generateHologram(metaData)
      .then(jid => {
        console.log(`Starting job ${jid}`);
        this.setState({ jobId: jid });
      })
      .catch(() => this.props.onGenerationFailure());
  };

  updateJobState = () => {
    console.log("Update function called");

    // Note: Due to a bug in HoloPipelines, this will get a 404 after the job has been cleaned up
    // by garbage collection. When requests from UI have been issued before termination, but only
    // get through after, this happens. It won't break anything, just show "404 NOT FOUND" errors
    // in console. Can be ignored for now; the issue should rather be fixed in the HoloPipelines.
    if (this.state.jobId && !this.state.finished) {
      // @ts-ignore because it looks to TS like state.jobId would always be undefined
      BackendServerService.getJobStateById(this.state.jobId)
        .then((stateUpdate: IJobStateResponse) => {
          console.log("Received job state update:", stateUpdate);
          const jobState = stateUpdate.state;
          const duration = stateUpdate.age;
          if (jobState && duration) {
            const message = `${jobState} since ${duration.toFixed(2)} seconds...`;
            this.setState({
              message,
              jobState
            });

            if (jobState === "FINISHED") {
              this.handleJobFinished();
            }
          }
        });
    }
  };

  componentDidMount = () => {
    // Note: This is not ideal; using callback upon component render to start the upload
    this._handleSubmit_Generate();

    // Start interval to check for state updates
    this.intervalId = setInterval(() => this.updateJobState(), stateRefreshInterval);
  };

  componentWillUnmount() {
    // Fallback, this should already have been called by handleJobFinished
    clearInterval(this.intervalId);
  }

  handleJobFinished() {
    // Edge case: request which was already issued before the interval was stopped may
    // return with "FINISHED" afterwards, so ensure to only run this once
    if (!this.state.finished) {
      console.log("handleJobFinished is running");
      clearInterval(this.intervalId);

      // Set to finished to stop further updates and display "Finished" on the screen
      this.setState({ finished: true });

      // Call parent handler to trigger refreshing holograms data
      this.props.onGenerationSuccess();

      // After some seconds, redirect to holograms overview page
      setTimeout(() => {
        navigate("/app/holograms");
      }, waitTimeAfterFinishBeforeRedirect);
    }
  }
}

export default GenerationProcessingStep;
