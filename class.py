from ssl import _create_default_https_context
import requests

class DynDNS:
    """Methods for updating dynamic DNS"""

    def __init__(self) -> None:

        self.ip_urls = [
            "https://api.ipify.org", 
            "https://ifconfig.me/ip", 
            "https://ip.seeip.org", 
            #"https://api.bigdatacloud.net/data/client-ip"
        ]
        
        self.log_path = "./ddns.log"

    def get_pub_ip(self):
        """Returns public IP"""

        pub_ip = set() # [requests.get(url).text for url in self.ip_urls ]

        for url in self.ip_urls:

            try: 
                r = requests.get(url)

                if not r.raise_for_status():
                    pub_ip.add(r.text)
                else:
                    raise "Weird response from server"
            except ConnectionError:
                self.update_logs("LOG: Unable to connect")
            
        if pub_ip:
            self.update_logs(f"LOG: PubIP {pub_ip}")

    def update_logs(self, message):
        """writes to log_path"""

        with open(self.log_path, 'a') as f:
            f.writelines(message)





test = DynDNS()

test.get_pub_ip()

