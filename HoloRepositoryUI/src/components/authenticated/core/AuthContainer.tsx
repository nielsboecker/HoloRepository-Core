import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Layout } from "antd";
import MenuHeader from "./MenuHeader";
import MainFooter from "../../core/MainFooter";
import ContentContainer from "./ContentContainer";

class AuthContainer extends Component<RouteComponentProps> {
  render() {
    return (
      <Layout>
        <MenuHeader />

        <Layout.Content style={{ padding: "0 50px", marginTop: "50px" }}>
          <ContentContainer>{this.props.children}</ContentContainer>
        </Layout.Content>

        <MainFooter />
      </Layout>
    );
  }
}

export default AuthContainer;
