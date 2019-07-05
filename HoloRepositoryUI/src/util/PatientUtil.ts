import { IHologram } from "../types";

const capitaliseString = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

const getAgeFromDobString = (dobString: string) => {
  const dateOfBirth = new Date(dobString);
  const ageDiffMs = Date.now() - dateOfBirth.getTime();
  const ageDate = new Date(ageDiffMs); // milliseconds from epoch
  return Math.abs(ageDate.getUTCFullYear() - 1970);
};

const getNumberOfHolograms = (holograms?: IHologram[] | undefined) => {
  const numOfHolograms: number | string =
    holograms && holograms.length >= 1 ? holograms.length : "No";
  return `${numOfHolograms} hologram${numOfHolograms != 1 ? "s" : ""} available`;
};

export { capitaliseString, getAgeFromDobString, getNumberOfHolograms };
