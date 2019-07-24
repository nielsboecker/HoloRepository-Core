import React, { Component } from "react";
import "./App.scss";
import MainContainer from "./MainContainer";
import { initializeIcons } from "@uifabric/icons";
import BackendService from "../../services/holoRepositoryServerService";
import { IPractitioner, IPatient } from "../../../../HoloRepositoryUI-Types";

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

export type PidToPatientsMap = Record<string, IPatient>;
export interface IAppState {
  practitioner?: IPractitioner;
  patients?: PidToPatientsMap;
  handlePractitionerChange: Function;
  handlePatientsChange: Function;
}

class App extends Component<any, IAppState> {
  constructor(props: any) {
    super(props);
    this.state = {
      practitioner: undefined,
      patients: {},
      handlePractitionerChange: this._handlePractitionerChange,
      handlePatientsChange: this._handlePatientsChange
    };
  }

  componentDidMount(): void {
    // Note: SMART login is currently not implemented, so a hard-coded practitioner will be the user
    const practitionerId = "b0016666-1924-455d-8b16-92c631fa5207";
    BackendService.getPractitioner(practitionerId).then(practitioner => {
      console.log("practitioner", practitioner);
      this._handlePractitionerChange(practitioner!);
    });

    // Load all patients for which the current practitioner is responsible
    BackendService.getAllPatientsForPractitioner(practitionerId).then(patients => {
      console.log("patients", patients);
      this._handlePatientsChange(patients!);
    });
  }

  render() {
    return (
      <div className="App">
        <MainContainer />
      </div>
    );
  }

  private _fetchImagingStudiesForPatients = () => {
    const { patients } = this.state;
    if (!patients) return;

    BackendService.getImagingStudiesForAllPatients(patients).then(combinedResult => {
      for (const pid in combinedResult) {
        const studies = combinedResult[pid];
        const patient = patients[pid];
        patient.imagingStudies = studies;
        this.setState({
          patients: {
            ...patients,
            [pid]: patient
          }
        });
      }
    });
  };

  private _fetchHologramsForPatients = () => {
    // Note: Similar with _fetchImagingStudiesForPatients, should be refactored
    const { patients } = this.state;
    if (!patients) return;

    BackendService.getHologramsForAllPatients(patients).then(combinedResult => {
      for (const pid in combinedResult) {
        const holograms = combinedResult[pid];
        const patient = patients[pid];
        patient.holograms = holograms;
        this.setState({
          patients: {
            ...patients,
            [pid]: patient
          }
        });
      }
    });
  };

  private _handlePractitionerChange = (practitioner: IPractitioner) => {
    this.setState({ practitioner });
  };

  private _fetchPatientSpecificData = () => {
    this._fetchImagingStudiesForPatients();
    this._fetchHologramsForPatients();
  };

  private _handlePatientsChange = (patientsFlat?: IPatient[]) => {
    if (!patientsFlat) return;

    console.debug(`Received ${patientsFlat.length} patients`);
    const patients = patientsFlat.reduce(
      (accumulator, patient) => ({ ...accumulator, [patient.pid]: patient }),
      {}
    );
    this.setState({ patients }, this._fetchPatientSpecificData);
  };
}

export default App;
