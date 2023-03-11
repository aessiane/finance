import streamlit as st
import pandas as pd
import numpy as np

import datetime

st.set_page_config(layout="wide")
#st.set_page_config(layout="centered")

st.title('Retirement Tax Planner')

with st.expander("About..."):
    st.markdown(open('README.md', 'rt').read())

if True:
#with st.sidebar:
    st.header('Parameters')

    st.warning('Inputs are not stored permanently and will not persist across page reloads!', icon="⚠️")

    # Default state?
    #st.write(st.session_state)

    with st.form(key='my_form'):

        tab1, tab2 = st.tabs(["Basic", "Advanced"])

        with tab1:

            col1, col2, col3 = st.columns(3)

            state_pension_years_help = "If in doubt [check on your National Insurance record](https://www.gov.uk/check-state-pension) how many years of full contributions you have, and add how many more years you plan to work or do voluntary contributions."

            marginal_income_tax_help = "Used to estimate income tax from withdrawing more than the Tax Free Cash from a SIPP before retirement."

            with col1:
                st.subheader('You')
                st.number_input('Year of birth:', min_value=1980, max_value=2080, step=1, value=1980, key='dob_1')
                st.number_input('State pension qualifying years at retirement:', min_value=0, max_value=35, step=1, value=35, key='state_pension_years_1', help=state_pension_years_help)
                st.number_input('SIPP value:', min_value=0, step=1, value=750000, key='sipp_1')
                st.number_input('SIPP yearly _gross_ contribution:', min_value=0, max_value=40000, step=1, value=0, key='sipp_contrib_1', help="Until retirement")
                st.select_slider("Marginal income tax rate:", options=(0.00, 0.20, 0.40, 0.45), value=0.40, format_func='{:.0%}'.format, key="marginal_income_tax_1", help=marginal_income_tax_help)

            with col2:
                st.subheader('Partner')
                st.number_input('Year of birth:', min_value=1980, max_value=2080, step=1, value=1980, key='dob_2')
                st.number_input('State pension qualifying years at retirement:', min_value=0, max_value=35, step=1, value=35, key='state_pension_years_2', help=state_pension_years_help)
                st.number_input('SIPP value:', min_value=0, step=1, value=125000, key='sipp_2')
                st.number_input('SIPP yearly _gross_ contribution:', min_value=0, max_value=40000, step=1, value=0, key='sipp_contrib_2', help="Until retirement")
                st.select_slider("Marginal income tax rate:", options=(0.00, 0.20, 0.40, 0.45), value=0.20, format_func='{:.0%}'.format, key="marginal_income_tax_2", help=marginal_income_tax_help)

            with col3:
                st.subheader('Shared')
                st.number_input('Retirement year:', min_value=2020, max_value=2080, step=1, value=1980 + 65, key='retirement_year')
                st.number_input('Retirement income (0 for maximum):', min_value=0, step=1000, value=0, key='retirement_income_net', help='Go to https://www.retirementlivingstandards.org.uk/ for guidance.')
                st.number_input('ISAs value:', min_value=0, step=1, value=125000, key='isa')
                st.number_input('GIAs value:', min_value=0, step=1, value=0, key='gia')
                st.number_input('ISAs/GIAs yearly savings:', min_value=0, step=1, value=0, key='misc_contrib', help="Until retirement.  The optimization will automatically maximize the ISA allowance.")

        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                max_rate = 10.0
                growth_rate_format = '%.1f%%'
                st.slider("Inflation rate:", min_value=0.0, max_value=max_rate, step=0.5, value=2.5, format=growth_rate_format, key="inflation_rate")
                st.slider("Your SIPP nominal growth rate:", min_value=0.0, max_value=max_rate, step=0.5, value=5.5, format=growth_rate_format, key="sipp_growth_rate_1")
                st.slider("Partner's SIPP nominal growth rate:", min_value=0.0, max_value=max_rate, step=0.5, value=5.5, format=growth_rate_format, key="sipp_growth_rate_2")
                st.slider("ISAs nominal growth rate:", min_value=0.0, max_value=max_rate, step=0.5, value=5.5, format=growth_rate_format, key="isa_growth_rate")
                st.slider("GIAs nominal growth rate:", min_value=0.0, max_value=max_rate, step=0.5, value=5.5, format=growth_rate_format, key="gia_growth_rate")

            with col2:

                st.selectbox("Retirement country:", options=("UK", "PT"), index=0, key='retirement_country',
                    help="Country to be tax resident from _retirement year_. " +
                    "Values still always in pounds.  Differences in cost of life not considered."
                )

        submitted = st.form_submit_button(label='Update', type='primary')


