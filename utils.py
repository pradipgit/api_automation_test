import requests
import json
import time
import select
import string
import random
import sys
import os
import fnmatch
import logging
import base64
logger = logging.getLogger("Test Run")

def print_test_results(passed, test_name):
    if passed:
        print ('**********************************')
        print ('    %s TEST PASSED' % test_name)
        print ('**********************************')
    else:
        print ('**********************************')
        print ('    %s TEST FAILED' % test_name)
        print ('**********************************')

def assignOrder(order):
        def do_assignment(to_func):
            to_func.order = order
            return to_func
        return do_assignment

def run_test_cases(class_obj):
    global TotalTests
    global TotalPassed
    TotalTests = 0
    TotalPassed = 0
    functions = sorted(
             #get a list of fields that have the order set
             [
               getattr(class_obj, field) for field in dir(class_obj)
               if hasattr(getattr(class_obj, field), 'order')
             ],
             #sort them by their order
             key = (lambda field: field.order)
            )
    #print functions
    print ("Running testcases of set " + class_obj.__class__.__name__ + " :")
    logger.info("Running testcases of set "+ class_obj.__class__.__name__ + " :")
    dict = {}
    dict2= {}
    for func in functions:
        TotalTests = TotalTests+1
        #print TotalTests
        print ("--------------------------------------")
        logger.info("--------------------------------------")
        status = func()
        #print "--------------------------------------"
        dict[time.time()] = [ func.__name__, status ]
        if status is True:
            print (func.__name__ + "............  OK")
            logger.info(func.__name__ + "............  OK")
            dict2[ func.__name__] = [1, 1]
            TotalPassed = TotalPassed+1
            print ("--------------------------------------")
            logger.info("--------------------------------------")
            #print TotalPassed
        elif status is False:
            print (func.__name__ + "............  Error")
            logger.info(func.__name__ + "............  Error")
            dict2[ func.__name__] = [1, 0]
            print ("--------------------------------------")
            logger.info("--------------------------------------")
        else:
            print ("Testcase did not return any status")
            logger.info("Testcase did not return any status")
    #return dict2, dict
    return dict

def assertEqual(a,b):
    if a == b:
        return True
    else:
        return False

def assertContains(a,b):
    # a: String
    # b: Substring
    if b in a:
        return True
    else:
        return False

def randomString(size=3, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def get_error_logs_test_run():
    open('test_error.log', 'w').close()
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'test_run.log'):
            fpod = open(file, "r")
            lines = fpod.readlines()
            test_start_position = 0
            for i in range(0, len(lines)):
                test_start_position = i if '----' in lines[i] else test_start_position
                if lines[i].__contains__(' Error'):
                    with open('test_error.log', 'a') as f:
                        for line in lines[test_start_position:i+1]:
                            f.write(line)



def decodeCredential(cred):
    return cred

def encodeCredential(cred):
    return cred
