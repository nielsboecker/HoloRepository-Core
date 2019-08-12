import PipelinesClient from "../../../common/clients/HoloPipelinesClient";

export class PipelinesService {
  public getJobURL = (): string => {
    return PipelinesClient.getJobURL();
  };

  public getJobStatusURL = (jid: string): string => {
    return PipelinesClient.getJobStatusURL(jid);
  };

  public getPipelinesURL = (): string => {
    return PipelinesClient.getPipelinesURL();
  };
}

export default new PipelinesService();
