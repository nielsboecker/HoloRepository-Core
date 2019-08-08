import AccessorClient from "../../../common/clients/HoloStorageAccesorClient";
import PipelinesClient from "../../../common/clients/HoloPipelinesClient";
import logger from "../../../common/logger";

export class HologramsService {
  public getAllForPatientsURL(pids: string): string {
    logger.info(`GET all Holograms for pids = '${pids}'`);
    return AccessorClient.getAllForPatientsURL(pids);
  }

  public getDownloadURL = (hid: string): string => {
    logger.info(`GET download hologram for pid = '${hid}'`);
    return AccessorClient.getDownloadURL(hid);
  };

  public getEndpointURL = (hid: string): string => {
    logger.info(`GET hologram endpoint for hid = '${hid}'`);
    return AccessorClient.getEndpointURL(hid);
  };

  public getBaseURL = (): string => {
    return AccessorClient.getBaseURL();
  };

  public getPipelineJobURL = (): string => {
    return PipelinesClient.getJobURL();
  };
}

export default new HologramsService();
