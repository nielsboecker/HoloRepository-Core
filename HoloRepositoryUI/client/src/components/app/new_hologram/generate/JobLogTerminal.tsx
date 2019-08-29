import React, { Component } from "react";
// @ts-ignore that this module has implicit any
import { LazyLog } from "react-lazylog";

export interface IJobLogTerminalProps {
  jid: string;
}

class JobLogTerminal extends Component<IJobLogTerminalProps> {
  // TODO: go through server
  logEndpoint = `http://51.105.47.56/api/v1/jobs/${this.props.jid}/log`;

  render() {
    return (
      <div>
        <LazyLog url={this.logEndpoint} height={200} />
      </div>
    );
  }
}

export default JobLogTerminal;
