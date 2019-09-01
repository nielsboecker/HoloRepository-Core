import React, { Component } from "react";
import { Link, Redirect, RouteComponentProps } from "@reach/router";
import {
  Dropdown,
  IDropdownOption,
  TextField,
  PrimaryButton,
  IImageProps,
  ImageFit,
  Image
} from "office-ui-fabric-react";
import { Layout } from "antd";
import appLogo from "../../assets/logo/2x/logo_and_font@2x.png";
import MainFooter from "../shared/MainFooter";
import { PropsWithContext, withAppContext } from "../shared/AppState";

//The practitioners list are hard-coded now, because the authentication is just a proof-of-concept
const options: IDropdownOption[] = [
  { key: "a100/03825", text: "Maudie Kirlin" },
  { key: "a101/03826", text: "Erlinda Franecki" },
  { key: "a102/03827", text: "Jonah Schroeder" }
];

const imageProps: IImageProps = {
  src: appLogo,
  imageFit: ImageFit.cover,
  maximizeFrame: true
};

class LoginPage extends Component<RouteComponentProps & PropsWithContext> {
  selectedItem: string | number = "";

  backgroundStyle = {
    background: "rgba(1,1,1,0.2)"
  };

  loginLogo = {
    width: "420px",
    height: "70px",
    background: "rgba(255, 255, 255, 0.2)",
    margin: "14px 14px 14px 14px"
  };

  LoginContainer = {
    backgroundColor: "white",
    maxHeight: "325px",
    minWidth: "500px",
    maxWidth: "850px",
    padding: "24px"
  };

  render() {
    return (
      <Layout style={{ ...this.backgroundStyle, height: "100vh" }}>
        <Layout.Content
          style={{
            padding: "0 50px",
            marginTop: "200px",
            display: "flex",
            justifyContent: "center"
          }}
        >
          <div style={{ ...this.LoginContainer }}>
            <div style={{ ...this.loginLogo }}>
              <Image {...(imageProps as any)} alt="app_logo" />
            </div>
            <Dropdown
              placeholder="Select your account"
              label="Practitioner"
              options={options}
              onChange={this._handleDropdownOptionChange}
            />
            <TextField
              label="Password"
              defaultValue={"password"}
              type="password"
              style={{ width: "300" }}
            />
            <div
              style={{
                marginTop: "20px",
                display: "flex",
                justifyContent: "center"
              }}
            >
              <Link to="/app/patients">
                <PrimaryButton
                  data-automation-id="login"
                  text="Login"
                  allowDisabledFocus={true}
                  onClick={this._selectPractitioner}
                />
              </Link>
            </div>
          </div>
        </Layout.Content>

        <MainFooter style={this.backgroundStyle} />
      </Layout>
    );
  }

  private _selectPractitioner = () => {
    if (this.selectedItem === "") {
      alert(`Please select the practitioner account!`);
    } else {
      if (typeof this.selectedItem !== "number") {
        const id = this.selectedItem.substring(0, this.selectedItem.indexOf("/"));
        const pin = this.selectedItem.substring(this.selectedItem.indexOf("/") + 1);
        this.props.context!.handleLogin(id, pin);
      }
    }
  };

  private _handleDropdownOptionChange = (
    event: React.FormEvent<HTMLDivElement>,
    option?: IDropdownOption
  ): void => {
    this.selectedItem = option!.key;
  };
}

export default withAppContext(LoginPage);
