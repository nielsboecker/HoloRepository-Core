import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Layout } from "antd";
import MenuHeader from "./MenuHeader";
import MainFooter from "../../core/MainFooter";

class AuthContainer extends Component<RouteComponentProps> {
  backgroundStyle = {
    //background: "radial-gradient(black, transparent)"
    background: "rgba(1,1,1,0.2)"
  };

  render() {
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
  }
}

export default AuthContainer;
