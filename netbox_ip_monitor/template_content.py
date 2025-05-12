import ipaddress
import netaddr

from netbox.settings import VERSION
if VERSION.startswith("3."):
    from extras.plugins import PluginTemplateExtension
else:
    from netbox.plugins import PluginTemplateExtension
from ipam.choices import PrefixStatusChoices
from ipam.models import IPAddress, Prefix


class IPMonitorPrefix(PluginTemplateExtension):
    model = "ipam.prefix"

    @staticmethod
    def get_ips(prefix_obj):
        """
        Return all IPs within this prefix as an IPSet.
        """
        prefix = netaddr.IPSet(prefix_obj.prefix)
        child_ranges = netaddr.IPSet([iprange.range for iprange in prefix_obj.get_child_ranges().filter(mark_populated=True)])
        ips = prefix - netaddr.IPSet(child_ranges)

        # IPv6 /127's, pool, or IPv4 /31-/32 sets are fully usable
        if (prefix_obj.family == 6 and prefix_obj.prefix.prefixlen >= 127) or prefix_obj.is_pool or (prefix_obj.family == 4 and prefix_obj.prefix.prefixlen >= 31):
            return ips

        if prefix_obj.family == 4:
            # For "normal" IPv4 prefixes, omit first and last addresses
            ips -= netaddr.IPSet([
                netaddr.IPAddress(prefix_obj.prefix.first),
                netaddr.IPAddress(prefix_obj.prefix.last),
            ])
        else:
            # For IPv6 prefixes, omit the Subnet-Router anycast address
            # per RFC 4291
            ips -= netaddr.IPSet([netaddr.IPAddress(prefix_obj.prefix.first)])
        return ips

    def get_different_parts(self, ip_address):
        """
        Returns the part of the IP address that differs in the subnet
        """
        subnet = ipaddress.IPv4Network(self.context["object"], strict=False)
        ip = ipaddress.IPv4Address(ip_address)

        network_address = subnet.network_address
        network_int = int(network_address)
        ip_int = int(ip)

        different_part = ip_int - network_int
        return "." + str(different_part)

    def left_page(self):
        prefix = Prefix.objects.get(prefix=str(self.context["object"]))
        if (
            prefix.status == PrefixStatusChoices.STATUS_CONTAINER
            or prefix.family == 6
            or prefix.prefix.prefixlen < 24
        ):
            return ""
        else:
            ip_addresses = list(self.get_ips(prefix))
            child_ips = prefix.get_child_ips()

            for i in range(len(ip_addresses)):
                for j in child_ips:
                    if str(j.address.ip) == str(ip_addresses[i]):
                        ip_addresses[i] = j
                        ip_addresses[i].short_ip = self.get_different_parts(
                            j.address.ip
                        )
                if type(ip_addresses[i]) is not IPAddress:
                    ip_addresses[i] = {
                        "ip": ip_addresses[i],
                        "short_ip": self.get_different_parts(str(ip_addresses[i])),
                    }

            output = self.render(
                "netbox_ip_monitor/ip_monitor.html",
                extra_context={
                    "prefix": self.context["object"],
                    "ip_addresses": ip_addresses,
                },
            )
            return output


template_extensions = [IPMonitorPrefix]
