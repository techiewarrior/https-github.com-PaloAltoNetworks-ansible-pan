#!/usr/bin/env python

#  Copyright 2017 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: panos_security_rule
short_description: Create security rule policy on PAN-OS devices or Panorama management console.
description: >
    Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
    The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
    the traffic is applied, the more specific rules must precede the more general ones.
author: "Ivan Bojer (@ivanbojer), Robert Hagen (@rnh556)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    action:
        description:
            - The action to be taken.  Supported values are I(add)/I(delete)/I(find).
    rule_name:
        description:
            - Name of the security rule.
        required: true
    rule_type:
        description:
            - Type of security rule (version 6.1 of PanOS and above).
        default: "universal"
    description:
        description:
            - Description for the security rule.
        default: "None"
    tag:
        description:
            - Administrative tags that can be added to the rule. Note, tags must be already defined.
        default: "None"
    from_zone:
        description:
            - List of source zones.
        default: "any"
    to_zone:
        description:
            - List of destination zones.
        default: "any"
    source:
        description:
            - List of source addresses.
        default: "any"
    source_user:
        description:
            - Use users to enforce policy for individual users or a group of users.
        default: "any"
    hip_profiles:
        description: >
            If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy
            on information collected by GlobalProtect. For example, the user access level can be determined HIP that
            notifies the firewall about the user's local configuration.
        default: "any"
    destination:
        description:
            - List of destination addresses.
        default: "any"
    application:
        description:
            - List of applications.
        default: "any"
    service:
        description:
            - List of services.
        default: "application-default"
    log_start:
        description:
            - Whether to log at session start.
        default: false
    log_end:
        description:
            - Whether to log at session end.
        default: true
    action:
        description:
            - Action to apply once rules maches.
        default: "allow"
    group_profile:
        description: >
            Security profile group that is already defined in the system. This property supersedes antivirus,
            vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
        default: None
    antivirus:
        description:
            - Name of the already defined antivirus profile.
        default: None
    vulnerability:
        description:
            - Name of the already defined vulnerability profile.
        default: None
    spyware:
        description:
            - Name of the already defined spyware profile.
        default: None
    url_filtering:
        description:
            - Name of the already defined url_filtering profile.
        default: None
    file_blocking:
        description:
            - Name of the already defined file_blocking profile.
        default: None
    data_filtering:
        description:
            - Name of the already defined data_filtering profile.
        default: None
    wildfire_analysis:
        description:
            - Name of the already defined wildfire_analysis profile.
        default: None
    devicegroup:
        description: >
            Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.
            If device group is not define we assume that we are contacting Firewall.
        default: None
'''

EXAMPLES = '''
- name: add an SSH inbound rule to devicegroup
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    operation: 'add'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    from_zone: ['public']
    to_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    hip_profiles: ['any']
    action: 'allow'
    devicegroup: 'Cloud Edge'

- name: add a rule to allow HTTP multimedia only from CDNs
  panos_security_rule:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    operation: 'add'
    rule_name: 'HTTP Multimedia'
    description: 'Allow HTTP multimedia only to host at 1.1.1.1'
    from_zone: ['public']
    to_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['content-delivery-networks']
    application: ['http-video', 'http-audio']
    service: ['service-http', 'service-https']
    hip_profiles: ['any']
    action: 'allow'

- name: add a more complex rule that uses security profiles
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    operation: 'add'
    rule_name: 'Allow HTTP w profile'
    log_start: false
    log_end: true
    action: 'allow'
    antivirus: 'default'
    vulnerability: 'default'
    spyware: 'default'
    url_filtering: 'default'
    wildfire_analysis: 'default'

- name: delete a devicegroup security rule
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    operation: 'delete'
    rule_name: 'Allow telnet'
    devicegroup: 'DC Firewalls'

- name: find a specific security rule
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    password: '{{ password }}'
    operation: 'find'
    rule_name: 'Allow RDP to DCs'
  register: result
- debug: msg='{{result.stdout_lines}}'

'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    import pan.xapi
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import objects
    from pandevice import policies
    import xmltodict
    import json

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dev_grps = device.refresh_devices()
    for grp in dev_grps:
        if isinstance(grp, pandevice.panorama.DeviceGroup):
            if grp.name == devicegroup:
                return True
    return False


def get_rulebase(device, devicegroup):
    # Build the rulebase
    if isinstance(device, pandevice.firewall.Firewall):
        rulebase = pandevice.policies.Rulebase()
        device.add(rulebase)
    elif isinstance(device, pandevice.panorama.Panorama):
        dg = panorama.DeviceGroup(devicegroup)
        device.add(dg)
        rulebase = policies.PreRulebase()
        dg.add(rulebase)
    else:
        return False
    policies.SecurityRule.refreshall(rulebase)
    return rulebase


def find_rule(rulebase, rule_name):
    # Search for the rule name
    rule = rulebase.find(rule_name)
    if rule:
        return rule
    else:
        return False


