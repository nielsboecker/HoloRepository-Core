import logger from "../../common/logger";
import { IHologram } from "../../../../HoloRepositoryUI-Types";

import sampleHolograms from "../../../test/samples/sampleHolograms.json";

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
}

export default new HologramsService();
