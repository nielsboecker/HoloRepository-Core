import React from "react";
import { shallow } from "enzyme";
import { Selection } from "office-ui-fabric-react";

import AppContainer from "../../components/app/core/AppContainer";
import MenuHeader from "../../components/app/core/MenuHeader";
import ContentContainer from "../../components/app/core/ContentContainer";
import FilterStatusMessageBar from "../../components/app/core/FilterStatusMessageBar";
import PlainContentContainer from "../../components/app/core/PlainContentContainer";
import DeviceConnectorPage from "../../components/app/DeviceConnectorPage";
import HologramsCommandBar from "../../components/app/holograms/HologramsCommandBar";
import HologramsDetailsList from "../../components/app/holograms/HologramsDetailsList";
import HologramsListPage from "../../components/app/holograms/HologramsListPage";
import GenerationProcessingStep from "../../components/app/new_hologram/generate/GenerationProcessingStep";
import ImagingStudyDetailsCard from "../../components/app/new_hologram/generate/ImagingStudyDetailsCard";
import ImagingStudySelectionStep from "../../components/app/new_hologram/generate/ImagingStudySelectionStep";
import PipelineSelectionStep from "../../components/app/new_hologram/generate/PipelineSelectionStep";
import PipelineSpecificationCard from "../../components/app/new_hologram/generate/PipelineSpecificationCard";
import NewHologramPage from "../../components/app/new_hologram/NewHologramPage";
import CreationModeSelectionStep from "../../components/app/new_hologram/shared/CreationModeSelectionStep";
import DetailsDeclarationStep from "../../components/app/new_hologram/shared/DetailsDeclarationStep";
import ExtendedChoiceGroupLabel from "../../components/app/new_hologram/shared/ExtendedChoiceGroupLabel";
import NewHologramControlsAndProgress from "../../components/app/new_hologram/shared/NewHologramControlsAndProgress";
import FileUploadStep from "../../components/app/new_hologram/upload/FileUploadStep";
import UploadProcessingStep from "../../components/app/new_hologram/upload/UploadProcessingStep";
import PatientBreadcrumb from "../../components/app/patient/PatientBreadcrumb";
import PatientDetailPage from "../../components/app/patient/PatientDetailPage";
import PatientCard from "../../components/app/patients/PatientCard";
import PatientCardsList from "../../components/app/patients/PatientCardsList";
import PatientListPage from "../../components/app/patients/PatientListPage";
import PipelineDetailBox from "../../components/app/PipelineDetailBox";
import ProfileInformationPage from "../../components/app/ProfileInformationPage";
import { IPatient } from "../../../../types";
import { mountWithContextProvider } from "../../__test_utils__/MockContextProvider";

import samplePatients from "../samples/samplePatients.json";

it("renders AppContainer without crashing", () => {
  mountWithContextProvider(<AppContainer />);
});

it("renders ContentContainer without crashing", () => {
  shallow(<ContentContainer title="" description={[""]} />);
});

it("renders FilterStatusMessageBar without crashing", () => {
  shallow(<FilterStatusMessageBar totalCount={0} filteredCount={0} />);
});

it("renders MenuHeader without crashing", () => {
  mountWithContextProvider(<MenuHeader />);
});

it("renders PlainContentContainer without crashing", () => {
  shallow(<PlainContentContainer />);
});

it("renders DeviceConnectorPage without crashing", () => {
  shallow(<DeviceConnectorPage />);
});

it("renders HologramsCommandBar without crashing", () => {
  mountWithContextProvider(<HologramsCommandBar selection={new Selection()} />);
});

it("renders HologramsDetailsList without crashing", () => {
  mountWithContextProvider(<HologramsDetailsList showFilters={false} />);
});

it("renders HologramsListPage without crashing", () => {
  shallow(<HologramsListPage />);
});

it("renders GenerationProcessingStep without crashing", () => {
  shallow(<GenerationProcessingStep onComponentDidMount={jest.fn()} />);
});

it("renders ImagingStudyDetailsCard without crashing", () => {
  shallow(<ImagingStudyDetailsCard />);
});

it("renders ImagingStudySelectionStep without crashing", () => {
  mountWithContextProvider(<ImagingStudySelectionStep onSelectedImagingStudyChange={jest.fn()} />);
});

it("renders PipelineSelectionStep without crashing", () => {
  mountWithContextProvider(<PipelineSelectionStep onPipelineSelectionChange={jest.fn()} />);
});

it("renders PipelineSpecificationCard without crashing", () => {
  shallow(<PipelineSpecificationCard />);
});

it("renders NewHologramPage without crashing", () => {
  mountWithContextProvider(<NewHologramPage />);
});

it("renders CreationModeSelectionStep without crashing", () => {
  shallow(
    <CreationModeSelectionStep
      selected={jest.requireMock("../../../../types")}
      handleModeChange={jest.fn}
    />
  );
});

it("renders DetailsDeclarationStep without crashing", () => {
  mountWithContextProvider(<DetailsDeclarationStep />);
});

it("renders ExtendedChoiceGroupLabel without crashing", () => {
  shallow(<ExtendedChoiceGroupLabel title="" description="" iconName="" />);
});

it("renders NewHologramControlsAndProgress without crashing", () => {
  shallow(
    <NewHologramControlsAndProgress
      onGoToPrevious={jest.fn}
      onGoToNext={jest.fn}
      steps={[]}
      current={0}
    />
  );
});

it("renders FileUploadStep without crashing", () => {
  shallow(<FileUploadStep onHologramFileChange={jest.fn()} />);
});

it("renders UploadProcessingStep without crashing", () => {
  shallow(<UploadProcessingStep onComponentDidMount={jest.fn()} />);
});

it("renders PatientBreadcrumb without crashing", () => {
  shallow(<PatientBreadcrumb name="" />);
});

it("renders PatientDetailPage without crashing", () => {
  mountWithContextProvider(<PatientDetailPage />);
});

it("renders PatientCard without crashing", () => {
  const patient = samplePatients[0] as IPatient;
  shallow(<PatientCard patient={patient} />);
});

it("renders PatientCardsList without crashing", () => {
  mountWithContextProvider(<PatientCardsList />);
});

it("renders PatientListPage without crashing", () => {
  shallow(<PatientListPage />);
});

it("renders PipelineDetailBox without crashing", () => {
  shallow(<PipelineDetailBox />);
});

it("renders ProfileInformationPage without crashing", () => {
  mountWithContextProvider(<ProfileInformationPage />);
});