def create_security_rule(**kwargs):
    security_rule = policies.SecurityRule(
        name=kwargs['rule_name'],
        description=kwargs['description'],
        tozone=kwargs['to_zone'],
        fromzone=kwargs['from_zone'],
        source=kwargs['source'],
        source_user=kwargs['source_user'],
        destination=kwargs['destination'],
        category=kwargs['category'],
        application=kwargs['application'],
        service=kwargs['service'],
        hip_profiles=kwargs['hip_profiles'],
        log_start=kwargs['log_start'],
        log_end=kwargs['log_end'],
        type=kwargs['rule_type'],
        action=kwargs['action'])

    if 'tag' in kwargs:
        security_rule.tag = kwargs['tag']

    # profile settings
    if 'group_profile' in kwargs:
        security_rule.group = kwargs['group_profile']
    else:
        if 'antivirus' in kwargs:
            security_rule.virus = kwargs['antivirus']
        if 'vulnerability' in kwargs:
            security_rule.vulnerability = kwargs['vulnerability']
        if 'spyware' in kwargs:
            security_rule.spyware = kwargs['spyware']
        if 'url_filtering' in kwargs:
            security_rule.url_filtering = kwargs['url_filtering']
        if 'file_blocking' in kwargs:
            security_rule.file_blocking = kwargs['file_blocking']
        if 'data_filtering' in kwargs:
            security_rule.data_filtering = kwargs['data_filtering']
        if 'wildfire_analysis' in kwargs:
            security_rule.wildfire_analysis = kwargs['wildfire_analysis']
    return security_rule


def add_rule(rulebase, sec_rule):
    if rulebase:
        rulebase.add(sec_rule)
        sec_rule.create()
        return True
    else:
        return False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        operation=dict(required=True, choices=['add', 'delete', 'find']),
        rule_name=dict(required=True),
        description=dict(default=''),
        tag=dict(),
        to_zone=dict(type='list', default=['any']),
        from_zone=dict(type='list', default=['any']),
        source=dict(type='list', default=["any"]),
        source_user=dict(type='list', default=['any']),
        destination=dict(type='list', default=["any"]),
        category=dict(type='list', default=['any']),
        application=dict(type='list', default=['any']),
        service=dict(type='list', default=['application-default']),
        hip_profiles=dict(type='list', default=['any']),
        group_profile=dict(),
        antivirus=dict(),
        vulnerability=dict(),
        spyware=dict(),
        url_filtering=dict(),
        file_blocking=dict(),
        data_filtering=dict(),
        wildfire_analysis=dict(),
        log_start=dict(type='bool', default=False),
        log_end=dict(type='bool', default=True),
        rule_type=dict(default='universal'),
        action=dict(default='allow'),
        devicegroup=dict(),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    operation = module.params['operation']
    rule_name = module.params['rule_name']
    description = module.params['description']
    tag = module.params['tag']
    from_zone = module.params['from_zone']
    to_zone = module.params['to_zone']
    source = module.params['source']
    source_user = module.params['source_user']
    destination = module.params['destination']
    category = module.params['category']
    application = module.params['application']
    service = module.params['service']
    hip_profiles = module.params['hip_profiles']
    log_start = module.params['log_start']
    log_end = module.params['log_end']
    rule_type = module.params['rule_type']
    action = module.params['action']
    group_profile = module.params['group_profile']
    antivirus = module.params['antivirus']
    vulnerability = module.params['vulnerability']
    spyware = module.params['spyware']
    url_filtering = module.params['url_filtering']
    file_blocking = module.params['file_blocking']
    data_filtering = module.params['data_filtering']
    wildfire_analysis = module.params['wildfire_analysis']
    devicegroup = module.params['devicegroup']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(
                failed=1,
                msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup
            )

    # Get the rulebase
    rulebase = get_rulebase(device, dev_group)

    # Which action shall we take on the object?
    if operation == "find":
        # Search for the object
        match = find_rule(rulebase, rule_name)
        # If found, format and return the result
        if match:
            match_dict = xmltodict.parse(match.element_str())
            module.exit_json(
                stdout_lines=json.dumps(match_dict, indent=2),
                msg='Rule matched'
            )
        else:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % rule_name)
    elif operation == "delete":
        # Search for the object
        match = find_rule(rulebase, rule_name)
        # If found, delete it
        if match:
            try:
                match.delete()
            except PanXapiError:
                exc = get_exception()
                module.fail_json(msg=exc.message)

            module.exit_json(changed=True, msg='Rule \'%s\' successfully deleted' % rule_name)
        else:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % rule_name)
    elif operation == "add":
        try:
            new_rule = create_security_rule(
                rule_name=rule_name,
                description=description,
                tag=tag,
                from_zone=from_zone,
                to_zone=to_zone,
                source=source,
                source_user=source_user,
                destination=destination,
                category=category,
                application=application,
                service=service,
                hip_profiles=hip_profiles,
                group_profile=group_profile,
                antivirus=antivirus,
                vulnerability=vulnerability,
                spyware=spyware,
                url_filtering=url_filtering,
                file_blocking=file_blocking,
                data_filtering=data_filtering,
                wildfire_analysis=wildfire_analysis,
                log_start=log_start,
                log_end=log_end,
                rule_type=rule_type,
                action=action
            )
            changed = add_rule(rulebase, new_rule)
        except PanXapiError:
            exc = get_exception()
            module.fail_json(msg=exc.message)
        module.exit_json(changed=changed, msg="Rule \'%s\' successfully added" % rule_name)
    else:
        module.fail_json(msg='Invalid action')


if __name__ == '__main__':
    main()