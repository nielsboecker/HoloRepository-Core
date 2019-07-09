import React, { Component } from "react";
import { MessageBar } from "office-ui-fabric-react";
// import { MessageBar } from "office-ui-fabric-react/lib/MessageBar";

export interface IFilterStatusMessageBarProps {
  totalCount: number;
  filteredCount: number;
  itemEntityName?: string;
}

class FilterStatusMessageBar extends Component<IFilterStatusMessageBarProps> {
  render() {
    const { totalCount, filteredCount, itemEntityName = "item" } = this.props;

    return (
      <>
        {totalCount !== filteredCount && (
          <MessageBar>{`Showing ${filteredCount} of ${totalCount} ${itemEntityName}s.`}</MessageBar>
        )}
      </>
    );
  }
}

export default FilterStatusMessageBar;
