# coding=utf-8
#
# From https://github.com/mk-fg/sht-sensor

import math

def dewpoint(t, rh):
    dict_tn = dict(water=243.12, ice=272.62) # Table 9
    dict_m = dict(water=17.62, ice=22.46) # Table 9
    if t is None: t, rh = self.read_t(), None
    if rh is None: rh = self.read_rh(t)
    t_range = 'water' if t >= 0 else 'ice'
    tn, m = dict_tn[t_range], dict_m[t_range]
    if rh/100.0 <= 0:
        # Cannot perform log on 0 or negative number
        return None
    else:
        return (
            tn * (math.log(rh / 100.0) + (m * t) / (tn + t))
            / (m - math.log(rh / 100.0) - m * t / (tn + t)) )


def c_to_f(temperture_c):
    return 9.0/5.0 * temperture_c + 32
