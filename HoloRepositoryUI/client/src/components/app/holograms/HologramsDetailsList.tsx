import React, { Component } from "react";
import {
  DetailsList,
  DetailsListLayoutMode,
  Fabric,
  getId,
  IColumn,
  IObjectWithKey,
  Label,
  SearchBox,
  Selection,
  SelectionMode,
  Spinner
} from "office-ui-fabric-react";
import { Col, Row } from "antd";
import {
  authorCol,
  dateCol,
  fileSizeCol,
  fileTypeCol,
  subjectCol,
  titleCol
} from "./HologramsDetailsListColumns";
import HologramsCommandBar from "./HologramsCommandBar";
import FilterStatusMessageBar from "../core/FilterStatusMessageBar";
import { IHologram } from "../../../../../types";
import { PidToPatientsMap, PropsWithContext, withAppContext } from "../../shared/AppState";

// const unknownPersonName = "Unknown";

const defaultColumns: IColumn[] = [
  fileTypeCol,
  subjectCol,
  titleCol,
  dateCol,
  authorCol,
  fileSizeCol
];

export interface IHologramsDetailsListState {
  loadingData: boolean;
  columns: IColumn[];
  filterText: string;
  allHologramDocuments: IHologramDocument[];
  displayedHologramDocuments: IHologramDocument[];
  selectionDetails: string;
}

export interface IHologramsDetailsListProps extends PropsWithContext {
  columns?: IColumn[];
  showFilters: boolean;
  limitToSelectedPatient?: boolean;
}

export interface IHologramDocument extends IObjectWithKey {
  wrappedHologram: IHologram;
  titleDisplay: string;
  authorDisplay: string;
  subjectDisplay: string;
  creationDateDisplay: string;
  creationDateValue: number;
  fileSizeInKbValue: number;
  fileSizeInKbDisplay: string;
}

class HologramsDetailsList extends Component<
  IHologramsDetailsListProps,
  IHologramsDetailsListState
