import unittest 
import re 
import sys 
from ipaddress import ip_address

#sys.path.append("../")

from ddns import get_pub_ip, get_cf_data


class TestDDNS(unittest.TestCase):
    """tests if an IP address is returned"""


    def test_get_pub_ip(self):
        """Verifies an IP is returned from get_pub_ip()"""

        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        match = re.match(ip_pattern, get_pub_ip())

        self.assertTrue(match)


    def test_get_cf_data(self):

        self.assertRaises(ConnectionError, get_cf_data)


unittest.main()




