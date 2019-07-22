import { IHologram, IImagingStudySeries } from "../../../../HoloRepositoryUI-Types";

const getConditionalPidsFilter = ({ pids }): ((v: IHologram | IImagingStudySeries) => boolean) => {
  if (pids) {
    const _pids: string[] = pids.split(",");
    return value => _pids.includes(value.subject.pid);
  } else {
    return value => true;
  }
};

export default getConditionalPidsFilter;
