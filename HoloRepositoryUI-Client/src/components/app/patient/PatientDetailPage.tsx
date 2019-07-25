import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Persona, PersonaSize } from "office-ui-fabric-react";
import { Col, Divider, Row } from "antd";
import { capitaliseString, getAgeFromDobString } from "../../../util/PatientUtil";
import PlainContentContainer from "../core/PlainContentContainer";
import PatientBreadcrumb from "./PatientBreadcrumb";
import {
  authorCol,
  dateCol,
  fileSizeCol,
  fileTypeCol,
  titleCol
} from "../holograms/HologramsDetailsListColumns";
import HologramsDetailsList from "../holograms/HologramsDetailsList";
import { PropsWithContext, withAppContext } from "../../shared/AppState";

interface IPatientDetailPageProps
  extends RouteComponentProps<{
      pid: string;
    }>,
    PropsWithContext {}

class PatientDetailPage extends Component<IPatientDetailPageProps> {
  render() {
    const { patients, selectedPatientId: pidFromContext } = this.props.context!;

    const patient = patients[pidFromContext || ""];
    if (!patient) {
      // This should never happen
      return <div>"Loading patient..."</div>;
    }

    return (
      <PlainContentContainer>
        <PatientBreadcrumb name={patient.name.full} />

        <Row gutter={16}>
          <Col span={6}>
            <Persona
              imageUrl={patient.pictureUrl ? patient.pictureUrl : undefined}
              text={patient.name.full}
              size={PersonaSize.size72}
              hidePersonaDetails={true}
            />
          </Col>

          <Col span={18}>
            <div>
              <ul>
                <li className="name">Full name: {`${patient.name.title} ${patient.name.full}`}</li>
                <li className="age">Age: {getAgeFromDobString(patient.birthDate)}</li>
                <li className="gender">Gender: {capitaliseString(patient.gender)}</li>
              </ul>
            </div>
          </Col>

          <Divider>Contact details</Divider>

          <ul>
            <li>Phone: {patient.phone}</li>
            <li>Mail: {patient.email}</li>
          </ul>

          <Divider>Holograms</Divider>

          <HologramsDetailsList
            columns={[fileTypeCol, titleCol, dateCol, authorCol, fileSizeCol]}
            showFilters={false}
            patientId={patient.pid}
          />
        </Row>
      </PlainContentContainer>
    );
  }

  componentDidMount() {
    const { handleSelectedPatientIdChange } = this.props.context!;

    // Use pid from URL. If user navigated from patient list, this is redundant. If they navigated
    // to this page manually, it is necessary to keep track of the selected patient.
    handleSelectedPatientIdChange(this.props.pid!);
  }
}

export default withAppContext(PatientDetailPage);
