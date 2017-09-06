#for index in range(len(string["test"])): # length of the array
#  for key in string["test"][index]: # loops over the keys in the array for each index
#      print(string["test"][index][key] # prints values of the keys

#^^
# Need to perform the same on agents to grab the agentId

# response = requests.post('https://api.thousandeyes.com/tests/http-server/new.json', json=data,  headers={'Authorization': 'Basic %s' % 'cGF0cnlhbjFAcGFsb2FsdG9uZXR3b3Jrcy5jb206YWdxOXh5OTRpZ3cwaHAxNGwyMWFzdmVvbGtiemp1amQ='})
# data = {"interval": 300, "agents":[{"agentId": 206}], "server": "www.patrick.com", "port": 80, "alertsEnabled": 0}

DOCUMENTATION = '''
module: te_test
short_description: Used to create a Thousand Eyes test
description: You are able to create a new test for any of the 9 tests available on Thousand Eyes. Requires a Basic Auth Token from your account.
version_added: 1.0
author: Patrick Ryan
requirements: requests
notes: Does not require anything other than the Requests python library.
options:
  username:
    description:
      - This has to be your thousand eyes Email
  basic_auth_token
    description:
      - Token from your account. This is used for authentication
  test_type:
    description:
      - The 
'''

EXAMPLES = '''
- name: Create New Thousand Eyes Test
  te_test:
    username: patryan1@paloaltonetworks.com
    basic_auth_token: kjahsdkfhlakjshkfhjkasdf
    test_type: http-server
    agent_list
'''


import json
import requests
from ansible.module_utils.basic import *


def createNewTest(module):
    response = requests.post('https://api.thousandeyes.com/tests/' + module.params.get('test_type') + '/' + 'new.json', json=payload, headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token') })


# module to grab agentId's to pass to createNewTest
def buildAgentIdList(module):
    # Sample agent NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']
    agent_id_array = []

    response = requests.get('https://api.thousandeyes.com/agents.json', headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token')})

    # String to dictionary
    agent_list = json.loads(response.content)

    for index in range(len(agent_list['agents'])):
        for key in agent_list['agents'][index]:
            agent_dict = {}
            if agent_list['agents'][index][key] in module.params.get('agent_list'):
                agent_dict['agents'] = agent_list['agents'][index]['agentId']
                agent_id_array.append(agent_dict)

    return agent_id_array




# module to grab the monitorId's to pass to createNewTest for BGP test
# @return list
def buildBgpMonitorList(module):
    # Sample monitor NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']
    # need to add to monitorId

    # Returned array for 'bgpMonitors' key in Test
    bgp_monitor_array = []

    response = requests.get('https://api.thousandeyes.com/bgp-monitors.json', headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token')})
    # String to dictionary
    monitor_list = json.loads(response.content)

    # We want to loop through bgp_monitor_list and grab the ID's for the monitoring id's
    for index in range(len(monitor_list['bgpMonitors'])):
        for key in monitor_list['bgpMonitors'][index]:
            monitor_dict = {}
            if monitor_list['bgpMonitors'][index][key] in module.params.get('bgp_monitor_list'):
                monitor_dict['monitorId'] = monitor_list['bgpMonitors'][index]['monitorId']
                bgp_monitor_array.append(agent_dict)

    return bgp_monitor_array


# Generates the payload being sent based on the test type
def generatePayload(module):
    test_type = module.params.get('test_type')
    # Default Payload
    payload = {
        "alertsEnables": module.params.get("alerts_enabled"),
        "testName": module.params.get('test_name')
    }

    if test_type == "bgp":
        # Required from API
        payload['prefix'] = module.params.get('prefix_bgp')

        payload['monitorId'] = buildBgpMonitorList()

        return payload
    elif test_type == "network"
        # Required from API
        payload['interval'] = module.params.get('interval')
        payload['agents'] = buildAgentIdList()

        # optional
        payload['bgpMonitors'] = buildBgpMonitorList()
        payload['port'] = module.params.get('port')
        payload['protocol'] = module.params.get('protocol')

        return payload
    elif test_type == "http-server":
        payload['agents']: buildAgentIdList()
        payload['interval']: module.params.get('interval')
        payload['url']: module.params.get('url')

        return payload
    elif test_type == 'page-load':
        payload['agents'] = buildAgentIdList()
        payload['interval'] = module.params.get('interval')
        payload['url'] = module.params.get('url')

        return payload
    elif test_type == 'transactions':





def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(required=True),
            basic_auth_token=dict(required=True),
            test_type=dict(required=True),
            agent_list=dict(type="list"),
            payload=dict(),
            interval=dict(),
            url=dict(),
            domain=dict(),
            test_name=dict(required=True, type='str'),
            server=dict(),
            port=dict(type="int"),
            protocol=dict(),
            alerts_enabled=dict(type="int"),
            prefix_bgp=dict(),
            bgp_monitor_list=dict(type='list'), # list of bgp monitors that get passed to the bgp test
            codecId=dict(),
            dscpId=dict(),
            jitterBuffer=dict(),
            targetAgentId=dict(),
        )
    )


if __name__ == '__main__':
    main()
