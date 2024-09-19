#
# Copyright (c) 2024 LateGenXer
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#


import streamlit as st

import common

from rtp.uk import state_pension_full

import annuities


common.set_page_config(
    page_title="Annuity Valuator",
)

st.title('Annuity Valuator')


st.markdown('''This tool calculates the [Actuary Present Value](https://en.wikipedia.org/wiki/Actuarial_present_value) of an annuity.  It uses:
- Institute and Faculty of Actuaries' [Unisex mortality rates](https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/other-cmi-outputs/unisex-rates-0) for the probability of surviving to future payments
- Bank of England's [Yield Curves](https://www.bankofengland.co.uk/statistics/yield-curves), specifically the nominal and real spot yield curves, to discount future payments.
''')


st.header('Parameters')

escalations = {
    'Level': 'Nominal',
    'Inflation-linked': 'Real',
}

age = st.number_input('Current age', value=66, min_value=20, max_value=120, step=1, key='age')
pay = st.number_input('Annuity annual pay', value=state_pension_full, min_value=1.0, step=1.0, key='pay')
escalation = st.radio('Annuity escalation', escalations.keys(), index=1, key='escalation')


st.header('Results')

st.warning('Mortality tables and yield curves are not yet being updated daily and might be out of date', icon="🚧")

kind = escalations[escalation]

unit_present_value = annuities.present_value(age, kind)

present_value = pay * unit_present_value

annuity_rate = 100000.0 / unit_present_value

col1, col2 = st.columns(2)
with col1:
    st.metric('Annuity present value', f'£{present_value:,.0f}')
with col2:
    st.metric('Annuity rate', f'£{annuity_rate:,.0f} / £100k')


common.analytics_html()