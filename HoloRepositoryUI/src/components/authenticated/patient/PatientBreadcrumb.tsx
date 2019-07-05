import React, { Component } from "react";
import { Breadcrumb, IBreadcrumbItem } from "office-ui-fabric-react/lib-commonjs/Breadcrumb";
import { navigate } from "@reach/router";

export interface IPatientBreadcrumbProps {
  name: string;
}

export default class PatientBreadcrumb extends Component<IPatientBreadcrumbProps> {
  render() {
    return (
      <div>
        <Breadcrumb
          items={[
            {
              text: "Your patients",
              key: "patients",
              onClick: () => navigate("/app/patients")
            },
            {
              text: this.props.name,
              key: "currentPatient",
              onClick: this._onBreadcrumbItemClicked,
              isCurrentItem: true
            }
          ]}
          ariaLabel={`Selected patient ${this.props.name} from your patients`}
          styles={{ root: { margin: "0 0 2rem 0" } }}
        />
      </div>
    );
  }

  private _onBreadcrumbItemClicked = (
    ev?: React.MouseEvent<HTMLElement>,
    item?: IBreadcrumbItem
  ): void => {
    console.log(`Breadcrumb item has been clicked.`);
  };
}
