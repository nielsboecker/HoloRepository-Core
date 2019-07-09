import React, { Component } from "react";
import { CommandBar, ICommandBarItemProps } from "office-ui-fabric-react/lib/CommandBar";

const buttons: ICommandBarItemProps[] = [
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
    disabled: true,
    onClick: () => console.log("Download")
  },

  {
    key: "delete",
    name: "Delete",
    iconProps: {
      iconName: "Delete"
    },
    disabled: true,
    onClick: () => console.log("Delete")
  }
];

class HologramsCommandBar extends Component {
  public render(): JSX.Element {
    return (
      <div>
        <CommandBar
          items={buttons}
          ariaLabel={"Use left and right arrow keys to navigate between commands"}
        />
      </div>
    );
  }
}

export default HologramsCommandBar;
