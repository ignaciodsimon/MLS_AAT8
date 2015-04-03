import numpy as np
import datetime
import multiprocessing as mp


def _dummy1(n, p, o, t):
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
    print p, o, t

def _dummy2(n, p, o):
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
   print p, o


# def _multiprocessing(function1, f1arg1, f1arg2, f1arg3, f1arg4, function2, f2arg1, f2arg2, f2arg3, f2arg4):
#     """
#     This function takes 2 functions as inputs and runs them in parallel
#
#     """
#
#     print 'Started parallel processing'
#
#     pool = mp.Pool()
#     # evaluate "function1(f1arg1, f1arg2, f1arg3, f1arg4)" asynchronously
#     result1 = pool.apply_async(function1, [f1arg1, f1arg2, f1arg3, f1arg4])

#     # evaluate "function2(f2arg1, f2arg2, f2arg3, f2arg4)" asynchronously
#     result2 = pool.apply_async(function2, [f2arg1, f2arg2, f2arg3, f2arg4])
#     answer1 = result1.get()
#     answer2 = result2.get()
#
#     print 'Finished parallel processing'

def _multiprocessing(function1, f1args, function2, f2args):
    """
    This function takes 2 functions as inputs and runs them in parallel
    It should be used as following:
    _multiprocessing(function1, f1args, function2, f2args) where
    function1 is the first function,
    f1args is a vector containing the arguments to be passed to function1
    function2 is the second function,
    f2args is a vector containing the arguments to be passed to function2

    """

    print 'Started parallel processing'

    pool = mp.Pool()
    result1 = pool.apply_async(function1, f1args) # evaluate "function1(f1arg1, f1arg2, f1arg3, f1arg4)" asynchronously
    result2 = pool.apply_async(function2, f2args) # evaluate "function2(f2arg1, f2arg2, f2arg3, f2arg4)" asynchronously
    answer1 = result1.get()
    answer2 = result2.get()

    print 'Finished parallel processing'

_dummy1args = [100, 1, 1, 1]
_dummy2args = [1000, 2, 2]

_multiprocessing(_dummy1, _dummy1args, _dummy2, _dummy2args)

