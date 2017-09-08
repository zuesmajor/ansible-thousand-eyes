ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: te_test
short_description: Used to create a Thousand Eyes test
description: You are able to create a new test for any of the 9 tests available on Thousand Eyes. Requires a Basic Auth Token from your account.
version_added: 1.0
author: Patrick Ryan
requirements: none
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
      - One of the 9 test types
  agent_list:
    description:
      - List of the agent names that you want binded to the test
  bgp_monitor_list:
    description:
      - List of the monitor names you want binded to the test
  interval:
    description:
      - value in seconds
  url:
    description:
      - Used for HTTP or website checks mainly
  domain:
    description:
      - Domain name
  test_name:
    description:
      - optional parameter but best practice to name all of your tests
  server:
    description:
      - fqdn of DNS resolver
  port:
    description:
      - port number for the server
  protocol:
    description:
      - what protocol will be Used
  alerts_enabled:
    description:
      - integer whether 1 is yes and 0 is no
  prefix_bgp:
    description:
      - a.b.c.d is a network address, with the prefix length defined as e. Prefixes can be any length from 8 to 24
  codec_id:
    description:
      - Voice Codic list
  dscp_id:
    description:
      - DSCP list
  jitterBugger:
    description:
      - de-jitter buffer size (in seconds)
  target_agent_id:
    description:
      - Both the "agents": [] and the target_agent_id cannot be cloud agents.
  transaction_steps_stepNum:
    description:
      - Steps must be provided sequentially, and must start at zero
  transaction_steps_stepName:
    description:
      - name for the step
  transaction_steps_command:
    description:
      - command for the step
  transactionSteps.target:
    description:
      - target for the step
  dns_server_list:
    description:
      - List of DNS servers required for the dns-server test type
'''

EXAMPLES = '''
- name: Create New Thousand Eyes Test
  te_test:
    username: patryan1@paloaltonetworks.com
    basic_auth_token: kjahsdkfhlakjshkfhjkasdf
    test_type: http-server
    agent_list: ['Tokyo-3', 'Orlando, FL', 'Amsterdam-3']
    url: www.google.com
    interval: 120
