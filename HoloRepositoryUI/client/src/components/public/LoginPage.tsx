import React, { Component } from "react";
import { RouteComponentProps, navigate } from "@reach/router";
import {
  Dialog,
  Dropdown,
  IDropdownOption,
  TextField,
  PrimaryButton,
  IImageProps,
  ImageFit,
  Image,
  DialogType,
  DialogFooter
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

export type LoginPageProps = RouteComponentProps & PropsWithContext;

export interface ILoginPageState {
  showErrorMessage: boolean;
}

class LoginPage extends Component<LoginPageProps, ILoginPageState> {
  state = {
    showErrorMessage: false
  };

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
              <PrimaryButton
                data-automation-id="login"
                text="Login"
                allowDisabledFocus={true}
                onClick={this._handlePractitionerLogin}
              />
            </div>
          </div>
        </Layout.Content>

        <Dialog
          hidden={!this.state.showErrorMessage}
          onDismiss={this._closeLoginErrorMessage}
          dialogContentProps={{
            type: DialogType.normal,
            title: "Login failed",
            subText: "Please select the practitioner account"
          }}
          modalProps={{
            isBlocking: false,
            styles: { main: { maxWidth: 450 } }
          }}
        >
          <DialogFooter>
            <PrimaryButton onClick={this._closeLoginErrorMessage} text="Okay" />
          </DialogFooter>
        </Dialog>

        <MainFooter style={this.backgroundStyle} />
      </Layout>
    );
  }

  private _handlePractitionerLogin = () => {
    if (this.selectedItem === "") {
      this._showLoginErrorMessage();
    } else {
      if (typeof this.selectedItem !== "number") {
        const id = this.selectedItem.substring(0, this.selectedItem.indexOf("/"));
        const pin = this.selectedItem.substring(this.selectedItem.indexOf("/") + 1);

        // Handle login in global state
        this.props.context!.handleLogin(id, pin);

        // Redirect to patient page
        navigate("/app/patients");
      }
    }
  };

  private _handleDropdownOptionChange = (
    event: React.FormEvent<HTMLDivElement>,
    option?: IDropdownOption
  ): void => {
    this.selectedItem = option!.key;
  };

  private _showLoginErrorMessage = (): void => {
    this.setState({ showErrorMessage: true });
  };

  private _closeLoginErrorMessage = (): void => {
    this.setState({ showErrorMessage: false });
  };
}

export default withAppContext(LoginPage);
