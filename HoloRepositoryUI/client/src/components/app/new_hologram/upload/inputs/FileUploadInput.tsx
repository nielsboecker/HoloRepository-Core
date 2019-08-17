import React, { Component } from "react";
import { Icon, message, Upload } from "antd";
import { getId } from "@uifabric/utilities";
import { PassDownProps, WrapperProps } from "formsy-react/dist/Wrapper";
import { Label } from "office-ui-fabric-react";
import { RcFile } from "antd/lib/upload";
import { withFormsy } from "formsy-react";

const { Dragger } = Upload;
const draggerId = getId("dragger");

interface Props extends Partial<PassDownProps>, Partial<WrapperProps> {
  maxFileSizeInMb: number;
}

interface State {
  fileList: object[];
}

class FileUploadInput extends Component<Props, State> {
  state = {
    fileList: []
  };

  _handleChange = (file: File): void => {
    console.log(this.props);

    this.props.setValue!(file);
  };

  render() {
    const { maxFileSizeInMb } = this.props;
    const { fileList } = this.state;

    return (
      <div>
        <Label htmlFor={draggerId}>Upload your file</Label>

        <Dragger
          id={draggerId}
          name="file"
          multiple={false}
          accept=".glb"
          fileList={fileList}
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
    console.log(`Trying to upload file ${file.name} [Size: ${file.size} bytes]`);

    if (this._check_fileSize(file) && this._check_fileType(file)) {
      // Use this file
      this._handleChange(file);

      // Replace old file in fileList to render in the view, and always render only one
      this.setState(state => ({
        fileList: [file]
      }));
    } else {
      message.error("Couldn't upload file.");
    }

    // Note: Always return false to manually handle upload
    return false;
  };

  _check_fileSize = (file: RcFile): boolean => {
    const { maxFileSizeInMb } = this.props;
    const fileSize = file.size / 1024 / 1024;
    return fileSize < maxFileSizeInMb;
  };

  _check_fileType = (file: RcFile): boolean => {
    // Note: Should always be true due to "accept" setting of Dragger
    return file.name.endsWith(".glb");
  };
}

export default withFormsy(FileUploadInput);
