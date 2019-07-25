import React, { Component } from "react";
import { Link, navigate } from "@reach/router";
import {
  IImageProps,
  Image,
  ImageFit,
  IPersonaSharedProps,
  Persona,
  PersonaPresence,
  PersonaSize
} from "office-ui-fabric-react";
import { Layout, Menu } from "antd";
import "./MenuHeader.scss";
import appLogo from "../../../assets/logo/2x/logo_and_font@2x.png";
import { PropsWithContext, withAppContext } from "../../shared/AppState";

const { Header } = Layout;
const { SubMenu } = Menu;

const imageProps: IImageProps = {
  src: appLogo,
  imageFit: ImageFit.cover,
  maximizeFrame: true
};

const practitionerPersona: IPersonaSharedProps = {};

class MenuHeader extends Component<PropsWithContext> {
  render() {
    const { practitioner } = this.props.context!;

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
                  imageUrl={practitioner!.pictureUrl}
                  text={practitioner!.name.full}
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

//export const withContext = <P extends {}>(Component: React.ComponentType<P>) =>
//  class WithContext extends React.PureComponent<P & IAppState> {
//    render() {
//      return (
//        <AppContext.Consumer>
//          {(context: IAppState) => <Component {...this.props} {...context} />}
//        </AppContext.Consumer>
//      );
//    }
//  };

//export const withContext = <P extends {}>(Component: React.ComponentType<P>) =>
//  class WithContext extends React.PureComponent<P & IAppState> {
//    render() {
//      return (
//        <AppContext.Consumer>
//          {(context: IAppState) => <Component {...this.props} appContext={context} />}
//        </AppContext.Consumer>
//      );
//    }
//  };

export default withAppContext(MenuHeader);
