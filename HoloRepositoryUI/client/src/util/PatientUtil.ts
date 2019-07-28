import { IHologram } from "../../../types";

const capitaliseString = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

const getAgeFromDobString = (dobString?: string): number | string => {
  if (!dobString) {
    return "Unknown";
  }
  const birthDate = new Date(dobString);
  const ageDiffMs = Date.now() - birthDate.getTime();
  const ageDate = new Date(ageDiffMs); // milliseconds from epoch
  return Math.abs(ageDate.getUTCFullYear() - 1970);
};

const getNumberOfHologramsString = (holograms?: IHologram[] | undefined) => {
  const numOfHolograms: number | string =
    holograms && holograms.length >= 1 ? holograms.length : "No";
  return `${numOfHolograms} hologram${numOfHolograms !== 1 ? "s" : ""} available`;
};

export { capitaliseString, getAgeFromDobString, getNumberOfHologramsString };
