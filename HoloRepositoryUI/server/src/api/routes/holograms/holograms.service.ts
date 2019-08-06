import AccesorClient from "../../../common/clients/HoloStorageAccesorClient";
import logger from "../../../common/logger";
import { IHologram } from "../../../../../types";

export class HologramsService {
  public getAllForPatients(pids: string): Promise<Record<string, IHologram[]> | void> {
    logger.info(`GET all Holograms for pids = '${pids}'`);
    return AccesorClient.get<Record<string, IHologram[]>>("/", { pid: pids });
  }

  public downloadById(hid: string): Promise<BinaryType | string> {
    // TODO: Implement
    logger.warn("Download not implemented yet", hid);
    return Promise.resolve("<holo-file>");
  }

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
