import React, { Component } from "react";
import { Menu, Layout } from "antd";
import { Image, IImageProps, ImageFit } from "office-ui-fabric-react/lib-commonjs/Image";
import {
  IPersonaSharedProps,
  Persona,
  PersonaSize,
  PersonaPresence
} from "office-ui-fabric-react/lib-commonjs/Persona";

import "antd/dist/antd.css";
import "./MenuHeader.scss";
import { Link, navigate } from "@reach/router";
import appLogo from "../../../assets/logo/2x/logo_and_font@2x.png";
import samplePractitioner from "../../../__tests__/samples/samplePractitioner.json";
import { IPractitioner } from "../../../types";

const { Header } = Layout;
const { SubMenu } = Menu;

const imageProps: IImageProps = {
  src: appLogo,
  imageFit: ImageFit.cover,
  maximizeFrame: true
};

const practitioner = samplePractitioner as IPractitioner;

const practitionerPersona: IPersonaSharedProps = {
  imageUrl: practitioner.pictureUrl,
  imageInitials: "NS",
  text: practitioner.name.full,
  secondaryText: "Practitioner"
  //tertiaryText: 'In a meeting',
  //optionalText: 'Available at 4:00pm'
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
          <Menu.Item key="holograms" onClick={({ key }) => this.doNavigate(key)}>
            Holograms
          </Menu.Item>
          <Menu.Item key="devices" onClick={({ key }) => this.doNavigate(key)}>
            Devices
          </Menu.Item>

          <SubMenu
            title={
              <div className="submenu-title-wrapper">
                <Persona
                  {...practitionerPersona}
                  size={PersonaSize.size32}
                  presence={PersonaPresence.online}
                  hidePersonaDetails={false}
                />
              </div>
            }
            style={{ float: "right", padding: "16px 0" }}
          >
            <Menu.Item key="profile" onClick={({ key }) => this.doNavigate(key)}>
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
