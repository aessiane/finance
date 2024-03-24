#
# Copyright (c) 2023 LateGenXer
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#


# https://taxsummaries.pwc.com/portugal/individual/taxes-on-personal-income
income_tax_bands = [
   (  7703, 0.1325),
   ( 11623, 0.1800),
   ( 16472, 0.2300),
   ( 21321, 0.2600),
   ( 27146, 0.3275),
   ( 39791, 0.3700),
   ( 51997, 0.4350),
   ( 80000, 0.4500),
   ( 81199, 0.4500 + 0.025),
   (250000, 0.4800 + 0.025),
   (  None, 0.4800 + 0.050),
]


cgt_rate = 0.28


def income_tax(gross_income, factor=1.0):
    tax = 0
    lbound = 0
    for ubound, rate in income_tax_bands:
        delta = max(gross_income - lbound, 0)
        if ubound is not None:
            ubound *= factor
            delta = min(delta, ubound - lbound)
        tax += delta * rate
        lbound = ubound
    assert tax <= gross_income
    return tax
