# Use a python manager dict to share across processes. Note that this is a bit of a
# misuse, as typically the reference to the variable would be explicitly handed to all
# processes. But this works, and it's not critical; also this way is much more readable.

# Initialise the status in the module's __init__ to prevent that a pipeline, which runs
# as a worker process, is the first to import this module. That would lead to the
# global state variable being initialised by that process, and the Manager() would
# spawn off another child process of that daemon.
from multiprocessing import Manager
import logging

jobs_status = Manager().dict()

logging.basicConfig(level=logging.INFO)
logging.info("Initialised global state")
