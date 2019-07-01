import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Layout } from "antd";
import MenuHeader from "./MenuHeader";
import MainFooter from "../../core/MainFooter";

class AuthContainer extends Component<RouteComponentProps> {
  render() {
    return (
      <Layout>
        <MenuHeader />

        <Layout.Content style={{ padding: "0 50px", marginTop: "50px" }}>
          <div style={{ background: "#fff", padding: 24, minHeight: 280 }}>
            {this.props.children}
          </div>
        </Layout.Content>

        <MainFooter />
      </Layout>
    );
  }
}

export default AuthContainer;
