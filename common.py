#
# Copyright (c) 2024 LateGenXer
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#


import os

import streamlit as st
import streamlit.components.v1 as components



# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
def set_page_config(page_title, page_icon=":material/savings:", layout="centered", initial_sidebar_state="auto"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items={
            "Get help": "https://github.com/LateGenXer/finance/discussions",
            "Report a Bug": "https://github.com/LateGenXer/finance/issues",
            "About": """LateGenXer's financial tools.

https://lategenxer.streamlit.app/

https://github.com/LateGenXer/finance

Copyright (c) 2024 LateGenXer.
""",
        }
    )


def analytics_html():
    # An invisible test marker, used when testing with Selenium to ensure a page ran till the end
    st.html('<span id="test-marker" style="display:none"></span>')

    # Use https://statcounter.com/ to understand which of the calculators are being
    # used, and therefore worthy of further attention.
    html = (
'''
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9J3F87PEF5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-9J3F87PEF5');
</script>
'''
    )

    components.html(html)