'''


import json
import ast
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

# One function to build the json instead of using requests for each other function
def build_test_type_json(module):

    if module.params.get('agent_list') and not module.params.get('bgp_monitor_list'):
        agent_string = json.loads(open_url('https://api.thousandeyes.com/agents.json',
            headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token'),
            'Content-Type':'application/json'}, method="GET").read())

        agent_dict = json.loads(agent_string)

        return agent_dict

    elif module.params.get('bgp_monitor_list') and not module.params.get('agent_list'):
        monitor_string = json.loads(open_url('https://api.thousandeyes.com/bgp-monitors.json',
            headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token'),
            'Content-Type':'application/json'}, method="GET").read())


        monitor_dict = json.loads(monitor_string)

        return monitor_dict


def create_new_test(module):
    payload = generate_payload(module)
    response = requests.post('https://api.thousandeyes.com/tests/' + module.params.get('test_type') + '/' + 'new.json',
        json=payload, headers={'Authorization': 'Basic %s' % module.params.get('basic_auth_token') })

# module to grab agentId's to pass to create_new_test
def build_agent_list(module):
    # Sample agent NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']
    agent_id_array = []

    # String to dictionary
    agent_list = build_test_type_json(module)

    for index in range(len(agent_list['agents'])):
        for key in agent_list['agents'][index]:
            agent_dict = {}
            if agent_list['agents'][index][key] in module.params.get('agent_list'):
                agent_dict['agents'] = agent_list['agents'][index]['agentId']
                agent_id_array.append(agent_dict)

    return agent_id_array



# module to grab the monitorId's to pass to create_new_test for BGP test
# @return list
def build_bgp_monitor_list(module):
    # Sample monitor NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']
    # need to add to monitorId

    # Returned array for 'bgpMonitors' key in Test
    bgp_monitor_array = []

    # String to dictionary
    monitor_list = build_test_type_json(module)

    # We want to loop through bgp_monitor_list and grab the ID's for the monitoring id's
    for index in range(len(monitor_list['bgpMonitors'])):
        for key in monitor_list['bgpMonitors'][index]:
            monitor_dict = {}
            if monitor_list['bgpMonitors'][index][key] in module.params.get('bgp_monitor_list'):
                monitor_dict['monitorId'] = monitor_list['bgpMonitors'][index]['monitorId']
                bgp_monitor_array.append(agent_dict)

    return bgp_monitor_array


# Generates the payload being sent based on the test type
def generate_payload(module):
    test_type = module.params.get('test_type')
    # Default Payload
    payload = {
        "alertsEnables": module.params.get("alerts_enabled"),
        "testName": module.params.get('test_name')
    }

    # 1
    if test_type == "bgp":
        # Required from API
        payload['prefix'] = module.params.get('prefix_bgp')

        payload['monitorId'] = build_bgp_monitor_list(module)

        return payload
    # 2
    elif test_type == "network"
        # Required from API
        payload['interval'] = module.params.get('interval')
        payload['agents'] = build_agent_list(module)

        # optional
        payload['bgpMonitors'] = build_bgp_monitor_list(module)
        payload['port'] = module.params.get('port')
        payload['protocol'] = module.params.get('protocol')

        return payload
    # 3
    elif test_type == "http-server":
        payload['agents']: build_agent_list(module)
        payload['interval']: module.params.get('interval')
        payload['url']: module.params.get('url')

        return payload
    # 4
    elif test_type == 'page-load':
        payload['agents'] = build_agent_list(module)
        payload['interval'] = module.params.get('interval')
        payload['url'] = module.params.get('url')

        return payload
    # 5
    elif test_type == 'transactions':
        payload['agents'] = build_agent_list(module)
        payload['interval'] = module.params.get('interval')
        payload['url'] = module.params.get('url')
        payload['transactionSteps.stepNum'] = module.params.get('transaction_steps_stepNum')
        payload['transactionSteps.stepName'] = module.params.get('transaction_steps_stepName')
        payload['transactionSteps.command'] = module.params.get('transaction_steps_command')
        payload['transactionSteps.target'] = module.params.get('transaction_steps_target')

        return payload
    elif test_type == "dns-trace":
        payload['agents'] = build_agent_list(module)
        payload['domain'] = module.params.get('domain')
        payload['interval'] = module.params.get('interval')

        return payload
    # 6
    elif test_type == "dns-server":
        payload['agents'] = build_agent_list(module)
        payload['dnsServers'] = module.params.get('dns_server_list')
        payload['domain'] = module.params.get('domain')
        payload['interval'] = module.params.get('interval')

        return payload
    # 7
    elif test_type == "dns-dnssec":
        payload['agents'] = build_agent_list(module)
        payload['domain'] = module.params.get('domain')
        payload['interval'] = module.params.get('interval')

        return payload
    # 8
    elif test_type == "voice":
        payload['agents'] = build_agent_list(module)
        payload['codecId'] = module.params.get('codec_id')
        payload['dscpId'] = module.params.get('dscp_id')
        payload['interval'] = module.params.get('interval')
        payload['jitterBuffer'] = module.params.get('jitter_buffer')
        payload['targetAgentId'] = module.params.get('target_agent_id')

        return payload


def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(required=True),
            basic_auth_token=dict(required=True),
            test_type=dict(required=True),
            agent_list=dict(type="list"),
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
            codec_id=dict(type='int'),
            dscp_id=dict(type='int'),
            jitter_buffer=dict(type='int'),
            target_agent_id=dict(type='int'),
            dns_server_list=dict(type='list'),
            # These are specifically for Transaction Test Type
            transaction_steps_stepNum=dict(type='int'),
            transaction_steps_stepName=dict(type='str'),
            transaction_steps_command=dict(type='str'),
            transaction_steps_target=dict(type='str')
        )
    )
    create_new_test(module)


if __name__ == '__main__':
    main()
