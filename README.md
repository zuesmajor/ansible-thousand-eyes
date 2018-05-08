# In Progress:
Create-Test is almost done. 

Need to generate Alert Rule list in order to bind it to the new agent to be created

Supported fields for the module

```python
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
```
# To-Do
Module for update and delete test
