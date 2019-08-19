from core.clients.holostorage_accessor import send_file_request_to_accessor


def dispatch_output(meta_data):
    send_file_request_to_accessor(meta_data)
