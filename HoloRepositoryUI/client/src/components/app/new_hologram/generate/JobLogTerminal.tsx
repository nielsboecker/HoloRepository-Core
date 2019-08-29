import React, { Component } from "react";
// @ts-ignore that this module has implicit any
import { LazyLog } from "react-lazylog";

export interface IJobLogTerminalProps {
  jobId: string;
  jobState: string;
}

export interface IJobLogTerminalState {
  lastJobState: string;
}

class JobLogTerminal extends Component<IJobLogTerminalProps, IJobLogTerminalState> {
  state = {
    lastJobState: ""
  };

  // TODO: go through server
  logEndpoint = `http://51.105.47.56/api/v1/jobs/${this.props.jobId}/log`;

  render() {
    return (
      <div>
        <LazyLog url={this.logEndpoint} height={250} />
      </div>
    );
  }

  componentWillReceiveProps(nextProps: Readonly<IJobLogTerminalProps>): void {
    // Note: This is a deprecated React hook, should be refactored to use more elegant solution
    if (nextProps.jobState !== this.state.lastJobState) {
      console.info(`New state: ${nextProps.jobState} => Updating logs`);
    }
  }
}

export default JobLogTerminal;
