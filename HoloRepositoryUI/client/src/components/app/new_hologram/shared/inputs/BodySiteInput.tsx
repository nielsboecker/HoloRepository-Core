import React, { Component } from "react";
import { TextField } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {}

class BodySiteInput extends Component<Props> {
  _handleChange = (_: any, newValue?: string): void => {
    this.props.setValue!(newValue);
  };

  render() {
    return (
      <TextField
        label="Body site"
        placeholder="For example, 'Right kidney'"
        onChange={this._handleChange}
      />
    );
  }
}

export default withFormsy(BodySiteInput);
