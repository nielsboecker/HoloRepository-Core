import React, { Component } from "react";
import { Menu, Layout } from "antd";
import { Image, IImageProps, ImageFit } from "office-ui-fabric-react/lib/Image";

import "antd/dist/antd.css";
import "./MenuHeader.scss";
import appLogo from "../../../assets/logo/2x/logo_and_font@2x.png";
import { Link, navigate } from "@reach/router";
import { Practitioner } from "../../../types";

const { Header } = Layout;
const { SubMenu } = Menu;

const imageProps: IImageProps = {
  src: appLogo,
  imageFit: ImageFit.cover,
  maximizeFrame: true
};

class MenuHeader extends Component {
  render() {
    return (
      <Header>
        <Link to="/app/patients">
          <div className="logo">
            <Image {...(imageProps as any)} alt="HoloRepository logo" />
          </div>
        </Link>

        <Menu
          theme="light"
          mode="horizontal"
          defaultSelectedKeys={["patients"]}
          style={{ lineHeight: "64px" }}
        >
          <Menu.Item key="patients" onClick={({ key }) => this.doNavigate(key)}>
            Patients
          </Menu.Item>
          <Menu.Item
            key="holograms"
            onClick={({ key }) => this.doNavigate(key)}
          >
            Holograms
          </Menu.Item>
          <Menu.Item key="devices" onClick={({ key }) => this.doNavigate(key)}>
            Devices
          </Menu.Item>

          <SubMenu
            title={<span className="submenu-title-wrapper">User Name</span>}
            style={{ float: "right" }}
          >
            <Menu.Item
              key="profile"
              onClick={({ key }) => this.doNavigate(key)}
            >
              Show profile
            </Menu.Item>
            <Menu.Item key="logout" onClick={() => this.doLogout()}>
              Log out
            </Menu.Item>
          </SubMenu>
        </Menu>
      </Header>
    );
  }

  doLogout(): void {
    console.log("Log out");
    navigate("/");
  }

  doNavigate(component: string) {
    navigate(`/app/${component}`);
  }
}

export default MenuHeader;
