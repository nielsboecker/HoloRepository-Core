import logger from "../../../common/logger";
import { IPractitioner } from "../../../../../types";
import FhirClient, { SupportedFhirResourceType } from "../../../common/clients/fhirClient";
import { R4 } from "@ahryman40k/ts-fhir-types";

export class PractitionersService {
  public getById(pid: string): Promise<IPractitioner> {
    logger.info(`GET Practitioner by id '${pid}'`);
    return FhirClient.getAndMap<R4.IPractitioner, IPractitioner>(
      SupportedFhirResourceType.Practitioner,
      pid
    );
  }
}

export default new PractitionersService();
