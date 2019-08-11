import React, { Component } from "react";
import { TextField } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {}

class DescriptionInput extends Component<Props> {
  _handleChange = (_: any, newValue?: string): void => {
    this.props.setValue!(newValue);
  };

  render() {
    return (
      <TextField
        onChange={this._handleChange}
        label="Description"
        placeholder="Add a short description"
        multiline
        autoAdjustHeight
      />
    );
  }
}

export default withFormsy(DescriptionInput);
