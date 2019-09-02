import PipelinesClient from "../../../common/clients/HoloPipelinesClient";

export class PipelinesService {
  public getJobsURL = (): string => {
    return PipelinesClient.getJobsURL();
  };

  public getJobStateURL = (jid: string): string => {
    return PipelinesClient.getJobStateURL(jid);
  };

  public getJobLogURL = (jid: string): string => {
    return PipelinesClient.getJobLogURL(jid);
  };

  public getPipelinesURL = (): string => {
    return PipelinesClient.getPipelinesURL();
  };
}

export default new PipelinesService();
