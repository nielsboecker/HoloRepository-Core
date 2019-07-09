import React, { Component } from "react";
import { TextField } from "office-ui-fabric-react/lib-commonjs/TextField";
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
import { IHologram, IPractitioner, unknownPersonName } from "../../../types";
import {
  fileTypeCol,
  subjectCol,
  titleCol,
  dateCol,
  authorCol,
  fileSizeCol
} from "./HologramsDetailsListColumns";
import samplePractitioner from "../../../__tests__/samples/samplePractitioner.json";

const practitioner = samplePractitioner as IPractitioner;

const classNames = mergeStyleSets({
  controlWrapper: {
    display: "flex",
    flexWrap: "wrap"
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

const defaultColumns: IColumn[] = [
  fileTypeCol,
  subjectCol,
  titleCol,
  dateCol,
  authorCol,
  fileSizeCol
];

export interface IHologramsDetailsListState {
  columns: IColumn[];
  items: IHologramDocument[];
  selectionDetails: string;
}

export interface IHologramsDetailsListProps {
  columns?: IColumn[];
  showFilters: boolean;
  patientId?: string;
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

class HologramsDetailsList extends Component<
  IHologramsDetailsListProps,
  IHologramsDetailsListState
> {
  private _selection: Selection = new Selection({
    onSelectionChanged: () => {
      this.setState({
        selectionDetails: this._getSelectionDetails()
      });
    }
  });

  private _allItems: IHologramDocument[] = _mapHologramsToDocuments();

  state = {
    items: this._allItems,
    columns: this.props.columns ? this.props.columns : defaultColumns,
    selectionDetails: this._getSelectionDetails()
  };

  public render() {
    const { columns, items, selectionDetails } = this.state;

    return (
      <Fabric>
        {this.props.showFilters && (
          <div className="filters">
            <div className={classNames.controlWrapper}>
              <TextField
                label="Filter by subject name:"
                onChange={this._onChangeText}
                styles={controlStyles}
              />
            </div>
            <div className={classNames.selectionDetails}>{selectionDetails}</div>
          </div>
        )}

        <DetailsList
          items={items}
          columns={columns}
          onColumnHeaderClick={this._onColumnHeaderClick}
          selectionMode={SelectionMode.single}
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

  private _onChangeText = (
    ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>,
    text: string = ""
  ): void => {
    this.setState({
      items: text
        ? this._allItems.filter(
            i => i.subjectReadable.toLowerCase().indexOf(text.toLowerCase()) > -1
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
          (this._selection.getSelection()[0] as IHologramDocument).wrappedHologram.title
        );
      default:
        return `${selectionCount} items selected`;
    }
  }

  private _onColumnHeaderClick = (_: any, column: IColumn | undefined): void => {
    const { columns, items } = this.state;
    const newColumns: IColumn[] = columns.slice();
    const currColumn: IColumn = newColumns.filter(currCol => column!.key === currCol.key)[0];
    newColumns.forEach((newCol: IColumn) => {
      if (newCol === currColumn) {
        currColumn.isSortedDescending = !currColumn.isSortedDescending;
        currColumn.isSorted = true;
      } else {
        newCol.isSorted = false;
        newCol.isSortedDescending = true;
      }
    });
    const newItems = _copyAndSort(items, currColumn.fieldName!, currColumn.isSortedDescending);
    this.setState({
      columns: newColumns,
      items: newItems
    });
  };
}

function _copyAndSort<T>(items: T[], columnKey: string, isSortedDescending?: boolean): T[] {
  const key = columnKey as keyof T;
  return items
    .slice(0)
    .sort((a: T, b: T) => ((isSortedDescending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1));
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
  if (!hologram.author || !hologram.author.name) {
    authorName = unknownPersonName;
  } else if (hologram.author.id === practitioner.id) {
    authorName = "You";
  } else {
    authorName = hologram.author.name.full;
  }
  return authorName;
}

function _getReadableSubjectName(hologram: IHologram): string {
  if (!hologram.subject.name) {
    return unknownPersonName;
  } else {
    return hologram.subject.name.full;
  }
}

export default HologramsDetailsList;
