import React, { Component } from "react";
import { Icon, Persona, PersonaSize } from "office-ui-fabric-react";
import { Col, Row } from "antd";
import { navigate } from "@reach/router";
import {
  capitaliseString,
  getAgeFromDobString,
  getNumberOfHologramsString
} from "../../../util/PatientUtil";
import "./PatientCard.scss";
import { IPatient } from "../../../../../types";
import { PropsWithContext, withAppContext } from "../../shared/AppState";

export interface IPatientCardProps extends PropsWithContext {
  patient: IPatient;
}

class PatientCard extends Component<IPatientCardProps, object> {
  render() {
    const { patient } = this.props;

    return (
      <div className="PatientCard" data-is-focusable={true} onClick={this._handleClick}>
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
                <li className="age">Age: {getAgeFromDobString(patient.birthDate)}</li>
                <li className="gender">Gender: {capitaliseString(patient.gender)}</li>
                <li className="numberOfHolograms">
                  {getNumberOfHologramsString(patient.holograms)}
                </li>
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

  private _handleClick = () => {
    let pid = this.props.patient.pid;
    this.props.context!.handleSelectedPatientIdChange(pid);
    navigate(`/app/patients/${pid}`);
  };
}

export default withAppContext(PatientCard);
