import os
import certifi
import urllib3
import requests
import re
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

URLS = {
    "sfc_analysis"    : ["https://www.wpc.ncep.noaa.gov/sfc/namussfcwbg.jpg"],

    "conv_outlook"    : ["https://www.spc.noaa.gov/products/outlook/day1otlk.html",
                         "https://www.spc.noaa.gov/products/outlook/day2otlk.html"],

    "fire_outlook"    : ["https://www.spc.noaa.gov/products/fire_wx/fwdy1.html",
                         "https://www.spc.noaa.gov/products/fire_wx/fwdy2.html"],

    "natl_fcst_chart" : ["https://www.wpc.ncep.noaa.gov/national_forecast/natfcst.php"],

    "shrt_rng_fcst"   : ["https://www.wpc.ncep.noaa.gov/basicwx/basicwx_ndfd.php"],

    "snow_composite"  : ["https://www.wpc.ncep.noaa.gov/wwd/day1_composite.gif",
                         "https://www.wpc.ncep.noaa.gov/wwd/day2_composite.gif",
                         "https://www.wpc.ncep.noaa.gov/wwd/day3_composite.gif"],

    "qpf"             : ["https://www.wpc.ncep.noaa.gov/qpf/qpf1.shtml",
                         "https://www.wpc.ncep.noaa.gov/qpf/day2.shtml",
                         "https://www.wpc.ncep.noaa.gov/qpf/day3.shtml"],

    "wpc_base"        : "https://www.wpc.ncep.noaa.gov"
}


def download_image(url, f_name, format):
    """
    Downloads an image via url

    Parameters
    ----------
    url : str
        URL of the image to download
    f_name : str
        Name to download the image as
    format : str
        Image file format
    """
    r = requests.get(url)
    i = Image.open(BytesIO(r.content))
    i.save(f_name, format=format)


def parse_sfc_analysis(url_dict, fname_dict):
    """
    Fetch the WPC Surface Analysis Chart

    Pretty straight forward as the image is uploaded under the same filename
    regardless of the date

    Parameters
    ----------
    url_dict : dict (str, list of str)

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    f_name = 'temp/sfc_analysis.png'
    url = url_dict["sfc_analysis"][0]
    print("Fetching WPC Surface Analysis...")
    download_image(url, f_name, 'PNG')
    fname_dict['sfc_analysis'] = f_name
    return fname_dict


def parse_conv_outlook(url_dict, fname_dict):
    """
    Fetch the Day 1 & Day 2 SPC Convective Outlooks

    Parameters
    ----------
    url_dict : dict (str, list of str)
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    time_re = r'\d{4} (\d{4}) UTC Day'
    f_names = ['temp/conv_outlk_d1.gif', 'temp/conv_outlk_d2.gif']
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    for idx, url in enumerate(url_dict["conv_outlook"]):
        idx_adj = idx + 1
        print("Fetching Day {} SPC Convective Outlook...".format(idx_adj))
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, features="html.parser")
        # Find the filename of the img
        tags = soup.find("td", {"class": "zz"})
        # Extract the validity time of the current image
        match = re.search(time_re, tags.contents[0])
        if (match):
            valid_time = match.group(1)
        # Modify original url to go directly to the image
        url = url.replace(".html", "")
        url += '_{}.gif'.format(valid_time)
        download_image(url, f_names[idx], 'GIF')
    fname_dict['conv_outlk_d1'] = f_names[0]
    fname_dict['conv_outlk_d2'] = f_names[1]
    return fname_dict


def parse_conv_outlook_simple(fname_dict):
    """
    Fetch the Day 1 & Day 2 SPC Convective Outlooks via the GIF image url

    Parameters
    ----------
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    base_url = 'https://www.spc.noaa.gov/products/outlook/day{}otlk.gif'
    f_names = ['temp/conv_outlk_d1.gif', 'temp/conv_outlk_d2.gif']
    for day in [1, 2]:
        idx = day - 1
        curr_url = base_url.format(day)
        download_image(curr_url, f_names[idx], 'GIF')
        fname_dict['conv_outlk_d{}'.format(day)] = f_names[idx]
    return fname_dict


def parse_shortrange_fsct(url_dict, fname_dict):
    """
    Fetch shortrange forecast graphics for hour 6, 12, 18, & 24.

    Parameters
    -----------
    url_dict : dict (str, list of str)
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    base_url = url_dict["shrt_rng_fcst"][0].rsplit('/', 1)[0]
    # !!! DO NOT REMOVE soup_url !!!
    soup_url = "https://www.wpc.ncep.noaa.gov/basicwx/basic_sfcjpg.shtml"
    hrs = [6, 12, 18, 24]
    img_fnames = []

    valid_re = re.compile("(\d{1,2}-hour fcst valid \d{2} or \d{2} UTC)")
    img_re = re.compile("/(\w+)_sm")

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', soup_url)
    soup = BeautifulSoup(response.data, features="html.parser")
    tags = soup.find_all("img", {"alt": re.compile(valid_re)})
    # Only get up to 24 hrs
    for idx, period in enumerate(tags[:4]):
        curr_hr = hrs[idx]
        print("Fetching WPC Short Range Fcst hr {}...".format(curr_hr))
        img_src = period.get("src")
        match = re.search(img_re, img_src)
        if (match):
            img_name = match.group(1)
            img_url = base_url + '/{}.gif'.format(img_name)
            f_name = "temp/shrt_rng_{}.gif".format(curr_hr)
            download_image(img_url, f_name, "GIF")
            fname_dict["shrt_rng_{}".format(curr_hr)] = f_name
    return fname_dict


