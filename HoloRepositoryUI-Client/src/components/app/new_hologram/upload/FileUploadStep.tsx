import React, { Component } from "react";
import { getId, Label } from "office-ui-fabric-react";
import { Upload, Icon, message } from "antd";
import { RcFile, UploadChangeParam } from "antd/lib/upload";
import { UploadFile } from "antd/lib/upload/interface";

const { Dragger } = Upload;
const draggerId = getId("dragger");
const maxFileSizeInMb = 10;

const beforeUpload: (file: RcFile, _: any) => boolean | PromiseLike<void> = file => {
  const fileSizeOkay = file.size / 1024 / 1024 < maxFileSizeInMb;
  if (!fileSizeOkay) {
    message.error(`File must be ${maxFileSizeInMb} MB at most`);
  }
  return fileSizeOkay;
};

const _draggerProps = {
  name: "file",
  multiple: false,
  accept: ".glb",
  beforeUpload: beforeUpload,
  action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
  onChange(info: UploadChangeParam<UploadFile>) {
    const { status } = info.file;
    if (status !== "uploading") {
      console.log(info.file, info.fileList);
    }
    if (status === "done") {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === "error") {
      message.error(`${info.file.name} file upload failed.`);
    }
  }
};

class FileUploadStep extends Component {
  render() {
    return (
      <div>
        <Label htmlFor={draggerId}>Upload your file</Label>
        <Dragger {..._draggerProps} id={draggerId}>
          <p className="ant-upload-drag-icon">
            <Icon type="inbox" />
          </p>
          <p className="ant-upload-text">Click or drag file to this area to upload</p>
          <p className="ant-upload-hint">
            Supports binary glTF files (GLB) up to {maxFileSizeInMb} MB
          </p>
        </Dragger>
      </div>
    );
  }
}

export default FileUploadStep;
