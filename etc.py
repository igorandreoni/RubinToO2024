# author: Igor Andreoni <igor.andreoni@gmail.com.>
# Formulae from https://smtn-002.lsst.io/v/OPSIM-1134/index.html

import numpy as np

params = {
          "u": {"Cm": 22.97,
                "dCm_inf": 0.54,
                "zp": 26.52,
                "fwhm": 0.92,
                "m_darksky": 23.05,
                "k_atm": 0.47
                },
          "g": {"Cm": 24.58,
                "dCm_inf": 0.09,
                "zp": 28.51,
                "fwhm": 0.87,
                "m_darksky": 22.25,
                "k_atm": 0.21
                },
          "r": {"Cm": 24.6,
                "dCm_inf": 0.04,
                "zp": 28.36,
                "fwhm": 0.83,
                "m_darksky": 21.2,
                "k_atm": 0.13
                },
          "i": {"Cm": 24.54,
                "dCm_inf": 0.03,
                "zp": 28.17,
                "fwhm": 0.80,
                "m_darksky": 20.46,
                "k_atm": 0.10
                },
          "z": {"Cm": 24.37,
                "dCm_inf": 0.02,
                "zp": 27.78,
                "fwhm": 0.78,
                "m_darksky": 19.61,
                "k_atm": 0.07
                },
          "y": {"Cm": 23.84,
                "dCm_inf": 0.02,
                "zp": 26.82,
                "fwhm": 0.76,
                "m_darksky": 18.6,
                "k_atm": 0.17
                }
          }


def get_exptime(m5, filt, X=1.):
    """
    Given a certain depth, return the exposure time

    Parameters
    ----------
    m5 float
        depth 5sigma (mag)
    filt str
        filter (one of ugrizy)
    X float
        airmass

    Returns
    -------
    exptime float
        exposure time to reach limiting magnitude
    """
    # assign the parameters to variables
    Cm = params[filt]["Cm"]
    k_atm = params[filt]["k_atm"]
    fwhm = params[filt]["fwhm"]
    m_darksky = params[filt]["m_darksky"]
    # Important: assuming darksky
    m_sky = m_darksky
    # FIXME approximation dCm=0 (fine within 0.3s for 30s exposures)
    # dCm_inf = params[filt]["dCm_inf"]
    # Tscale = exptime / 30. * 10**(-1 * 0.4 * (m_sky - m_darksky))
    # dCm = dCm_inf - 1.25 * np.log10(1 + (10**(0.8 * dCm_inf) - 1) / Tscale)
    dCm = 0
    # Calculate the exposure time
    exptime = 30 * 10 ** ((1 / 1.25) * (m5 - Cm - dCm - 0.5 * (m_sky - 21.) -
                                        2.5 * np.log10(0.7 / fwhm) +
                                        k_atm*(X - 1.0)))

    return exptime


def get_m5(exptime, filt, X=1.):
    """
    Given a certain exposure time return 5sigma depth
    Parameters
    ----------
    exptime int or float
        exposure time
    filt str
        filter (one of ugrizy)
    X float
        airmass

    Returns
    -------
    m5 float
        5sigma limiting magnitude
    """
    # assign the parameters to variables
    Cm = params[filt]["Cm"]
    dCm_inf = params[filt]["dCm_inf"]
    k_atm = params[filt]["k_atm"]
    fwhm = params[filt]["fwhm"]
    m_darksky = params[filt]["m_darksky"]
    # Important: assuming darksky
    m_sky = m_darksky
    # Calculate m5
    Tscale = exptime / 30. * 10**(-1 * 0.4 * (m_sky - m_darksky))
    dCm = dCm_inf - 1.25 * np.log10(1 + (10**(0.8 * dCm_inf) - 1) / Tscale)
    m5 = Cm + dCm + 0.5 * (m_sky - 21.) + 2.5 * np.log10(0.7 / fwhm) + \
        1.25 * np.log10(exptime / 30.) - k_atm*(X - 1.0)

    return m5


if __name__ == "__main__":
    # Testing getting exptime given a list of mag limits
    m5s = [23.70, 24.97, 24.52, 24.13, 23.56, 22.55]
    for m5, filt in zip(m5s, "ugrizy"):
        # m5_out = get_m5(exptime, filt, X=1.)
        exptime_out = get_exptime(m5, filt, X=1.)
        # print('{:.2f}'.format(m5_out))
        print('{:.2f}'.format(exptime_out))
