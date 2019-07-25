import React, { Component } from "react";
import "./App.scss";
import MainContainer from "./MainContainer";
import { initializeIcons } from "@uifabric/icons";
import BackendService from "../../services/holoRepositoryServerService";
import { IPatient, IPractitioner, IPipeline } from "../../../../HoloRepositoryUI-Types";
import { AppContext, IAppState, initialState } from "./AppState";

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

class App extends Component<any, IAppState> {
  constructor(props: any) {
    super(props);
    this.state = {
      ...initialState,
      handlePractitionerChange: this._handlePractitionerChange,
      handlePatientsChange: this._handlePatientsChange,
      handleSelectedPatientIdChange: this._handleSelectedPatientIdChange,
      handlePipelinesChange: this._handlePipelinesChange
    };
  }

  componentDidMount(): void {
    // Note: SMART login is currently not implemented, so a hard-coded practitioner will be the user
    const practitionerId = "b0016666-1924-455d-8b16-92c631fa5207";
    BackendService.getPractitioner(practitionerId).then(practitioner => {
      console.log("Fetched data: practitioner", practitioner);
      this._handlePractitionerChange(practitioner!);
    });

    // Fetch all patients for which the current practitioner is responsible
    BackendService.getAllPatientsForPractitioner(practitionerId).then(patients => {
      console.log("Fetched data: patients", patients);
      this._handlePatientsChange(patients!);
    });

    // Fetch information about available pipelines
    BackendService.getAllPipelines().then(pipelines => {
      console.log("Fetched data: pipelines", pipelines);
      this._handlePipelinesChange(pipelines || []);
    });
  }

  render() {
    return (
      <AppContext.Provider value={this.state}>
        <div className="App">
          <MainContainer />
        </div>
      </AppContext.Provider>
    );
  }

  private _fetchPatientSpecificData = () => {
    this._fetchImagingStudiesForPatients();
    this._fetchHologramsForPatients();
  };

  private _fetchImagingStudiesForPatients = () => {
    const { patients } = this.state;
    if (!patients) return;

    BackendService.getImagingStudiesForAllPatients(patients).then(combinedResult => {
      console.log("Fetched data: imaging studies", combinedResult);
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
      console.log("Fetched data: holograms", combinedResult);
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

  private _handlePatientsChange = (patientsArray?: IPatient[]) => {
    if (!patientsArray) return;

    console.debug(`Received ${patientsArray.length} patients`);
    const patients = patientsArray.reduce(
      (accumulator, patient) => ({ ...accumulator, [patient.pid]: patient }),
      {}
    );
    this.setState({ patients }, this._fetchPatientSpecificData);
  };

  private _handleSelectedPatientIdChange = (pid: string) => {
    this.setState({ selectedPatientId: pid });
  };

  private _handlePipelinesChange = (pipelines: IPipeline[]) => {
    this.setState({ pipelines });
  };
}

export default App;
