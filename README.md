<meta name="author" content="Marco Noce">
<meta name="description" content="Gathers facts about Solaris dladm show attributes on Solaris 11.">
<meta name="copyright" content="Marco Noce 2024">
<meta name="keywords" content="ansible, module, solaris, dladm, show, aggr, link, vnic, ether, phys, attribute">

<div align="center">

![Ansible Custom Module][ansible-shield]
![Oracle Solaris][solaris-shield]
![python][python-shield]
![license][license-shield]

</div>


### dladm_show_facts ansible custom module
#### Gathers facts about Solaris dladm show attributes.

#### Description :

<b>dladm_show_facts</b> is a custom module for ansible that creates an ansible_facts containing the attribute list of dladm show on a SunOS/Oracle Solaris 11 host.

#### Repo files:

```
├── /library                
│   └── dladm_show_facts.py     ##<-- python custom module
└── dladm_show.yml              ##<-- ansible playbook example for Solaris 11 release
```

#### Requirements :

*  This module supports SunOS/Oracle Solaris 11 only
*  The dladm info are gathered from the [dladm] command on Solaris 11.x

Module supports :
* dladm show-aggr
* dladm show-link
* dladm show-vnic
* dladm show-ether
* dladm show-phys


#### Parameters :

|Parameter|Type         |Required|Sample                             |Comment             |
|---------|-------------|--------|-----------------------------------|--------------------|
|attribute|string/choice|True    |'aggr' 'link' 'vnic' 'ether' 'phys'|The dladm show type | 

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|
|facts     |full   |Action returns an ansible_facts dictionary that will update existing host facts.    |

#### Examples :

#### Tasks
```yaml
---
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
```
#### facts list example
#### dladm show-link facts:
```json
  "ansible_facts": {
    "dladm_link_list": [
      {
        "LINK": "net0",
        "CLASS": "phys",
        "MTU": "1500",
        "STATE": "up",
        "OVER": "--"
      },
      {
        "LINK": "net1",
        "CLASS": "phys",
        "MTU": "1500",
        "STATE": "up",
        "OVER": "--"
      }
    ]
  },
```
#### dladm show-ether facts:
```json
  "ansible_facts": {
    "dladm_ether_list": [
      {
        "LINK": "net0",
        "PTYPE": "current",
        "STATE": "up",
        "AUTO": "yes",
        "SPEED-DUPLEX": "1G-f",
        "PAUSE": "bi"
      },
      {
        "LINK": "net1",
        "PTYPE": "current",
        "STATE": "up",
        "AUTO": "yes",
        "SPEED-DUPLEX": "1G-f",
        "PAUSE": "bi"
      }
    ]
  },
```
#### dladm show-phys facts:
```json
  "ansible_facts": {
    "dladm_phys_list": [
      {
        "LINK": "net0",
        "MEDIA": "Ethernet",
        "STATE": "up",
        "SPEED": "1000",
        "DUPLEX": "full",
        "DEVICE": "e1000g0"
      },
      {
        "LINK": "net1",
        "MEDIA": "Ethernet",
        "STATE": "up",
        "SPEED": "1000",
        "DUPLEX": "full",
        "DEVICE": "e1000g1"
      }
    ]
  },
```
#### debug output from example :
```
TASK [print state, device and speed-duplex of net0] *****************************************
ok: [sol11host] => {
    "msg": "net0 is up on e1000g0 at 1G-f speed"
}
```
#### Returned Facts :

*  Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.
*  Attributes change according to attribute selected.

|Key              |Type                  |Description                        |Returned                |Sample              |
|-----------------|----------------------|-----------------------------------|------------------------|--------------------|
|dladm_aggr_list  |list / elements=string|dladm attribute list.              |if attribute is aggr    |                    |
|LINK             |string                |The link name.                     |always                  |"aggr1"             |
|MODE             |string                |The link mode.                     |always                  |"trunk"             |
|POLICY           |string                |The link policy.                   |always                  |"L4"                |
|ADDRPOLICY       |string                |The link address policy.           |always                  |"auto"              |
|LACPACTIVITY     |string                |The lacp activity.                 |always                  |"active"            |
|LACPTIMER        |string                |The lacp timer.                    |always                  |"short"             |
|dladm_link_list  |list / elements=string|dladm attribute list.              |if attribute is link    |                    |
|LINK             |string                |The link name.                     |always                  |"net0"              |
|CLASS            |string                |The link class.                    |always                  |"phys"              |
|MTU              |string                |The link MTU.                      |always                  |"1500"              |
|STATE            |string                |The link state.                    |always                  |"up"                |
|OVER             |string                |The over interface of link.        |always                  |"--"                |
|dladm_vnic_list  |list / elements=string|dladm attribute list.              |if attribute is vnic    |                    |
|LINK             |string                |The link name.                     |always                  |"ldoms-vsw0.vport0" |
|OVER             |string                |The over interface of link.        |always                  |"net0"              |
|SPEED            |string                |The link speed.                    |always                  |"1000"              |
|MACADDRESS       |string                |The link mac address.              |always                  |"0:11:4f:fa:e1:f5"  |
|MACADDRTYPE      |string                |The link mac address type.         |always                  |"fixed"             |
|IDS              |string                |The link IDS.                      |always                  |"VID:0,415"         |
|dladm_ether_list |list / elements=string|dladm attribute list.              |if attribute is ether   |                    |
|LINK             |string                |The link name.                     |always                  |"net0"              |
|PTYPE            |string                |The link property type.            |always                  |"current"           |
|STATE            |string                |The link state.                    |always                  |"up"                |
|AUTO             |string                |The link auto.                     |always                  |"yes"               |
|SPEED-DUPLEX     |string                |The link speed duplex.             |always                  |"1G-f"              |
|PAUSE            |string                |The link pause.                    |always                  |"bi"                |
|dladm_phys_list  |list / elements=string|dladm attribute list.              |if attribute is phys    |                    |
|LINK             |string                |The link name.                     |always                  |"net0"              |
|MEDIA            |string                |The link type.                     |always                  |"Ethernet"          |
|STATE            |string                |The link state.                    |always                  |"up"                |
|SPEED            |string                |The link speed.                    |always                  |"1000"              |
|DUPLEX           |string                |The link duplex.                   |always                  |"full"              |
|DEVICE           |string                |The link device.                   |always                  |"ixgbe4"            |


## SANITY TEST

* Ansible sanity test is available in [SANITY.md] file

## Integration

1. Assuming you are in the root folder of your ansible project.

Specify a module path in your ansible configuration file.

```shell
$ vim ansible.cfg
```
```ini
[defaults]
...
library = ./library
...
```

Create the directory and copy the python modules into that directory

```shell
$ mkdir library
$ cp path/to/module library
```

2. If you use Ansible AWX and have no way to edit the control node, you can add the /library directory to the same directory as the playbook .yml file

```
├── root repository
│   ├── playbooks
│   │    ├── /library                
│   │    │   └── dladm_show_facts.py        ##<-- python custom module
│   │    └── your_playbook.yml              ##<-- you playbook
```   

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[solaris-shield]: https://img.shields.io/badge/oracle-solaris-red?style=for-the-badge&logo=oracle&logoColor=red
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow
[license-shield]: https://img.shields.io/github/license/nomakcooper/svcs_attr_facts?style=for-the-badge&label=LICENSE


[dladm]: https://docs.oracle.com/cd/E26502_01/html/E28987/ggtuo.html
[SANITY.md]: SANITY.md
