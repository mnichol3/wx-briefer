"""
Fetch National Airspace System information from the FAA Air Traffic Control
System Command Center (ATCSCC) OIS System

Matt Nicholson
9 Feb 2020
"""
import certifi
import urllib3
import requests
from bs4 import BeautifulSoup

url_ois = 'https://www.fly.faa.gov/ois/jsp/summary_sys.jsp'
url_adv = 'https://www.fly.faa.gov/adv/adv_spt.jsp'

fetch_ops_adv(url):
    """
    Fetch the FAA ATCSCC Current Operations Plan Advisory

    Parameters
    -----------
    url : str
        URL of the ATCSCC ops advisory
    """
    f_name = 'ois_out.txt'
    dir_out = './output'
    f_out = os.path.join(dir_out, f_name)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")

    with open(f_out, 'w') as f_out:
        f_out.write(soup.pre.contents[0].strip())
