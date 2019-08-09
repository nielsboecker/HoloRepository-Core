import React from "react";
import { IColumn, Icon, mergeStyleSets } from "office-ui-fabric-react";
import { IHologramDocument } from "./HologramsDetailsList";

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
  }
});

const fileTypeCol: IColumn = {
  key: "col:fileType",
  name: "File Type",
  className: classNames.fileIconCell,
  iconClassName: classNames.fileIconHeaderIcon,
  ariaLabel: "Column operations for File type, Press to sort on File type",
  iconName: "Page",
  isIconOnly: true,
  fieldName: undefined, // overwrite with onRender()
  minWidth: 16,
  maxWidth: 16,
  onRender: (item: IHologramDocument) => (
    <Icon iconName="HealthSolid" className={classNames.fileIconImg} />
  )
};

const subjectCol: IColumn = {
  key: "col:subject",
  name: "Subject",
  fieldName: "subjectDisplay",
  minWidth: 150,
  maxWidth: 350,
  isRowHeader: true,
  isResizable: true,
  isSorted: true,
  isSortedDescending: false,
  sortAscendingAriaLabel: "Sorted A to Z",
  sortDescendingAriaLabel: "Sorted Z to A",
  data: "string",
  isPadded: true
};

const titleCol: IColumn = {
  key: "col:title",
  name: "Title",
  fieldName: "titleDisplay",
  minWidth: 150,
  maxWidth: 350,
  isRowHeader: true,
  isResizable: true,
  isSorted: true,
  isSortedDescending: false,
  sortAscendingAriaLabel: "Sorted A to Z",
  sortDescendingAriaLabel: "Sorted Z to A",
  data: "string",
  isPadded: true
};

const dateCol: IColumn = {
  key: "col:date",
  name: "Date created",
  fieldName: "creationDateValue",
  minWidth: 70,
  maxWidth: 90,
  isResizable: true,
  data: "number",
  onRender: (item: IHologramDocument) => {
    return <span>{item.creationDateDisplay}</span>;
  },
  isPadded: true
};

const authorCol: IColumn = {
  key: "col:author",
  name: "Created by",
  fieldName: "authorDisplay",
  minWidth: 70,
  maxWidth: 90,
  isResizable: true,
  isCollapsible: true,
  data: "string",
  onRender: (item: IHologramDocument) => {
    return <span>{item.authorDisplay}</span>;
  },
  isPadded: true
};

const fileSizeCol: IColumn = {
  key: "col:size",
  name: "File size",
  fieldName: "fileSizeInKbValue",
  minWidth: 70,
  maxWidth: 90,
  isResizable: true,
  isCollapsible: true,
  data: "number",
  onRender: (item: IHologramDocument) => {
    return <span>{item.fileSizeInKbDisplay}</span>;
  }
};

export { fileTypeCol, subjectCol, titleCol, dateCol, authorCol, fileSizeCol };
