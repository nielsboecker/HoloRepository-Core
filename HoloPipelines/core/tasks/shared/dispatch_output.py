"""
This module contains a function to dispatch the pipeline output so a consumer.
"""

from core.clients.holostorage_accessor import send_file_request_to_accessor


def dispatch_output(job_id: str, plid: str, medical_data: dict) -> None:
    send_file_request_to_accessor(job_id, plid, medical_data)
