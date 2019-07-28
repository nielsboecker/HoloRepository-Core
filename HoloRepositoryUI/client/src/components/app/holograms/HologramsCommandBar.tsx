import React, { Component } from "react";
import { CommandBar, ICommandBarItemProps, Selection } from "office-ui-fabric-react";
import { navigate } from "@reach/router";
import { HologramCreationMode } from "../../../types";
import { PropsWithContext, withAppContext } from "../../shared/AppState";

export interface IHologramsCommandBarProps extends PropsWithContext {
  selection: Selection;
}

class HologramsCommandBar extends Component<IHologramsCommandBarProps> {
  public render(): JSX.Element {
    const { handleDeleteHolograms, handleDownloadHolograms } = this.props.context!;
    const { selection } = this.props;

    const _selectionItems: ICommandBarItemProps[] = [
      {
        key: "preview",
        name: "Preview",
        iconProps: {
          iconName: "View"
        },
        disabled: selection.getSelectedCount() !== 1,
        onClick: () => alert("3D model preview not implemented yet")
      },

      {
        key: "download",
        name: "Download",
        iconProps: {
          iconName: "Download"
        },
        disabled: selection.getSelectedCount() < 1,
        onClick: () =>
          handleDownloadHolograms(this.props.selection.getSelection().map(item => item.key))
      },

      {
        key: "delete",
        name: "Delete",
        iconProps: {
          iconName: "Delete"
        },
        disabled: selection.getSelectedCount() < 1,
        onClick: () =>
          handleDeleteHolograms(this.props.selection.getSelection().map(item => item.key))
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
              name: "Generate from an imaging study",
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

export default withAppContext(HologramsCommandBar, false);
