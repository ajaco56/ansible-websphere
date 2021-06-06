#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Amir Mofasser <amir.mofasser@gmail.com> (@amimof)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import subprocess
import platform
import datetime
#import time

def main():

    # Read arguments
    module = AnsibleModule(
        argument_spec = dict(
            state = dict(default='started', choices=['started', 'stopped', 'status']),
            servername = dict(required=True),
            libertydir = dict(required=True, type='path')
            
        )
    )

    state = module.params['state']
    servername = module.params['servername']
    libertydir = module.params['libertydir']

    # Check if paths are valid
    #if not os.path.exists(libertydir):
    #    module.fail_json(msg=libertydir+" does not exists")

    if state == 'stopped':
        child = subprocess.Popen([libertydir+"/bin/server stop " + servername], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = child.communicate()
        if child.returncode != 0:
           if not stderr_value.find(b"is not running") != -1:
               module.fail_json(msg=servername + " stop failed", stdout=stdout_value, stderr=stderr_value)

        module.exit_json(changed=True, msg=servername + " stopped successfully", stdout=stdout_value)

    if state == 'started':
        child = subprocess.Popen([libertydir+"/bin/server start " + servername], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = child.communicate()
        if child.returncode != 0:
           if not stderr_value.find(b"is running with process") != -1:
               module.fail_json(msg=servername + " start failed", stdout=stdout_value, stderr=stderr_value)
        
        #time.sleep(5)
        
        module.exit_json(changed=True, msg=servername + " started successfully", stdout=stdout_value)
        
    if state == 'status':
        child = subprocess.Popen([libertydir+"/bin/server status " + servername], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = child.communicate()
        #if child.returncode != 0:
        if stdout_value.find(b"does not exist") = 0:
            module.fail_json(msg=servername + " status failed", stdout=stdout_value, stderr=stderr_value)
        
        #time.sleep(5)
        
        module.exit_json(changed=False, msg=servername + " status successfully", stdout=stdout_value)


# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
