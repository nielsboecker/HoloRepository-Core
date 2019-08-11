import React, { Component } from "react";
import { DatePicker, DayOfWeek } from "office-ui-fabric-react";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { withFormsy } from "formsy-react";

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {}

class DateOfImagingInput extends Component<Props> {
  _handleChange = (date: Date | null | undefined): void => {
    date && this.props.setValue!(date.toISOString());
  };

  render() {
    return (
      <DatePicker
        onSelectDate={this._handleChange}
        label="Date of imaging"
        ariaLabel="Date of imaging"
        placeholder="Pick a date"
        firstDayOfWeek={DayOfWeek.Monday}
        maxDate={new Date()}
      />
    );
  }
}

export default withFormsy(DateOfImagingInput);
