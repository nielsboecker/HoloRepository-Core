from enum import Enum


# TODO: Refactor this whole thing
# TODO: when using for update_job, pass the enum not the sting value
# TODO: sort them to be chronological


class JobStatus(Enum):
    STARTING = 1
    PREPROCESSING = 2
    GENERATING_MODEL = 3
    CONVERTING_MODEL = 4
    FINISHED = 5
    FETCHING_DATA = 6
