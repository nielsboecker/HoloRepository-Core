import React, { Component } from "react";
import { CommandBar, ICommandBarItemProps, Selection } from "office-ui-fabric-react";
import { navigate } from "@reach/router";
import { HologramCreationMode } from "../../../types";

export interface IHologramsCommandBarProps {
  selection: Selection;
}

class HologramsCommandBar extends Component<IHologramsCommandBarProps> {
  public render(): JSX.Element {
    const _selectionItems: ICommandBarItemProps[] = [
      {
        key: "preview",
        name: "Preview",
        iconProps: {
          iconName: "View"
        },
        disabled: this.props.selection.count < 1,
        onClick: () => console.log("View")
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

    const _createItem: ICommandBarItemProps[] = [
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
              name: "Generate from an imaging studyy",
              iconProps: {
                iconName: "Blur"
              },
              onClick: () =>
                navigate("/app/holograms/new", {
                  state: { mode: HologramCreationMode.generateFromImagingStudy }
                })
            },
            {
              key: "uploadExisting",
              name: "Upload an existing 3D model",
              iconProps: {
                iconName: "Upload"
              },
              onClick: () =>
                navigate("/app/holograms/new", {
                  state: { mode: HologramCreationMode.uploadExistingModel }
                })
            }
          ]
        }
      }
    ];

    return (
      <div>
        <CommandBar
          items={_selectionItems}
          farItems={_createItem}
          ariaLabel={"Use left and right arrow keys to navigate between commands"}
        />
      </div>
    );
  }
}

export default HologramsCommandBar;
