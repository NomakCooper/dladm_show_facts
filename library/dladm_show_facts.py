#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: dladm_show_facts
author:
    - Marco Noce (@NomakCooper)
description:
    - Gathers facts about Solaris dladm show attributes on Solaris 11.
    - This module currently supports SunOS Family, Oracle Solaris 11.
requirements:
  - dladm
short_description: Gathers facts about Solaris dladm show attributes.
notes:
  - |
    This module shows the list of attributes of Solaris dladm show.
options:
    attribute:
        description:
            - The dladm show attribute.
        required: true
        type: str
        choices:
            - aggr
            - link
            - vnic
            - ether
            - phys
'''

EXAMPLES = r'''
- name: Gather facts dladm link
  dladm_show_facts:
    attribute: 'link'

- name: Gather facts dladm ether
  dladm_show_facts:
    attribute: 'ether'

- name: Gather facts dladm phys
  dladm_show_facts:
    attribute: 'phys'

- name: set fact for print
  set_fact:
    net0_state: "{{ ansible_facts.dladm_link_list | selectattr('LINK','equalto', 'net0' ) | map(attribute='STATE') | first }}"
    net0_speed_duplex: "{{ ansible_facts.dladm_ether_list | selectattr('LINK','equalto', 'net0' ) | map(attribute='SPEED-DUPLEX') | first }}"
    net0_device: "{{ ansible_facts.dladm_phys_list | selectattr('LINK','equalto', 'net0' ) | map(attribute='DEVICE') | first }}"

- name: print state, device and speed-duplex of net0
  debug:
    msg: "net0 is {{net0_state}} on {{net0_device}} at {{net0_speed_duplex}} speed"
'''

RETURN = r'''
ansible_facts:
  description: Dictionary containing the attribute of dladm show
  returned: always
  type: complex
  contains:
    dladm_aggr_list:
      description: A list of attribute of dladm show-aggr
      returned: if attribute is aggr
      type: list
      contains:
        LINK:
          description: The link name.
          returned: always
          type: str
          sample: "aggr1"
        MODE:
          description: The link mode.
          returned: always
          type: str
          sample: "trunk"
        POLICY:
          description: The link policy.
          returned: always
          type: str
          sample: "L4"
        ADDRPOLICY:
          description: The link address policy.
          returned: always
          type: str
          sample: "auto"
        LACPACTIVITY:
          description: The lacp activity.
          returned: always
          type: str
          sample: "active"
        LACPTIMER:
          description: The lacp timer.
          returned: always
          type: str
          sample: "short"
    dladm_link_list:
      description: A list of attribute of dladm show-link
      returned: if attribute is link
      type: list
      contains:
        LINK:
          description: The link name.
          returned: always
          type: str
          sample: "net0"
        CLASS:
          description: The link class.
          returned: always
          type: str
          sample: "phys"
        MTU:
          description: The link MTU.
          returned: always
          type: str
          sample: "1500"
        STATE:
          description: The link state.
          returned: always
          type: str
          sample: "up"
        OVER:
          description: The over interface of link.
          returned: always
          type: str
          sample: "--"
    dladm_vnic_list:
      description: A list of attribute of dladm show-vnic
      returned: if attribute is vnic
      type: list
      contains:
        LINK:
          description: The link name.
          returned: always
          type: str
          sample: "ldoms-vsw0.vport0"
        OVER:
          description: The over interface of link.
          returned: always
          type: str
          sample: "net0"
        SPEED:
          description: The link speed.
          returned: always
          type: str
          sample: "1000"
        MACADDRESS:
          description: The link mac address.
          returned: always
          type: str
          sample: "0:11:4f:fa:e1:f5"
        MACADDRTYPE:
          description: The link mac address type.
          returned: always
          type: str
          sample: "fixed"
        IDS:
          description: The link IDS.
          returned: always
          type: str
          sample: "VID:0,415"
    dladm_ether_list:
      description: A list of attribute of dladm show-ether
      returned: if attribute is ether
      type: list
      contains:
        LINK:
          description: The link name.
          returned: always
          type: str
          sample: "net0"
        PTYPE:
          description: The link property type.
          returned: always
          type: str
          sample: "current"
        STATE:
          description: The link state.
          returned: always
          type: str
          sample: "up"
        AUTO:
          description: The link auto.
          returned: always
          type: str
          sample: "yes"
        SPEED-DUPLEX:
          description: The link speed duplex.
          returned: always
          type: str
          sample: "1G-f"
        PAUSE:
          description: The link pause.
          returned: always
          type: str
          sample: "bi"
    dladm_phys_list:
      description: A list of attribute of dladm show-phys
      returned: if attribute is phys
      type: list
      contains:
        LINK:
          description: The link name.
          returned: always
          type: str
          sample: "net0"
        MEDIA:
          description: The link type.
          returned: always
          type: str
          sample: "Ethernet"
        STATE:
          description: The link state.
          returned: always
          type: str
          sample: "up"
        SPEED:
          description: The link speed.
          returned: always
          type: str
          sample: "1000"
        DUPLEX:
          description: The link duplex.
          returned: always
          type: str
          sample: "full"
        DEVICE:
          description: The link device.
          returned: always
          type: str
          sample: "ixgbe4"
