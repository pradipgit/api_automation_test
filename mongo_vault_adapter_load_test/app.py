#!/usr/bin/python3

import threading
import time
import uuid

import MongoVaultCallService

DEFAULT_ID=str(uuid.uuid4())
class MyThread(threading.Thread):
    def init(self, id):
        self.setName(id)

    def run(self):
        MongoVaultCallService.serviceCallIntegration(threading.current_thread().getName(),str(uuid.uuid4()),DEFAULT_ID)
        ''' For Default tenant
        MongoVaultCallService.serviceCallIntegration(threading.current_thread().getName(),str(uuid.uuid4()), None)
        '''
        pass

if __name__ == '__main__':
    for i in range(3):
        t = MyThread()
        t.start()
