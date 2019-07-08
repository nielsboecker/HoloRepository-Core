import React, { Component } from "react";
import { Icon } from "office-ui-fabric-react/lib-commonjs/Icon";
import { PersonaSize, Persona } from "office-ui-fabric-react/lib-commonjs";
import { Row, Col } from "antd";
import { Link } from "@reach/router";
import { IPatient } from "../../../types";
import {
  capitaliseString,
  getAgeFromDobString,
  getNumberOfHolograms
} from "../../../util/PatientUtil";
import "./PatientCard.scss";

export interface IPatientCardProps {
  patient: IPatient;
}

export default class PatientCard extends Component<IPatientCardProps, object> {
  render() {
    const { patient } = this.props;

    return (
      <div className="PatientCard" data-is-focusable={true}>
        <Link to={`/app/patient/${patient.id}`}>
          <Row gutter={16} type="flex" align="middle">
            <Col span={3}>
              <Persona
                imageUrl={patient.pictureUrl ? patient.pictureUrl : undefined}
                text={patient.name.full}
                size={PersonaSize.size48}
                hidePersonaDetails={true}
              />
            </Col>

            <Col span={19}>
              <div>
                <h3 className="name">{patient.name.full}</h3>

                <ul>
                  <li className="age">Age: {getAgeFromDobString(patient.dateOfBirth)}</li>
                  <li className="gender">Gender: {capitaliseString(patient.gender)}</li>
                  <li className="numberOfHolograms">{getNumberOfHolograms(patient.holograms)}</li>
                </ul>
              </div>
            </Col>

            <Col span={2}>
              <Icon iconName="ChevronRight" />
            </Col>
          </Row>
        </Link>
      </div>
    );
  }
}