'''

import platform
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule


def aggr_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header )
    # LINK              MODE  POLICY   ADDRPOLICY           LACPACTIVITY LACPTIMER

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 6)
        try:
            if len(cells) == 6:
                LINK, MODE, POLICY, ADDRPOLICY, LACPACTIVITY, LACPTIMER = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `dladm show-aggr` table layout "LINK,MODE,POLICY,ADDRPOLICY,LACPACTIVITY,LACPTIMER" \
                but got something else: {0}'.format(line)
            )

        result = {
            'LINK': LINK,
            'MODE': MODE,
            'POLICY': POLICY,
            'ADDRPOLICY': ADDRPOLICY,
            'LACPACTIVITY': LACPACTIVITY,
            'LACPTIMER': LACPTIMER,
        }
        results.append(result)
    return results


def link_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header )
    # LINK                CLASS     MTU    STATE    OVER

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 5)
        try:
            if len(cells) == 5:
                LINK, CLASS, MTU, STATE, OVER = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `dladm show-link` table layout "LINK,CLASS,MTU,STATE,OVER" \
                but got something else: {0}'.format(line)
            )

        result = {
            'LINK': LINK,
            'CLASS': CLASS,
            'MTU': MTU,
            'STATE': STATE,
            'OVER': OVER,
        }
        results.append(result)
    return results


def vnic_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header )
    # LINK            OVER           SPEED  MACADDRESS        MACADDRTYPE IDS

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 6)
        try:
            if len(cells) == 6:
                LINK, OVER, SPEED, MACADDRESS, MACADDRTYPE, IDS = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `dladm show-vnic` table layout "LINK,OVER,SPEED,MACADDRESS,MACADDRTYPE,IDS" \
                but got something else: {0}'.format(line)
            )

        result = {
            'LINK': LINK,
            'OVER': OVER,
            'SPEED': SPEED,
            'MACADDRESS': MACADDRESS,
            'MACADDRTYPE': MACADDRTYPE,
            'IDS': IDS,
        }
        results.append(result)
    return results


def ether_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header )
    # LINK              PTYPE    STATE    AUTO  SPEED-DUPLEX                    PAUSE

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 6)
        try:
            if len(cells) == 6:
                LINK, PTYPE, STATE, AUTO, SPEED_DUPLEX, PAUSE = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `dladm show-ether` table layout "LINK,PTYPE,STATE,AUTO,SPEED-DUPLEX,PAUSE" \
                but got something else: {0}'.format(line)
            )

        result = {
            'LINK': LINK,
            'PTYPE': PTYPE,
            'STATE': STATE,
            'AUTO': AUTO,
            'SPEED-DUPLEX': SPEED_DUPLEX,
            'PAUSE': PAUSE,
        }
        results.append(result)
    return results


def phys_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header )
    # LINK            MEDIA         STATE      SPEED  DUPLEX    DEVICE

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 6)
        try:
            if len(cells) == 6:
                LINK, MEDIA, STATE, SPEED, DUPLEX, DEVICE = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `dladm show-phys` table layout "LINK,MEDIA,STATE,SPEED,DUPLEX,DEVICE" \
                but got something else: {0}'.format(line)
            )

        result = {
            'LINK': LINK,
            'MEDIA': MEDIA,
            'STATE': STATE,
            'SPEED': SPEED,
            'DUPLEX': DUPLEX,
            'DEVICE': DEVICE,
        }
        results.append(result)
    return results


def main():
    module = AnsibleModule(
        argument_spec=dict(
            attribute=dict(type='str', required=True, choices=['aggr', 'link', 'vnic', 'ether', 'phys']),
        ),
        supports_check_mode=True,
    )

    attr = module.params['attribute']

    if attr == 'aggr':
        command_args = ['show-aggr']
        commands_map = {
            'dladm': {
                'args': [],
                'parse_func': aggr_parse
            },
        }
        commands_map['dladm']['args'] = command_args

    if attr == 'link':
        command_args = ['show-link']
        commands_map = {
            'dladm': {
                'args': [],
                'parse_func': link_parse
            },
        }
        commands_map['dladm']['args'] = command_args

    if attr == 'vnic':
        command_args = ['show-vnic']
        commands_map = {
            'dladm': {
                'args': [],
                'parse_func': vnic_parse
            },
        }
        commands_map['dladm']['args'] = command_args

    if attr == 'ether':
        command_args = ['show-ether']
        commands_map = {
            'dladm': {
                'args': [],
                'parse_func': ether_parse
            },
        }
        commands_map['dladm']['args'] = command_args

    if attr == 'phys':
        command_args = ['show-phys']
        commands_map = {
            'dladm': {
                'args': [],
                'parse_func': phys_parse
            },
        }
        commands_map['dladm']['args'] = command_args

    if platform.system() != 'SunOS':
        module.fail_json(msg='This module requires SunOS.')

    if platform.release() != '5.11':
        module.fail_json(msg='This module requires Solaris 11.x Major Release.')

    result = {
        'changed': False,
        'ansible_facts': {
            'dladm_' + attr + '_list': [],
        },
    }

    try:
        command = None
        bin_path = None
        for c in sorted(commands_map):
            bin_path = module.get_bin_path(c, required=False)
            if bin_path is not None:
                command = c
                break

        if bin_path is None:
            raise EnvironmentError(msg='Unable to find any of the supported commands in PATH: {0}'.format(", ".join(sorted(commands_map))))

        args = commands_map[command]['args']
        rc, stdout, stderr = module.run_command([bin_path] + args)
        if rc == 0:
            parse_func = commands_map[command]['parse_func']
            results = parse_func(stdout)

            for net in results:
                result['ansible_facts']['dladm_' + attr + '_list'].append(net)
    except (KeyError, EnvironmentError) as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
