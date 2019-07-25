import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Persona, PersonaSize } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import PlainContentContainer from "./core/PlainContentContainer";
import { capitaliseString, getAgeFromDobString } from "../../util/PatientUtil";
import { PropsWithContext, withAppContext } from "../shared/AppState";

class ProfileInformationPage extends Component<RouteComponentProps & PropsWithContext> {

  render() {
    const practitioner = this.props.context!.practitioner!;

    return (
      <PlainContentContainer>
        <Row gutter={16}>
          <Col span={6}>
            <Persona
              imageUrl={practitioner.pictureUrl ? practitioner.pictureUrl : undefined}
              text={practitioner.name.full}
              size={PersonaSize.size72}
              hidePersonaDetails={true}
            />
          </Col>

          <Col span={18}>
            <div>
              <ul>
                <li className="name">
                  Full name: {`${practitioner.name.title} ${practitioner.name.full}`}
                </li>
                <li className="age">Age: {getAgeFromDobString(practitioner.birthDate)}</li>
                <li className="gender">Gender: {capitaliseString(practitioner.gender)}</li>
              </ul>
            </div>
          </Col>

          <Divider>Contact details</Divider>

          <ul>
            <li>Phone: {practitioner.phone || "Unknown"}</li>
            <li>Mail: {practitioner.email || "Unknown"}</li>
          </ul>
        </Row>
      </PlainContentContainer>
    );
  }
}

export default withAppContext(ProfileInformationPage);
