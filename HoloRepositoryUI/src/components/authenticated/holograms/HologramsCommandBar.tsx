import React, { Component } from "react";
import { CommandBar, ICommandBarItemProps } from "office-ui-fabric-react/lib/CommandBar";
import { Selection } from "office-ui-fabric-react/lib-commonjs/DetailsList";

export interface IHologramsCommandBarProps {
  selection: Selection;
}

class HologramsCommandBar extends Component<IHologramsCommandBarProps> {
  public render(): JSX.Element {
    const _items: ICommandBarItemProps[] = [
      {
        key: "newItem",
        name: "New",
        cacheKey: "myCacheKey", // changing this key will invalidate this items cache
        iconProps: {
          iconName: "Add"
        },
        ariaLabel: "New",
        subMenuProps: {
          items: [
            {
              key: "fromImagingStudy",
              name: "Generate from imaging study",
              iconProps: {
                iconName: "Blur"
              }
            },
            {
              key: "uploadExisting",
              name: "Upload existing 3D model",
              iconProps: {
                iconName: "Upload"
              }
            }
          ]
        }
      },

      {
        key: "download",
        name: "Download",
        iconProps: {
          iconName: "Download"
        },
        disabled: this.props.selection.count < 1,
        onClick: () => console.log("Download")
      },

      {
        key: "delete",
        name: "Delete",
        iconProps: {
          iconName: "Delete"
        },
        disabled: this.props.selection.count < 1,
        onClick: () => console.log("Delete")
      }
    ];

    return (
      <div>
        <CommandBar
          items={_items}
          ariaLabel={"Use left and right arrow keys to navigate between commands"}
        />
      </div>
    );
  }
}

export default HologramsCommandBar;
