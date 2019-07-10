import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Persona, PersonaSize } from "office-ui-fabric-react/lib-commonjs";
import { Col, Divider, Row } from "antd";
import { capitaliseString, getAgeFromDobString } from "../../../util/PatientUtil";
import PlainContentContainer from "../core/PlainContentContainer";
import PatientBreadcrumb from "./PatientBreadcrumb";
import { IPatient } from "../../../types";
import {
  authorCol,
  dateCol,
  fileSizeCol,
  fileTypeCol,
  titleCol
} from "../holograms/HologramsDetailsListColumns";

import samplePatients from "../../../__tests__/samples/samplePatients.json";
import samplePatientsWithHolograms from "../../../__tests__/samples/samplePatientsWithHolograms.json";
import HologramsDetailsList from "../holograms/HologramsDetailsList";

const allSamplePatients = [...samplePatients, ...samplePatientsWithHolograms] as IPatient[];

interface IPatientDetailPageProps
  extends RouteComponentProps<{
    id: string;
  }> {}

class PatientDetailPage extends Component<IPatientDetailPageProps> {
  patient: IPatient | undefined = allSamplePatients.find(patient => patient.id === this.props.id);

  render() {
    if (!this.patient) throw new Error("No patient (only in dev prototype)");

    return (
      <PlainContentContainer>
        <PatientBreadcrumb name={this.patient.name.full} />

        <Row gutter={16}>
          <Col span={6}>
            <Persona
              imageUrl={this.patient.pictureUrl ? this.patient.pictureUrl : undefined}
              text={this.patient.name.full}
              size={PersonaSize.size72}
              hidePersonaDetails={true}
            />
          </Col>

          <Col span={18}>
            <div>
              <ul>
                <li className="name">
                  Full name: {`${this.patient.name.title} ${this.patient.name.full}`}
                </li>
                <li className="age">Age: {getAgeFromDobString(this.patient.dateOfBirth)}</li>
                <li className="gender">Gender: {capitaliseString(this.patient.gender)}</li>
              </ul>
            </div>
          </Col>

          <Divider>Contact details</Divider>

          <ul>
            <li>Phone: {this.patient.phone}</li>
            <li>Mail: {this.patient.email}</li>
          </ul>

          <Divider>Holograms</Divider>

          <HologramsDetailsList
            columns={[fileTypeCol, titleCol, dateCol, authorCol, fileSizeCol]}
            showFilters={false}
            patientId={this.patient.id}
          />
        </Row>
      </PlainContentContainer>
    );
  }
}

export default PatientDetailPage;
