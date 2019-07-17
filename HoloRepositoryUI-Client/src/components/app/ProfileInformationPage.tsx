import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Persona, PersonaSize } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import PlainContentContainer from "./core/PlainContentContainer";
import { capitaliseString, getAgeFromDobString } from "../../util/PatientUtil";
import { IPractitioner } from "../../../../HoloRepositoryUI-Types";

import samplePractitioner from "../../__tests__/samples/samplePractitioner.json";

class ProfileInformationPage extends Component<RouteComponentProps> {
  practitioner = samplePractitioner as IPractitioner;

  render() {
    return (
      <PlainContentContainer>
        <Row gutter={16}>
          <Col span={6}>
            <Persona
              imageUrl={this.practitioner.pictureUrl ? this.practitioner.pictureUrl : undefined}
              text={this.practitioner.name.full}
              size={PersonaSize.size72}
              hidePersonaDetails={true}
            />
          </Col>

          <Col span={18}>
            <div>
              <ul>
                <li className="name">
                  Full name: {`${this.practitioner.name.title} ${this.practitioner.name.full}`}
                </li>
                <li className="age">Age: {getAgeFromDobString(this.practitioner.birthDate)}</li>
                <li className="gender">Gender: {capitaliseString(this.practitioner.gender)}</li>
              </ul>
            </div>
          </Col>

          <Divider>Contact details</Divider>

          <ul>
            <li>Phone: {this.practitioner.phone}</li>
            <li>Mail: {this.practitioner.email}</li>
          </ul>
        </Row>
      </PlainContentContainer>
    );
  }
}

export default ProfileInformationPage;
