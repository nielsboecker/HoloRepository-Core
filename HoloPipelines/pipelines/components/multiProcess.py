from testing import testing
from multiprocessing import Process


def testMul(a, b):
    p = Process(target=testing, args=(*[a, b]))
    return p
