import numpy as np
import datetime
import multiprocessing as mp


def _dummy1(n):
    """
    This is a dummy function used to test multiprocessing.
    It displays the start second and end second of the function

    """

    now1 = datetime.datetime.now()
    milisec1 = now1.microsecond/1000.0
    print '_dummy1 started at %d seconds' % now1.second, '%f miliseconds' % milisec1
    A = np.ones([n, n])
    B = np.ones([n, n])
    C = A*B
    now2 = datetime.datetime.now()
    milisec2 = now2.microsecond/1000.0
    print '_dummy1 finished at %d seconds' % now2.second, '%f miliseconds' % milisec2


def _dummy2(n):
    """
    This is a dummy function used to test multiprocessing.
    It displays the start time of the function

    """

    now3 = datetime.datetime.now()
    milisec3 = now3.microsecond/1000.0
    print '_dummy2 started at %d seconds and' % now3.second, '%f miliseconds' % milisec3
    A = np.ones([n, n])
    B = np.ones([n, n])
    C = A*B
    now4 = datetime.datetime.now()
    milisec4 = now4.microsecond/1000.0
    print '_dummy2 finished at %d seconds and' % now4.second, '%f miliseconds' % milisec4


def _multiprocessing(function1, n, function2, m):
    """
    This function takes 2 functions as inputs and runs them in parallel

    """

    print 'Started parallel processing'

    pool = mp.Pool()
    result1 = pool.apply_async(function1, [n])    # evaluate "solve1(A)" asynchronously
    result2 = pool.apply_async(function2, [m])    # evaluate "solve2(B)" asynchronously
    answer1 = result1.get(timeout=10)
    answer2 = result2.get(timeout=10)

    print 'Finished parallel processing'

_multiprocessing(_dummy1, 100, _dummy2, 1000)

# if __name__ == '__main__':
#     p1 = mp.Process(target=_dummy1(100))
#     p1.start()
#     p2 = mp.Process(target=_dummy2(1000))
#     p2.start()
#     p1.join()
#     p2.join()

# pool = mp.Pool()
# result1 = pool.apply_async(_dummy1, [100])
# result2 = pool.apply_async(_dummy2, [1000])
# answer1 = result1.get(timeout=10)
# answer2 = result2.get(timeout=10)



