import React, { Component } from "react";
import { Layout } from "antd";

const { Footer } = Layout;

class MainFooter extends Component {
  render() {
    return <Footer style={{ textAlign: "center" }}>©2019 UCL</Footer>;
  }
}

export default MainFooter;
