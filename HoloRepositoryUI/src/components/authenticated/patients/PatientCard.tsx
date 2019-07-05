import React, { Component } from "react";
import { Gender, IPatient } from "../../../types";
import { DocumentCard } from "office-ui-fabric-react";
import { Row, Col } from "antd";
import { Icon } from "office-ui-fabric-react/lib-commonjs/Icon";
import {
  ImageFit,
  Image,
  PersonaSize,
  PersonaPresence,
  Persona
} from "office-ui-fabric-react/lib-commonjs";
import "./PatientCard.scss";

export interface IPatientCardProps {
  patient: IPatient;
}

/**
 * id: string,
 name: string,
 gender: Gender,
 age: number,
 pictureUrl?: string
 */

export default class PatientCard extends Component<IPatientCardProps, object> {
  render() {
    const { patient } = this.props;

    {
      /*<DocumentCard
        onClickHref={`/app/patient/${patient.id}`}
      >
        <h2>{patient.name.full}</h2>
        <p>bla</p>
        <p>bla</p>
        <p>bla</p>d

      </DocumentCard>*/
    }

    return (
      <div className="PatientCard" data-is-focusable={true}>
        <Row gutter={16}>
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
              <h2>{patient.name.full}</h2>
              <p>{patient.id}</p>

              <ul>
                <li>Age: 12</li>
                <li>Gender: male</li>
                <li>3 holograms available</li>
              </ul>
            </div>
          </Col>

          <Col span={2}>
            <Icon iconName="ChevronRight" />
          </Col>
        </Row>
      </div>
    );
  }
}