def parse_nat_fcst_chart(url_dict, fname_dict):
    """
    Fetch the WPC National Forecast Chart image

    Parameters
    -----------
    url_dict : dict (str, list of str)
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    url = url_dict["natl_fcst_chart"][0]
    src_re = re.compile("/noaa/noaad\d.gif\?\d+")

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    tags = soup.find_all("img", {"src": src_re})[0]
    base_ext = tags.get("src")
    f_names = [base_ext,
               base_ext.replace("noaad1", "noaad2"),
               base_ext.replace("noaad1", "noaad3")
              ]
    url = url.rsplit('/', 2)[0]
    for idx, f_name in enumerate(f_names):
        idx_adj = idx + 1
        print("Fetching Day {} WPC National Forecast Chart...".format(idx_adj))
        curr_url = url + '/{}'.format(f_name)
        curr_fname = "temp/nat_fsct_chart_{}.gif".format(idx_adj)
        download_image(curr_url, curr_fname, "GIF")
        fname_dict["nat_fsct_chart_{}".format(idx_adj)] = curr_fname
    return fname_dict


def fetch_fire_outlook(fname_dict):
    """
    Fetch the Day 1 & Day 2 SPC Fire Outlooks via the GIF image url

    Parameters
    ----------
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    base_url = 'https://www.spc.noaa.gov/products/fire_wx/day{}otlk_fire.gif'
    f_names = ['temp/fire_outlk_d1.gif', 'temp/fire_outlk_d2.gif']
    for day in [1, 2]:
        print("Fetching Day {} Fire Outlook...".format(day))
        idx = day - 1
        curr_url = base_url.format(day)
        download_image(curr_url, f_names[idx], 'GIF')
        fname_dict['fire_outlk_d{}'.format(day)] = f_names[idx]
    return fname_dict


def fetch_snow_composite(url_dict, fname_dict):
    """
    Fetch the WPC Snowfall Composite graphic for Day 1, 2, & 3

    Parameters
    -----------
    url_dict : dict (str, list of str)
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """
    f_names = ['temp/snow_comp_d1.gif', 'temp/snow_comp_d2.gif', 'temp/snow_comp_d3.gif']
    for idx, url in enumerate(url_dict['snow_composite']):
        day = idx + 1
        print("Fetching Day {} Snowfall Composite...".format(day))
        download_image(url, f_names[idx], 'GIF')
        fname_dict['snow_comp_d{}'.format(day)] = f_names[idx]
    return fname_dict


def fetch_qpf(url_dict, fname_dict):
    """
    Fetch WPC Quantitative Precip Forecast (QPF) graphics

    Parameters
    -----------
    url_dict : dict (str, list of str)
    fname_dict : dict (str, str)
        Dictionary containing local filenames

    Returns
    -------
    fname_dict : dict (str, str)
        Dictionary containing local filenames
    """

    for idx, url in enumerate(url_dict["qpf"]):
        idx_adj = idx + 1
        print("Fetching Day {} QPF...".format(idx_adj))
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, features="html.parser")
        tags = soup.find_all("a", {"id": "day{}".format(idx_adj)})[0]
        curr_url = url_dict["wpc_base"]
        print(tags)


def main():
    f_names = {}

    fetch_fire_outlook(f_names)
    fetch_snow_composite(URLS, f_names)
    # parse_sfc_analysis(URLS, f_names)
    #
    # parse_conv_outlook(URLS, f_names)
    #
    # parse_shortrange_fsct(URLS, f_names)
    # parse_nat_fcst_chart(URLS, f_names)


    #fetch_qpf(URLS, f_names)



if __name__ == '__main__':
    main()
