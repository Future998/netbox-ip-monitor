from netbox.plugins import PluginConfig


class NetBoxIPMonitorConfig(PluginConfig):
    name = 'netbox_ip_monitor'
    verbose_name = ' NetBox IP Monitor'
    description = 'Visual representation of IP addresses'
    version = '0.1.1'
    base_url = 'ip-monitor'
    author = 'Alexander Burmatov'
    author_email = 'burmatov202002@gmail.com'
    min_version = '4.3.0'
    max_version = '4.4.99'

config = NetBoxIPMonitorConfig