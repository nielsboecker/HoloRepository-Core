from enum import Enum


class JobStatus(Enum):
    STARTJOB = 1
    PPREPROCESSING = 2
    MODELGENERATION = 3
    MODELCONVERSION = 4
    FINISHED = 5
