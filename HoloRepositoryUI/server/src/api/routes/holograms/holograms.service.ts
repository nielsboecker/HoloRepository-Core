import logger from "../../../common/logger";
import { IHologram } from "../../../../../HoloRepositoryUI-Types";

import sampleHolograms from "../../../__tests__/samples/internal/sampleHolograms.json";

const _sampleHolograms = sampleHolograms as IHologram[];

// Note: This will have to remain mocked until HoloStorage API endpoints are ready

export class HologramsService {
  public getAll(): Promise<IHologram[]> {
    logger.info("GET all Holograms");
    return Promise.resolve(_sampleHolograms);
  }

  public getAllForPatient(pid: string) {
    logger.info(`GET all Holograms for pid = '${pid}'`);
    return Promise.resolve(_sampleHolograms);
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
