## netbox-ip-monitor

Visual representation of IP addresses

IP monitor to display all IP addresses in a prefix

> The monitor does not display IP addresses in IPv6, container and overly large (</24) prefixes.

![alt text](docs/images/ip_monitor.png "IP Monitor")

## Compatibility

| NetBox Version| Plugin Version|
|---------------|---------------|
| 4.2           | >= 0.0.0      |
| 3.X           | 0.0.0         |


## Installation

The plugin is available as a [Python package](https://pypi.org/project/netbox-ip-monitor/) in PyPI and can be installed with pip
```
source /opt/netbox/venv/bin/activate
python3 -m pip install netbox-ip-monitor
# or
# python3 -m pip install netbox-ip-monitor==<version>
```

Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_ip_monitor']
```

Run collectstatic:
```
python3 manage.py collectstatic --no-input
```

To ensure the plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the NetBox root directory (alongside `requirements.txt`) and append the `netbox-ip-monitor` package:

```no-highlight
echo netbox-ip-monitor >> local_requirements.txt
```