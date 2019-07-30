import { IHologram, IImagingStudy } from "../../../../HoloRepositoryUI-Types";

/**
 * This queries all data and filters afterwards. Instead, FHIR queries should be built such
 * that the server filters the data and only returns relevant resources in the first place.
 * @deprecated
 */
const getConditionalPidsFilter = ({ pids }): ((v: IHologram | IImagingStudy) => boolean) => {
  if (pids) {
    const _pids: string[] = pids.split(",");
    return value => _pids.includes(value.subject.pid);
  } else {
    return () => true;
  }
};

export default getConditionalPidsFilter;