> {
  constructor(props: IHologramsDetailsListProps) {
    super(props);

    this.state = {
      loadingData: true,
      columns: this.props.columns ? this.props.columns : defaultColumns,
      filterText: "",
      allHologramDocuments: [],
      displayedHologramDocuments: [],
      selectionDetails: this._getSelectionDetails()
    };
  }

  private _selection: Selection = new Selection({
    onSelectionChanged: () => {
      this.setState({
        selectionDetails: this._getSelectionDetails()
      });
    }
  });

  public render() {
    const {
      columns,
      allHologramDocuments,
      displayedHologramDocuments,
      selectionDetails
    } = this.state;

    // Ensure that the ID is unique on the page.
    const filterSubjectId = getId("filterSubject");

    if (this.state.loadingData) {
      return <Spinner label="Loading holograms..." />;
    } else {
      return (
        <Fabric>
          {this.props.showFilters && (
            <div className="filters">
              <Row>
                <Col span={12} style={{ padding: "0 24px" }}>
                  <div>
                    <Label htmlFor={filterSubjectId}>Filter by subject</Label>
                    <SearchBox
                      id={filterSubjectId}
                      placeholder="Filter holograms..."
                      onChange={this._onChangeText}
                      iconProps={{ iconName: "Filter" }}
                    />
                  </div>
                </Col>
              </Row>

              <FilterStatusMessageBar
                totalCount={allHologramDocuments.length}
                filteredCount={displayedHologramDocuments.length}
                itemEntityName="hologram"
              />
            </div>
          )}

          {displayedHologramDocuments.length === 0 ? (
            <div>
              <p>
                No holograms available.
                {this.props.showFilters && " Change filter settings or create a new hologram."}
              </p>
            </div>
          ) : (
            <div className="list">
              <DetailsList
                items={displayedHologramDocuments}
                columns={columns}
                onColumnHeaderClick={this._onColumnHeaderClick}
                selectionMode={SelectionMode.multiple}
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

              <div>{selectionDetails}</div>
            </div>
          )}

          <div className="commands" style={{ marginTop: "24px" }}>
            <HologramsCommandBar selection={this._selection} />
          </div>
        </Fabric>
      );
    }
  }

  componentDidMount(): void {
    // This is needed to show data if it is already loaded and user navigates here from other page
    this._updateHologramState_all();
  }

  componentDidUpdate(
    prevProps: Readonly<IHologramsDetailsListProps>,
    prevState: Readonly<IHologramsDetailsListState>
  ): void {
    // Note: To properly display spinner until holograms are loaded, more complex logic required
    if (this.state.loadingData && this.props.context!.patients) {
      this.setState({ loadingData: false });
    }

    if (prevProps.context!.patients !== this.props.context!.patients) {
      this._updateHologramState_all();
    }

    if (prevState.filterText !== this.state.filterText) {
      this._updateHologramState_displayed();
    }
  }

  private _updateHologramState_all = () => {
    let { patients, selectedPatientId } = this.props.context!;

    if (this.props.limitToSelectedPatient && selectedPatientId) {
      patients = { [selectedPatientId]: patients[selectedPatientId] };
    }

    const allHologramDocuments: IHologramDocument[] = this._mapToDocuments(patients);
    this.setState({ allHologramDocuments }, this._updateHologramState_displayed);
  };

  private _updateHologramState_displayed = () => {
    const { allHologramDocuments, filterText } = this.state;
    const displayedHologramDocuments = allHologramDocuments.filter(doc =>
      doc.subjectDisplay.toLowerCase().includes(filterText.toLowerCase())
    );
    this.setState({ displayedHologramDocuments });
  };

  private _onChangeText = (_: any, filterText: string = ""): void => {
    this.setState({ filterText });
  };

  private _onItemInvoked = (item: any): void => {
    alert(`Item invoked: ${item.name}`);
  };

  private _getSelectionDetails = (): string => {
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
  };

  private _onColumnHeaderClick = (_: any, column: IColumn | undefined): void => {
    const { columns, displayedHologramDocuments } = this.state;
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
    const newItems = _copyAndSort(
      displayedHologramDocuments,
      currColumn.fieldName!,
      currColumn.isSortedDescending
    );
    this.setState({
      columns: newColumns,
      displayedHologramDocuments: newItems
    });
  };

  private _mapToDocuments = (holograms: PidToPatientsMap): IHologramDocument[] => {
    const combinedHologramDocuments: IHologramDocument[] = [];

    Object.entries(holograms).forEach(([pid, patient]) => {
      if (patient.holograms && patient.holograms.length >= 1) {
        const patientHolograms = patient.holograms.map(hologram => {
          const creationDate = new Date(hologram.creationDate);

          return {
            // Note: appending random suffix because of duplicate IDs in mocked data, will be replaced
            key: hologram.hid + Math.random(),
            titleDisplay: hologram.title,
            authorDisplay: this._getDisplayAuthorName(hologram),
            subjectDisplay: this._getDisplaySubjectName(hologram),
            wrappedHologram: hologram,
            creationDateDisplay: creationDate.toLocaleDateString(),
            creationDateValue: creationDate.valueOf(),
            fileSizeInKbValue: hologram.fileSizeInKb,
            fileSizeInKbDisplay: `${hologram.fileSizeInKb} kB`
          };
        });
        combinedHologramDocuments.push(...patientHolograms);
      }
    });

    return combinedHologramDocuments;
  };

  private _getDisplayAuthorName = (hologram: IHologram): string => {
    //    const { practitioner } = this.props.context!;

    let authorName = "Unknown";
    // TODO: Repair

    //    if (!hologram.author || !hologram.author.name) {
    //      authorName = unknownPersonName;
    //    } else if (hologram.author.aid === practitioner!.pid) {
    //      authorName = "You";
    //    } else {
    //      authorName = hologram.author.name.full;
    //    }
    return authorName;
  };

  private _getDisplaySubjectName = (hologram: IHologram): string => {
    return "Unknown";
    // TODO: Repair

    //    if (!hologram.subject.name) {
    //      return unknownPersonName;
    //    } else {
    //      return hologram.subject.name.full;
    //    }
  };
}

function _copyAndSort<T>(items: T[], columnKey: string, isSortedDescending?: boolean): T[] {
  const key = columnKey as keyof T;
  return items
    .slice(0)
    .sort((a: T, b: T) => ((isSortedDescending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1));
}

export default withAppContext(HologramsDetailsList);
