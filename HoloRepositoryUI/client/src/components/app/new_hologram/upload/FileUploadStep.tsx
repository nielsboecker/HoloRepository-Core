import React, { Component } from "react";
import { getId, Label } from "office-ui-fabric-react";
import { Icon, message, Upload } from "antd";
import { RcFile } from "antd/lib/upload";

const { Dragger } = Upload;
const draggerId = getId("dragger");
const maxFileSizeInMb = 10;

export interface IFileUploadStepProps {
  onHologramFileChange: (file: File) => void;
}

class FileUploadStep extends Component<IFileUploadStepProps> {
  render() {
    return (
      <div>
        <Label htmlFor={draggerId}>Upload your file</Label>
        <Dragger
          id={draggerId}
          name="file"
          multiple={false}
          accept=".glb"
          beforeUpload={this._beforeUpload}
        >
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

  _beforeUpload = (file: RcFile, _: any): false => {
    const fileSizeOkay = file.size / 1024 / 1024 < maxFileSizeInMb;
    if (fileSizeOkay) {
      this.props.onHologramFileChange(file);
    } else {
      message.error(`File must be ${maxFileSizeInMb} MB at most`);
    }
    // Note: Manually handle upload
    return false;
  };
}

export default FileUploadStep;
