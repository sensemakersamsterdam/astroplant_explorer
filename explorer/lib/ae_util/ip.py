"""
ae_util IP utilities.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

import os


class IP_Utils:
    @staticmethod
    def get_ip_addresses():
        """Get a list of all IPV4 IP addresses on a default route and their metrics.
        Sort with the least cost one first. 
        """
        address_list = []
        try:
            with os.popen('/bin/ip -4 route') as f:
                for line in f.readlines():
                    fields = line.strip().split(' ')
                    if fields[0] == 'default':
                        pos = fields.index('metric')
                        ip = fields[pos-1]
                        metric = fields[pos+1]
                        address_list.append((metric, ip))
        except Exception as ex:
            print(ex)
        return sorted(address_list)

    @staticmethod
    def get_main_ip_address():
        """Return the IP address on the cheapest default route.
        Return None if no IP address found.
        """
        al = IP_Utils.get_ip_addresses()
        if len(al) > 0:
            # Return the one with the least cost.
            return al[0][1]
        else:
            return None

    @staticmethod
    def ping(ip_address):
        """Ping a host or ip_address. Return True if reachable.
        """
        return not os.system('/bin/ping -n -c 1 -4 2>&1 1>/dev/null ' + ip_address)
