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
              display: "flex",
              justifyContent: "center"
            }}
          >
            {this.props.children}
          </Layout.Content>

          <MainFooter style={this.backgroundStyle} />
        </Layout>
      );
    } else {
      return (
        <div>
          <Spinner label="Loading..." />
        </div>
      )
    }
  }
}

export default withAppContext(AppContainer);
