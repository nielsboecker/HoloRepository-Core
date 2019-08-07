import AccessorClient from "../../../common/clients/HoloStorageAccesorClient";
import logger from "../../../common/logger";
import { IHologram } from "../../../../../types";

export class HologramsService {
  public getAllForPatients(pids: string): Promise<Record<string, IHologram[]> | void> {
    logger.info(`GET all Holograms for pids = '${pids}'`);
    return AccessorClient.getJson<Record<string, IHologram[]>>("/", { pid: pids });
  }

  public getDownloadURL = (hid: string): string => {
    logger.info(`GET download hologram for pid = '${hid}'`);
    return AccessorClient.getDownloadURL(hid);
  };

  public deleteById(hid: string): Promise<boolean> {
    // TODO: Implement
    logger.warn("Delete not implemented yet", hid);
    return Promise.resolve(true);
  }

  public upload(): Promise<boolean> {
    // TODO: Implement
    logger.warn("Upload not implemented yet");
    return Promise.resolve(true);
  }

  public generate(): Promise<boolean> {
    // TODO: Generate
    logger.warn("Generate not implemented yet");
    return Promise.resolve(true);
  }
}

export default new HologramsService();
