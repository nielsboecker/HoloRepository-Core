import logger from "../../../common/logger";
import { IHologram } from "../../../../../HoloRepositoryUI-Types";

import sampleHolograms from "../../../__tests__/samples/sampleHolograms.json";
import { Request, Response } from "express";

const _sampleHolograms = sampleHolograms as IHologram[];

export class HologramsService {
  public getAll(): Promise<IHologram[]> {
    logger.info("GET all Holograms");
    return Promise.resolve(_sampleHolograms);
  }

  public getById(hid: string): Promise<IHologram> {
    logger.info(`GET Hologram by id '${hid}'`);
    const hologram = _sampleHolograms.find(hologram => hologram.hid === hid);
    if (hologram) {
      return Promise.resolve(hologram);
    }
  }

  public downloadById(hid: string): Promise<BinaryType | string> {
    // TODO: Implement
    logger.warn("Download not implemented yet");
    return Promise.resolve("<holo-file>");
  }

  public deleteById(hid: string): Promise<boolean> {
    // TODO: Implement
    logger.warn("Delete not implemented yet");
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