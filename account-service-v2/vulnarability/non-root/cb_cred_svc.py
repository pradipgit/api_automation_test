import time
import subprocess
import utils
from utils import assignOrder
from utils import assertEqual
from utils import assertContains
from utils import randomString
import threading
import Queue
import random
from collections import OrderedDict
import logging
import pprint
import ConfigParser
import json
import random
import requests
import datetime
import paramiko , sys

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = ConfigParser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
# db=config.get('params','db')
# invalidUrl =config.get('params', 'invalidUrl')
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

global nbytes,hostname,port,username,password,command1,command2,stdout_data,stderr_data,stdout_data1,stderr_data1
global pversion,nversion
pversion ='2.7.15'
nversion='v8.12.0'

nbytes = 4096
hostname = '9.199.144.69'
port = 22
username = 'root'
password = 'Gravitant123!'
stdout_data = []
stderr_data = []
stdout_data1 = []
stderr_data1 = []


class NonRootTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(1)
    def non_root_test_cb_cred_svc(self):
        try:
            passed = False
            command1 = 'kubectl -n dev-core get pods | awk \'{print $1}\''
            command2 = 'kubectl -n dev-core exec -it pod -- ps -eaf | sed \'1d;$d\'| awk \'{print $2}\''
            client1 = paramiko.Transport((hostname, port))
            client1.connect(username=username, password=password)
            session1 = client1.open_channel(kind='session')
            session1.exec_command(command1)
            while True:
                if session1.recv_ready():
                    stdout_data1.append(session1.recv(nbytes))
                if session1.recv_stderr_ready():
                    stderr_data1.append(session1.recv_stderr(nbytes))
                if session1.exit_status_ready():
                    break

            print 'exit status: ', session1.recv_exit_status()
            resp1= ''.join(stdout_data1)
            print resp1

            session1.close()
            client1.close()
            line = resp1.split('\n')

            p=[e for e in line if e.startswith('cb-cred-svc')]
            print p[0]
            client = paramiko.Transport((hostname, port))
            client.connect(username=username, password=password)
            session = client.open_channel(kind='session')
            print p[0]
            command2=command2.replace("pod",p[0])
            print command2
            session.exec_command(command2)
            command2 = command2.replace(p[0], "pod")
            while True:
                if session.recv_ready():
                    stdout_data.append(session.recv(nbytes))
                if session.recv_stderr_ready():
                    stderr_data.append(session.recv_stderr(nbytes))
                if session.exit_status_ready():
                    break

            print 'exit status: ', session.recv_exit_status()
            resp2= ''.join(stdout_data)
            print resp2

            x=resp2.rsplit()
            print x[0]

            if x[0]=='root':
                passed = False
            else:
                passed = True

            session.close()
            client.close()

            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(2)
    def non_root_test_cb_cred_svc_version_check(self):
        stdout_data = []
        stderr_data = []
        stdout_data1 = []
        stderr_data1 = []
        try:
            passed = False
            command1 = 'kubectl -n dev-core get pods | awk \'{print $1}\''
            command2 = 'kubectl -n dev-core exec -it pod -- node --version'
            client1 = paramiko.Transport((hostname, port))
            client1.connect(username=username, password=password)
            session1 = client1.open_channel(kind='session')
            session1.exec_command(command1)
            while True:
                if session1.recv_ready():
                    stdout_data1.append(session1.recv(nbytes))
                if session1.recv_stderr_ready():
                    stderr_data1.append(session1.recv_stderr(nbytes))
                if session1.exit_status_ready():
                    break

            print 'exit status: ', session1.recv_exit_status()
            resp1= ''.join(stdout_data1)
            print resp1

            session1.close()
            client1.close()
            line = resp1.split('\n')

            p=[e for e in line if e.startswith('cb-cred-svc')]
            print "pod is: " +p[0]

            client = paramiko.Transport((hostname, port))
            client.connect(username=username, password=password)
            session = client.open_channel(kind='session')
            command2 = command2.replace("pod",p[0])
            print command2

            session.exec_command(command2)

            while True:
                if session.recv_ready():
                    stdout_data.append(session.recv(nbytes))
                if session.recv_stderr_ready():
                    stderr_data.append(session.recv_stderr(nbytes))
                if session.exit_status_ready():
                    break

            print stdout_data
            print stderr_data
            print 'exit status: ', session.recv_exit_status()
            resp2= ''.join(stderr_data)
            print resp2

            passed = pversion in resp2
            print passed

            session.close()
            client.close()

            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False
