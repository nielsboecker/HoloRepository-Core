import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Layout } from "antd";
import MenuHeader from "./MenuHeader";
import MainFooter from "../../shared/MainFooter";
import { PropsWithContext, withAppContext } from "../../shared/AppState";
import { Spinner } from "office-ui-fabric-react";

class AppContainer extends Component<RouteComponentProps & PropsWithContext> {
  backgroundStyle = {
    //background: "radial-gradient(black, transparent)"
    background: "rgba(1,1,1,0.2)"
  };

  render() {
    // Render this component and all children only when the user is authenticated
    if (this.props.context!.practitioner) {
      return (
        <Layout style={{ ...this.backgroundStyle, height: "100vh" }}>
          <MenuHeader />

          <Layout.Content
            style={{
              padding: "0 50px",
              marginTop: "50px",
              marginBottom: "90px",
              display: "flex",
              justifyContent: "center",
              overflowY: "auto"
            }}
          >
            {this.props.children}
          </Layout.Content>

          <MainFooter
            style={{
              background: "rgba(1,1,1,0.2)",
              position: "fixed",
              right: 0,
              bottom: 0,
              left: 0
            }}
          />
        </Layout>
      );
    } else if (!this.props.context!.loginFlag) {
      this._hrefToLoginPage();
      return <div />;
    } else {
      return (
        <div>
          <Spinner label="Loading..." />
        </div>
      );
    }
  }

  private _hrefToLoginPage = (): void => {
    window.location.href = "/";
  };
}

export default withAppContext(AppContainer);
