import PipelinesClient from "../../../common/clients/HoloPipelinesClient";

export class PipelinesService {
  public getJobsURL = (): string => {
    return PipelinesClient.getJobsURL();
  };

  public getJobStatusURL = (jid: string): string => {
    return PipelinesClient.getJobStatusURL(jid);
  };

  public getPipelinesURL = (): string => {
    return PipelinesClient.getPipelinesURL();
  };
}

export default new PipelinesService();
