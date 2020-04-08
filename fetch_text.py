"""
Fetch NWS test products from their FTP servers

Matt Nicholson
7 April 2020
"""
import shutil
from ftplib import FTP

import config


def open_ftp():
    """
    Open and return a connection to the FTP server to be used to retrieve
    multiple text products

    Parameters
    ----------
    None

    Returns
    -------
    Instance of the ftplib.FTP class
    """
    ftp = FTP(config.FPT_URL.ftp_base)
    ftp.login()
    return ftp


def download_binary(ftp, target_file, outfile):
    """
    Download a file from the FTP server in binary transfer mode.

    Parameters
    ----------
    ftp : ftplib.FTP object
        Connection to the FTP server.
    target_file : str
        Name of the file to download from the FTP server.
    outfile : str
        Filename of the file to write to.
    """
    with open(outfile, 'wb') as f_handler:
        ftp.retrbinary('RETR {}'.format(target_file), f_handler.write)


def fetch_zone_forecast(ftp):
        """
        Retrieve zone forecast text product.

        Parameters
        ----------
        ftp : ftplib.FTP object
            FTP connection to the NWS FTP server

        Returns
        -------
        None
        """
        for state, zone in config.FCST_ZONES.items():
            ftp.cwd('~/' + config.FPT_URL.fz_base + '/' + state)
            if isinstance(zone, list):
                for z in zone:
                    target_file = z + '.txt'
                    outfile = 'temp/zone_forecast-' + target_file
                    download_binary(ftp, target_file, outfile)
            else:
                target_file = zone + '.txt'
                outfile = 'temp/zone_forecast-' + target_file
                download_binary(ftp, target_file, outfile)


def fetch_forecast_disc(ftp):
    """
    Retrieve forecasters discussion text product.

    Parameters
    ----------
    ftp : ftplib.FTP object
        FTP connection to the NWS FTP server

    Returns
    -------
    None
    """
    ftp.cwd('~/' + config.FPT_URL.fx_base)
    for disc in config.FCST_DISCS:
        target_file = disc + '.txt'
        outfile = 'temp/forecast_discussion-' + target_file
        download_binary(ftp, target_file, outfile)


def fetch_metar(ftp):
    """
    Retrieve METAR text files

    Parameters
    ----------
    ftp : ftplib.FTP object
        FTP connection to the NWS FTP server

    Returns
    -------
    None
    """
    ftp.cwd('~/' + config.FPT_URL.metar_base)
    for station in config.METARS:
        target_file = station + '.TXT'      # Not a typo
        outfile = 'temp/METAR-' + target_file
        outfile = outfile.replace('TXT', 'txt')
        download_binary(ftp, target_file, outfile)


if __name__ == '__main__':
    ftp = open_ftp()
    # fetch_zone_forecast(ftp)
    # fetch_forecast_disc(ftp)
    fetch_metar(ftp)
    ftp.quit()
