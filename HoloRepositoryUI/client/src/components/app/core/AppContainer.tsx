import React, { Component } from "react";
import { Redirect, RouteComponentProps } from "@reach/router";
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
    } else if (this.props.context!.loginWasInitiated) {
      // Will appear after initiating login, and before the server returns the practitioners's details
      return (
        <div>
          <Spinner label="Loading..." />
        </div>
      );
    } else {
      // This will happen if practitioners go directly to a subpage instead of starting on the login
      // page. Given that we currently don't store anything in the cache, after a direct load or
      // page refresh, there is no way to know who the user is.
      return <Redirect to="/" noThrow />;
    }
  }
}

export default withAppContext(AppContainer);
