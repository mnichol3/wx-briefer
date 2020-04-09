"""
Functions to generate the brief PDF file.

Matt Nicholson
8 April 2020
"""
from fpdf import FPDF
from datetime import datetime,timezone


def fetch_datetime():
    """
    Return the current date & time (UTC) as a string.

    Parameters
    ----------
    None

    Returns
    -------
    str
        Current date. Format: DD Month YYYY.
    """
    now = datetime.now(timezone.utc)
    return now.strftime('%d %b %Y %H%Mz')


def generate_pdf():
    """
    Generate the briefing PDF.

    Parameters
    ----------
    None

    Returns
    -------
    Idk

    Notes
    -----
    * Unit of measurement is mm
    """
    # --- Configure PDF settings
    pdf = FPDF(format='Letter')
    pdf.set_margins(12.7, 12.7, 12.7)       # 0.5 inch margins
    pdf.set_fill_color(224, 224, 224)
    pdf.add_page()
    # --- Write title
    pdf.set_font('Courier', size=14)#, style='B')
    txt = 'Weather Brief - ' + fetch_datetime()
    pdf.cell(0, 10, txt=txt, ln=1, align='C', fill=True, border=1)
    pdf.output('simple_demo.pdf')

generate_pdf()
