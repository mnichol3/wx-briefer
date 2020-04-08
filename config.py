# --- Graphical Products -------------------------------------------------------
class IMG_URL:
    """
    URLS for graphical products.
    """
    sfc_analysis    = ['https://www.wpc.ncep.noaa.gov/sfc/namussfcwbg.jpg']

    conv_outlook    = ['https://www.spc.noaa.gov/products/outlook/day1otlk.html',
                       'https://www.spc.noaa.gov/products/outlook/day2otlk.html']

    fire_outlook    = ['https://www.spc.noaa.gov/products/fire_wx/fwdy1.html',
                       'https://www.spc.noaa.gov/products/fire_wx/fwdy2.html']

    natl_fcst_chart = ['https://www.wpc.ncep.noaa.gov/national_forecast/natfcst.php']

    shrt_rng_fcst   = ['https://www.wpc.ncep.noaa.gov/basicwx/basicwx_ndfd.php']

    snow_composite  = ['https://www.wpc.ncep.noaa.gov/wwd/day1_composite.gif',
                       'https://www.wpc.ncep.noaa.gov/wwd/day2_composite.gif',
                       'https://www.wpc.ncep.noaa.gov/wwd/day3_composite.gif']

    qpf             = ['https://www.wpc.ncep.noaa.gov/qpf/qpf1.shtml',
                       'https://www.wpc.ncep.noaa.gov/qpf/day2.shtml',
                       'https://www.wpc.ncep.noaa.gov/qpf/day3.shtml']

    wpc_base        = 'https://www.wpc.ncep.noaa.gov'


# --- Text Products ------------------------------------------------------------

class FPT_URL:
    """
    FTP urls.
    fz = zone forecast, fx = forecasters dicsussion.
    """
    ftp_base = 'tgftp.nws.noaa.gov'
    fz_base  = 'data/forecasts/zone'
    fx_base  = 'data/raw/fx'
    metar_base = 'data/observations/metar/stations'


"""
Zones for zone forecast text product.
Key : State directory
Val : State forecast zone (doubles as the filename on the ftp server)
"""
FCST_ZONES = {'md': 'mdz014'}


"""
Forecasters discussions
"""
FCST_DISCS = ['fxus61.klwx.afd.lwx']


"""
METAR Stations
"""
METARS = ['KIAD', 'KDCA', 'KBWI']