#if submitted:
if True:
    st.header('Results')

    if False:
        df = pd.read_csv('retirement_lp.csv')
    else:
        import model

        params = dict(st.session_state)

        perc_xform = lambda x: x*.01
        state_xforms =  {
            'inflation_rate': perc_xform,
            'sipp_growth_rate_1': perc_xform,
            'sipp_growth_rate_2': perc_xform,
            'isa_growth_rate': perc_xform,
            'gia_growth_rate': perc_xform,
        }
        for key, xform in state_xforms.items():
            params[key] = xform(st.session_state[key])

        params['present_year'] = datetime.date.today().year
        params['pt'] = st.session_state.retirement_country == 'PT'

        #with st.expander("Parameters"):
        #    st.write(params)

        result = model.model(**params)

        df = model.dataframe(result.data)

    st.info("All values presented are in _today_'s pounds.", icon="ℹ️")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Start net worth", value=f"£{result.net_worth_start:,.0f}")
    with col2:
        st.metric(label="Retirement net income", value=f"£{result.retirement_income_net:,.0f}")
    with col3:
        st.metric(label="End net worth", value=f"£{result.net_worth_end:,.0f}")
    with col4:
        st.metric(label="Total tax", value=f"£{result.total_tax:,.0f}")

    column_headers = {
        'year': 'Year',

        'income_state': 'SP',

        'sipp_uf_1': 'UF1',
        'sipp_df_1': 'DF1',
        'sipp_delta_1': '(\u0394)',
        'lta_ratio_1': 'LTA1',
        'sipp_uf_2': 'UF2',
        'sipp_df_2': 'DF2',
        'sipp_delta_2': '(\u0394)',
        'lta_ratio_2': 'LTA2',

        'isa': 'ISAs',
        'isa_delta': '(\u0394)',
        'gia': 'GIA',
        'gia_delta': '(\u0394)',
        'income_gross_1': 'GI1',
        'income_gross_2': 'GI2',
        'income_net': 'NI',
        'income_surplus': 'Error',
        'income_tax_1': 'IT1',
        'income_tax_rate_1': '(%)',
        'income_tax_2': 'IT2',
        'income_tax_rate_2': '(%)',
        'cgt': 'CGT',
        'cgt_rate': '(%)',
        'lac': 'LAC',
    }

    float_format = '{:,.0f}'
    perc_format = '{:5.1%}'
    formatters = {
            'year': '{:}',
            'lta_ratio_1':  perc_format,
            'lta_ratio_2':  perc_format,
            'income_tax_rate_1': perc_format,
            'income_tax_rate_2': perc_format,
            'cgt_rate':     perc_format,
    }

    df = df[column_headers.keys()]

    s = df.style
    #s = pd.io.formats.style.Styler(df, uuid_len=0, cell_ids=False)
    s.hide(axis='index')
    s.format(float_format)
    #s.format(formatters, precision=0, thousands=' ') #, subset=[df.columns.get_loc(column) for column in formatters.keys()])
    s.format(formatters, subset=list(formatters.keys()))
    s.relabel_index(list(column_headers.values()), axis='columns')
    #s.set_properties(**{'font-size': '8pt'})
    s.set_table_styles([
        {'selector': 'td', 'props': 'text-align: right; padding:0px 2px 0px 2px;'}
    ])

    # https://stackoverflow.com/a/72303007
    #df_ = df[df['year'].gt(st.session_state.retirement_year)]
    #slice_ = pd.IndexSlice[df_.index, df_.columns]
    #s.set_properties(**{'background-color': '#f5f5f5'}, subset=slice_)
    s.highlight_between(subset=['year'], left=st.session_state.retirement_year, props='font-weight:bold')

    if True:
        # https://pandas.pydata.org/docs/user_guide/style.html#Background-Gradient-and-Text-Gradient
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html
        #s.background_gradient(cmap='Wistia', text_color_threshold=0, subset=['income_gross_1', 'income_gross_2'], vmin=12570, vmax=50270)
        s.background_gradient(cmap='Wistia', text_color_threshold=0, subset=['income_gross_1', 'income_gross_2'], vmin=0, vmax=100000)
        s.background_gradient(cmap='Oranges', subset=['income_tax_rate_1', 'income_tax_rate_2', 'cgt_rate'], vmin=0, vmax=1)
        #s.background_gradient(cmap='Oranges', subset=['income_tax_1', 'income_tax_2', 'cgt', 'lac'], vmin=0)
        s.background_gradient(cmap='magma', subset=['lta_ratio_1', 'lta_ratio_2'], vmin=0, vmax=1)

        # https://pandas.pydata.org/docs/user_guide/style.html#Bar-charts
        #s.bar(subset=['lta_ratio_1', 'lta_ratio_2'], align='left', color='#d65f5f', vmin=0, vmax=1)

    if True:
        import altair as alt

        cdf = pd.DataFrame()

        # https://stackoverflow.com/questions/46658232/pandas-convert-column-with-year-integer-to-datetime
        cdf['Year'] = pd.to_datetime(df['year'], format='%Y')

        cdf['SIPP1'] = df['sipp_uf_1'] + df['sipp_df_1']
        cdf['SIPP2'] = df['sipp_uf_2'] + df['sipp_df_2']
        cdf['ISA'] = df['isa']
        cdf['GIA'] = df['gia']

        # https://altair-viz.github.io/user_guide/data.html#converting-with-pandas
        cdf = cdf.melt('Year', var_name='Asset', value_name='Value')

        adf = pd.DataFrame()
        adf['Year'] = pd.to_datetime(df['year'], format='%Y')
        adf['LAC'] = df['lac']
        adf['Event'] = 'LAC'
        adf = adf[adf['LAC'] > 80]
        adf['Y'] = 0

        # https://altair-viz.github.io/user_guide/generated/core/altair.Legend.html
        # https://stackoverflow.com/questions/68624885/position-altair-legend-top-center
        legend = alt.Legend(
            orient='top-right',
            #legendX=130, legendY=-40,
            #direction='horizontal',
            #titleAnchor='middle'
        )

        yScale = alt.Scale(domainMin=0)
        yAxis = alt.Axis(format=',.0f', title=None)

        chart = (
            alt.Chart(cdf, title='Asset allocation')
            .mark_area()
            .encode(
                alt.X("Year:T", axis=alt.Axis(format="%Y", domain=False, tickSize=0)),
                alt.Y("Value:Q", stack="zero", scale=yScale, axis=yAxis),
                alt.Color("Asset:N", legend=legend),
            )
        )
        if False:
            # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart#annotating-charts
            annotation_layer = (
                alt.Chart(adf)
                .mark_text(size=20, text="⬇", dx=-8, dy=-10, align="left")
                .encode(
                    x="Year:T",
                    y=alt.Y("Y:Q"),
                    tooltip=["Event"],
                )
            )
            chart = chart + annotation_layer
        st.altair_chart(chart, use_container_width=True)

        cdf = pd.DataFrame()

        # https://stackoverflow.com/questions/46658232/pandas-convert-column-with-year-integer-to-datetime
        cdf['Year'] = pd.to_datetime(df['year'], format='%Y')

        cdf['Income Tax 1'] = df['income_tax_1']
        cdf['Income Tax 2'] = df['income_tax_2']
        cdf['Capital Gains Tax'] = df['cgt']
        cdf['Lifetime Allowance Charge'] = df['lac']

        cdf = cdf.melt('Year', var_name='Tax', value_name='Value')

        chart2 = (
            alt.Chart(cdf, title='Taxes')
            .mark_area()
            .encode(
                alt.X("Year:T", axis=alt.Axis(format="%Y", tickSize=0)),
                alt.Y("Value:Q", stack="zero", scale=yScale, axis=yAxis),
                alt.Color("Tax:N", legend=legend),
            )
        )
        #chart2 = alt.concat(chart, chart2)
        st.altair_chart(chart2, use_container_width=True)

    st.subheader("Plan")

    with st.expander("Abbreviations..."):
        st.markdown('''
* **1**: You
* **2**: Your partner
* **SP**: State Pension
* **UF**: Uncrystalized Funds
* **DF**: Drawdown Funds (for example, _flexi-access drawdown_)
* **GIA**: General Investment Account
* **GI**: Gross Income
* **NI**: Net Income
* **Error**: Error relative to target income; should be zero, unless there are modelling errors.
* **LTA**: Lifetime Allowance
* **\u0394**: Cash flow, that is, cash going in or out of the pot; excluding growth and tax charges.
* **IT**: Income Tax
* **CGT**: Capital Gains Tax
* **LAC**: Lifetime Allowance Charge
''')
    #st.dataframe(s)
    #st.table(s)

    # https://github.com/streamlit/streamlit/issues/4830#issuecomment-1147878371
    st.markdown(s.to_html(table_uuid="table_1"), unsafe_allow_html=True)