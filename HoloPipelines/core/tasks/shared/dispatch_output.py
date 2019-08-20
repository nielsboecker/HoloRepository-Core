from core.clients.holostorage_accessor import send_file_request_to_accessor


def dispatch_output(job_id: str, plid: str, medical_data: dict):
    send_file_request_to_accessor(job_id, plid, medical_data)
