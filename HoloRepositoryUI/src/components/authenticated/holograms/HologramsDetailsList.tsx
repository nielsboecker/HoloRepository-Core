import * as React from "react";
import { TextField } from "office-ui-fabric-react/lib-commonjs/TextField";
import { Toggle } from "office-ui-fabric-react/lib-commonjs/Toggle";
import { Fabric } from "office-ui-fabric-react/lib-commonjs/Fabric";
import {
  DetailsList,
  DetailsListLayoutMode,
  Selection,
  SelectionMode,
  IColumn
} from "office-ui-fabric-react/lib-commonjs/DetailsList";
import { mergeStyleSets } from "office-ui-fabric-react/lib-commonjs/Styling";
import sampleHolograms from "../../../__tests__/samples/sampleHolograms.json";
import { IHologram, IPractitioner, UNKNOWN_PERSON_NAME } from "../../../types";

// TODO move
import { initializeIcons } from "@uifabric/icons";
import { Icon } from "office-ui-fabric-react/lib-commonjs/Icon";
import samplePractitioner from "../../../__tests__/samples/samplePractitioner.json";

initializeIcons();

const practitioner = samplePractitioner as IPractitioner;

const classNames = mergeStyleSets({
  fileIconHeaderIcon: {
    padding: 0,
    fontSize: "16px"
  },
  fileIconCell: {
    textAlign: "center",
    selectors: {
      "&:before": {
        content: ".",
        display: "inline-block",
        verticalAlign: "middle",
        height: "100%",
        width: "0px",
        visibility: "hidden"
      }
    }
  },
  fileIconImg: {
    verticalAlign: "middle",
    maxHeight: "16px",
    maxWidth: "16px"
  },
  controlWrapper: {
    display: "flex",
    flexWrap: "wrap"
  },
  exampleToggle: {
    display: "inline-block",
    marginBottom: "10px",
    marginRight: "30px"
  },
  selectionDetails: {
    marginBottom: "20px"
  }
});
const controlStyles = {
  root: {
    margin: "0 30px 20px 0",
    maxWidth: "300px"
  }
};

export interface IHologramsDetailsListState {
  columns: IColumn[];
  items: IHologramDocument[];
  selectionDetails: string;
  isModalSelection: boolean;
}

export interface IHologramDocument {
  wrappedHologram: IHologram;
  titleReadable: string;
  authorReadable: string;
  subjectReadable: string;
  createdDateReadable: string;
  createdDateValue: number;
  fileSizeInKbValue: number;
  fileSizeInKbReadable: string;
}

class HologramsDetailsList extends React.Component<
  {},
  IHologramsDetailsListState
