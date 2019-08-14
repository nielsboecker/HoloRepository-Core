import React, { Component } from "react";
import { TextField } from "office-ui-fabric-react";
import { withFormsy } from "formsy-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {}

class TitleInput extends Component<Props> {
  _handleChange = (_: any, newValue?: string): void => {
    this.props.setValue!(newValue);
  };

  render() {
    const { isRequired, isValid } = this.props;

    return (
      <TextField
        label="Hologram title"
        placeholder={`For example, "Renal tumour"`}
        onChange={this._handleChange}
        required={isRequired}
        errorMessage={isValid ? undefined : "Provide valid title for hologram"}
      />
    );
  }
}

export default withFormsy(TitleInput);
