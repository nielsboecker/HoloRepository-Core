import React, { Component } from "react";
import { Menu, Layout } from "antd";
import { Image, IImageProps, ImageFit } from "office-ui-fabric-react/lib/Image";

import "antd/dist/antd.css";
import "./MenuHeader.scss";
import appLogo from "../../../assets/logo/2x/logo_and_font@2x.png";

const { Header } = Layout;

const imageProps: IImageProps = {
  src: appLogo,
  imageFit: ImageFit.cover,
  maximizeFrame: true
};

class MenuHeader extends Component {
  render() {
    return (
      <Header>
        <div className="logo">
          <Image {...(imageProps as any)} alt="HoloRepository logo" />
        </div>

        <Menu
          theme="light"
          mode="horizontal"
          defaultSelectedKeys={["patients"]}
          style={{ lineHeight: "64px" }}
        >
          <Menu.Item key="patients">Patients</Menu.Item>
          <Menu.Item key="holograms">Holograms</Menu.Item>
          <Menu.Item key="devices">Devices</Menu.Item>
        </Menu>
      </Header>
    );
  }
}

export default MenuHeader;
