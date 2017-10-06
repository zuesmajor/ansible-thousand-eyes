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
  alert_list:
    description:
      - List of alert names that you'll want to include when alerts are enables
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

RETURN = '''
obj:
    description: The Json of the created Test
    returned: success, changed
    type: dict
'''


import json


def create_new_test(module):
    str_payload = generate_payload(module)
    json_payload = json.dumps(str_payload)

    response = open_url('https://api.thousandeyes.com/tests/' + module.params.get('test_type') + '/' + 'new.json',
        data=json_payload, headers={'Authorization': 'Basic ' + module.params.get('basic_auth_token'), 'Content-Type':'application/json'},
            method="POST")

    return response.read()


def build_alert_list(module):
    alert_id_array = []

    if module.params.get('alert_list') and module.params.get('alerts_enabled'):
        alert_json = open_url('https://api.thousandeyes.com/alerts.json',
            headers={'Authorization': 'Basic ' + module.params.get('basic_auth_token'),
            'Content-Type':'application/json'}, method="GET").read()

        # string to dictionary
        alert_list = json.loads(alert_json)

        for index in range(len(alert_list['alertRules'])):
            for key in alert_list['alertRules'][index]:
                alert_dict = {}
                if alert_list['alertRules'][index][key] in module.params.get('alert_list'):
                    alert_dict['ruleId'] = alert_list['alertRules'][index]['ruleId']
                    alert_id_array.append(alert_dict)

        return alert_id_array

# module to grab agentId's to pass to create_new_test
def build_agent_list(module):
    agent_id_array = []
    # Sample agent NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']

    agent_json = open_url('https://api.thousandeyes.com/agents.json',
        headers={'Authorization': 'Basic ' + module.params.get('basic_auth_token'),
        'Content-Type':'application/json'}, method="GET").read()



    # String to dictionary
    agent_list = json.loads(agent_json)

    for index in range(len(agent_list['agents'])):
        for key in agent_list['agents'][index]:
            agent_dict = {}
            if agent_list['agents'][index][key] in module.params.get('agent_list'):
                agent_dict['agentId'] = agent_list['agents'][index]['agentId']
                agent_id_array.append(agent_dict)

    return agent_id_array



# module to grab the monitorId's to pass to create_new_test for BGP test
# @return list
def build_bgp_monitor_list(module):
    # Returned array for 'bgpMonitors' key in Test
    bgp_monitor_array = []

    # Sample monitor NAME array parameter = ['Orland, FL', 'Atlanda, GA', 'Ashburn, VA-2']
    # need to add to monitorId

    monitor_json = open_url('https://api.thousandeyes.com/bgp-monitors.json',
        headers={'Authorization': 'Basic ' + module.params.get('basic_auth_token'),
        'Content-Type':'application/json'}, method="GET").read()

    # String to dictionary
    monitor_list = json.loads(monitor_json)

    # We want to loop through bgp_monitor_list and grab the ID's for the monitoring id's
    for index in range(len(monitor_list['bgpMonitors'])):
        for key in monitor_list['bgpMonitors'][index]:
            monitor_dict = {}
            if monitor_list['bgpMonitors'][index][key] in module.params.get('bgp_monitor_list'):
                monitor_dict['monitorId'] = monitor_list['bgpMonitors'][index]['monitorId']
                bgp_monitor_array.append(monitor_dict)

    return bgp_monitor_array


# Generates the payload being sent based on the test type
def generate_payload(module):
    test_type = module.params.get('test_type')
    # Default Payload
    payload = {
        "alertsEnabled": module.params.get("alerts_enabled"),
        "testName": module.params.get('test_name'),
    }

    if module.params.get('alert_list'):
        payload['alertRules'] = build_alert_list(module)

    # 1
    if test_type == "bgp":
        # Required from API
        payload['prefix'] = module.params.get('prefix_bgp')

        payload['monitorId'] = build_bgp_monitor_list(module)

        return payload
    # 2
    elif test_type == "network":
        # Required from API
        payload['interval'] = module.params.get('interval')
        payload['agents'] = build_agent_list(module)

        # optional
        if module.params.get('bgp_monitor_list'):
            payload['bgpMonitors'] = build_bgp_monitor_list(module)
        if module.params.get('port'):
            payload['port'] = module.params.get('port')
        if module.params.get('protocol'):
            payload['protocol'] = module.params.get('protocol')

        return payload
    # 3
    elif test_type == "http-server":
        payload['agents'] = build_agent_list(module)
        payload['interval'] = module.params.get('interval')
        payload['url'] = module.params.get('url')

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
            basic_auth_token=dict(required=True, no_log=True),
            test_type=dict(required=True),
            interval=dict(type="int"),
            url=dict(),
            domain=dict(),
            test_name=dict(required=True, type='str'),
            server=dict(),
            port=dict(type="int"),
            protocol=dict(),
            alerts_enabled=dict(required=True, type="int"),
            prefix_bgp=dict(),
            bgp_monitor_list=dict(type='list'), # list of bgp monitors that get passed to the bgp test
            agent_list=dict(type="list"),
            alert_list=dict(type="list"),
            codec_id=dict(type='int'),
            dscp_id=dict(type='int'),
            jitter_buffer=dict(type='int'),
            target_agent_id=dict(type='int'),
            dns_server_list=dict(type='list'),
            # These are specifically for Transaction Test Type
            transaction_steps_stepNum=dict(type='int'),
            transaction_steps_stepName=dict(type='str'),
            transaction_steps_command=dict(type='str'),
            transaction_steps_target=dict(type='str'),
            supports_check_mode=False
        )
    )
    result= create_new_test(module)

    module.exit_json(result=result, changed=True)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
