# Cloudflare dynamic dns update script 8.27.2022 by Mike Smith
import requests 
import json
from dotenv import load_dotenv
import os

load_dotenv()

CLOUDFLARE_URL = "https://api.cloudflare.com/client/v4/"
PUB_IP_URL = "https://ifconfig.me/ip"
CF_TOKEN = os.environ.get('CF_TOKEN')
ZONE_ID = os.environ.get("ZONE_ID")
RECORD_ID = os.environ.get("RECORD_ID")
SITE_URL = os.environ.get("SITE_URL")

HEADERS = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json",
    }

def need_update(pub_ip, cf_ip):
    """Returns True if pub_ip == cf_ip"""

    return pub_ip == cf_ip


def get_pub_ip(): 
    """Fetches public IP and returns STR of ip address"""

    r = requests.get(PUB_IP_URL)
    return str(r.text)


def get_cf_data():
    """Returns A record IP from Cloud flare"""

    params = {
        "name": f"{SITE_URL}",
        
    }

    r = requests.get(
        url= f"{CLOUDFLARE_URL}zones/{ZONE_ID}/dns_records",
        headers=HEADERS,
        params=params,

    )
    a_record_ip = r.json()['result'][0]['content']

    return a_record_ip


def update_cf_dns(my_ip):
    """Function updates CF root A record"""

    update_params = {
        "type": "A", 
        "name": f"{SITE_URL}", 
        "content": f"{my_ip}", 
        "ttl": 1, 
        "proxied": bool("true"),
        }

    data = json.dumps(update_params)

    up = requests.put(
        url = f"{CLOUDFLARE_URL}zones/{ZONE_ID}/dns_records/{RECORD_ID}", 
        headers=HEADERS,
        data= data ,
        
    ) 

    return up.json()


if __name__ == "__main__":

    pub_ip = get_pub_ip()
    if not need_update(pub_ip=pub_ip, cf_ip=get_cf_data()):
            update_cf_dns(pub_ip)
            print(f'Updated A record with {pub_ip}')



