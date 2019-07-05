import React, { Component } from "react";
import { Icon } from "office-ui-fabric-react/lib-commonjs/Icon";
import { PersonaSize, Persona } from "office-ui-fabric-react/lib-commonjs";
import { Row, Col } from "antd";
import { Link } from "@reach/router";
import { IHologram, IPatient } from "../../../types";
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
                  <li className="age">Age: {PatientCard._getAge(patient.dateOfBirth)}</li>
                  <li className="gender">Gender: {PatientCard._capitalize(patient.gender)}</li>
                  <li className="numberOfHolograms">
                    {PatientCard._getNumberOfHologramsLabel(patient.holograms)}
                  </li>
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

  static _capitalize(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  static _getAge(dobString: string) {
    const dateOfBirth = new Date(dobString);
    const ageDiffMs = Date.now() - dateOfBirth.getTime();
    const ageDate = new Date(ageDiffMs); // milliseconds from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
  }

  static _getNumberOfHologramsLabel(holograms?: IHologram[] | undefined) {
    const numOfHolograms: number | string =
      holograms && holograms.length >= 1 ? holograms.length : "No";
    return `${numOfHolograms} hologram${numOfHolograms != 1 ? "s" : ""} available`;
  }
}
