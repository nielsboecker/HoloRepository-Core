import React, { Component } from "react";

export interface IJobLogTerminalProps {
  jobId: string;
  jobState: string;
}

export interface IJobLogTerminalState {
  lastJobState: string;
  log: string;
}

class JobLogTerminal extends Component<IJobLogTerminalProps, IJobLogTerminalState> {
  state = {
    lastJobState: "",
    log: "..."
  };

  // TODO: go through server
  jobLogEndpoint = `http://51.105.47.56/api/v1/jobs/${this.props.jobId}/log`;

  render() {
    return (
      <div
        style={{
          height: "250px",
          padding: "20px",
          overflowY: "scroll",
          backgroundColor: "#333",
          color: "#FFB81C",
          fontSize: "small"
        }}
      >
        <pre style={{ overflow: "initial" }}>{this.state.log}</pre>
      </div>
    );
  }

  componentWillReceiveProps(nextProps: Readonly<IJobLogTerminalProps>): void {
    // Note: This is a deprecated React hook, should be refactored to use more elegant solution
    if (nextProps.jobState !== this.state.lastJobState) {
      console.info(`New state: ${nextProps.jobState} => Updating logs`);
      fetch(this.jobLogEndpoint)
        .then(response => response.text())
        .then(log => this.setState({ log }));
    }
  }
}

export default JobLogTerminal;
