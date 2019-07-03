import React, { Component, CSSProperties } from "react";
import { Layout } from "antd";

const { Footer } = Layout;

interface IMainFooterProps {
  style: CSSProperties;
}

class MainFooter extends Component<IMainFooterProps> {
  render() {
    return (
      <Footer
        style={{ ...this.props.style, textAlign: "center", color: "#ccc" }}
      >
        © 2019 University College London
        <br />
        <small>
          Built in cooperation with Microsoft and GOSH DRIVE. Source code and
          licence available{" "}
          <a href="https://github.com/nbckr/HoloRepository-Core">on GitHub</a>.
          Icon derived from a work by{" "}
          <a href="https://www.freepik.com/">Freepik</a> from{" "}
          <a href="https://www.flaticon.com/">www.flaticon.com</a>.
        </small>
      </Footer>
    );
  }
}

export default MainFooter;