> {
  private _selection: Selection;
  private _allItems: IHologramDocument[];

  constructor(props: {}) {
    super(props);

    this._allItems = _mapHologramsToDocuments();

    const columns: IColumn[] = [
      {
        key: "col:fileType",
        name: "File Type",
        className: classNames.fileIconCell,
        iconClassName: classNames.fileIconHeaderIcon,
        ariaLabel:
          "Column operations for File type, Press to sort on File type",
        iconName: "Page",
        isIconOnly: true,
        fieldName: undefined, // overwrite with onRender()
        minWidth: 16,
        maxWidth: 16,
        // onColumnClick: this._onColumnClick,
        onRender: (item: IHologramDocument) => (
          <Icon iconName="HealthSolid" className={classNames.fileIconImg} />
        )
      },

      {
        key: "col:subject",
        name: "Subject",
        fieldName: "subjectReadable",
        minWidth: 150,
        maxWidth: 350,
        isRowHeader: true,
        isResizable: true,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingAriaLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        data: "string",
        isPadded: true
      },

      {
        key: "col:title",
        name: "Title",
        fieldName: "titleReadable",
        minWidth: 150,
        maxWidth: 350,
        isRowHeader: true,
        isResizable: true,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingAriaLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        data: "string",
        isPadded: true
      },

      {
        key: "col:date",
        name: "Date created",
        fieldName: "createdDateValue",
        minWidth: 70,
        maxWidth: 90,
        isResizable: true,
        onColumnClick: this._onColumnClick,
        data: "number",
        onRender: (item: IHologramDocument) => {
          return <span>{item.createdDateReadable}</span>;
        },
        isPadded: true
      },

      {
        key: "col:author",
        name: "Created by",
        fieldName: "authorReadable",
        minWidth: 70,
        maxWidth: 90,
        isResizable: true,
        isCollapsible: true,
        data: "string",
        onColumnClick: this._onColumnClick,
        onRender: (item: IHologramDocument) => {
          return <span>{item.authorReadable}</span>;
        },
        isPadded: true
      },

      {
        key: "col:size",
        name: "File size",
        fieldName: "fileSizeInKbValue",
        minWidth: 70,
        maxWidth: 90,
        isResizable: true,
        isCollapsible: true,
        data: "number",
        onColumnClick: this._onColumnClick,
        onRender: (item: IHologramDocument) => {
          return <span>{item.fileSizeInKbReadable}</span>;
        }
      }
    ];

    this._selection = new Selection({
      onSelectionChanged: () => {
        this.setState({
          selectionDetails: this._getSelectionDetails()
        });
      }
    });

    this.state = {
      items: this._allItems,
      columns: columns,
      selectionDetails: this._getSelectionDetails(),
      isModalSelection: false
    };
  }

  public render() {
    const { columns, items, selectionDetails, isModalSelection } = this.state;

    return (
      <Fabric>
        <div className={classNames.controlWrapper}>
          <Toggle
            label="Enable modal selection"
            checked={isModalSelection}
            onChange={this._onChangeModalSelection}
            onText="Modal"
            offText="Normal"
            styles={controlStyles}
          />
          <TextField
            label="Filter by subject name:"
            onChange={this._onChangeText}
            styles={controlStyles}
          />
        </div>
        <div className={classNames.selectionDetails}>{selectionDetails}</div>
        <DetailsList
          items={items}
          columns={columns}
          selectionMode={
            isModalSelection ? SelectionMode.multiple : SelectionMode.none
          }
          setKey="set"
          layoutMode={DetailsListLayoutMode.justified}
          isHeaderVisible={true}
          selection={this._selection}
          selectionPreservedOnEmptyClick={true}
          onItemInvoked={this._onItemInvoked}
          enterModalSelectionOnTouch={true}
          ariaLabelForSelectionColumn="Toggle selection"
          ariaLabelForSelectAllCheckbox="Toggle selection for all items"
        />
      </Fabric>
    );
  }

  public componentDidUpdate(
    previousProps: any,
    previousState: IHologramsDetailsListState
  ) {
    if (
      previousState.isModalSelection !== this.state.isModalSelection &&
      !this.state.isModalSelection
    ) {
      this._selection.setAllSelected(false);
    }
  }

  private _onChangeModalSelection = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean = false
  ): void => {
    this.setState({ isModalSelection: checked });
  };

  private _onChangeText = (
    ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>,
    text: string = ""
  ): void => {
    this.setState({
      items: text
        ? this._allItems.filter(
            i =>
              i.subjectReadable.toLowerCase().indexOf(text.toLowerCase()) > -1
          )
        : this._allItems
    });
  };

  private _onItemInvoked(item: any): void {
    alert(`Item invoked: ${item.name}`);
  }

  private _getSelectionDetails(): string {
    const selectionCount = this._selection.getSelectedCount();

    switch (selectionCount) {
      case 0:
        return "No items selected";
      case 1:
        return (
          "1 item selected: " +
          (this._selection.getSelection()[0] as IHologramDocument)
            .wrappedHologram.title
        );
      default:
        return `${selectionCount} items selected`;
    }
  }

  private _onColumnClick = (
    ev: React.MouseEvent<HTMLElement>,
    column: IColumn
  ): void => {
    const { columns, items } = this.state;
    const newColumns: IColumn[] = columns.slice();
    const currColumn: IColumn = newColumns.filter(
      currCol => column.key === currCol.key
    )[0];
    newColumns.forEach((newCol: IColumn) => {
      if (newCol === currColumn) {
        currColumn.isSortedDescending = !currColumn.isSortedDescending;
        currColumn.isSorted = true;
      } else {
        newCol.isSorted = false;
        newCol.isSortedDescending = true;
      }
    });
    const newItems = _copyAndSort(
      items,
      currColumn.fieldName!,
      currColumn.isSortedDescending
    );
    this.setState({
      columns: newColumns,
      items: newItems
    });
  };
}

function _copyAndSort<T>(
  items: T[],
  columnKey: string,
  isSortedDescending?: boolean
): T[] {
  const key = columnKey as keyof T;
  return items
    .slice(0)
    .sort((a: T, b: T) =>
      (isSortedDescending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1
    );
}

function _mapHologramsToDocuments(): IHologramDocument[] {
  const holograms = sampleHolograms as IHologram[];

  return holograms.map(hologram => {
    const createdDate = new Date(hologram.createdDate);

    return {
      titleReadable: hologram.title,
      authorReadable: _getReadableAuthorName(hologram),
      subjectReadable: _getReadableSubjectName(hologram),
      wrappedHologram: hologram,
      createdDateReadable: createdDate.toLocaleDateString(),
      createdDateValue: createdDate.valueOf(),
      fileSizeInKbValue: hologram.fileSizeInKb,
      fileSizeInKbReadable: `${hologram.fileSizeInKb} kB`
    };
  });
}

function _getReadableAuthorName(hologram: IHologram): string {
  let authorName;
  if (!hologram.author) {
    authorName = UNKNOWN_PERSON_NAME;
  } else if (hologram.author.id === practitioner.id) {
    authorName = "You";
  } else {
    authorName = hologram.author.id;
  }
  return authorName;
}

function _getReadableSubjectName(hologram: IHologram): string {
  if (!hologram.subject.name) {
    return UNKNOWN_PERSON_NAME;
  } else {
    return hologram.subject.name.full;
  }
}

export default HologramsDetailsList;
