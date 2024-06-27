import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
from streamlit_option_menu import option_menu
from pages.fund_level import agg_fund_summary


def main(): 
    v_menu = ['Agg Fund Summary']

    with st.sidebar:
        st.header('Fund Level Reporting')

        selected = option_menu(
            menu_title = None,
            options = v_menu,
            icons = None,
            menu_icon = 'menu-down',
            default_index = 0,
            # use_container_width=True
        )

    if selected == 'Agg Fund Summary':
        agg_fund_summary.main()

if __name__ == '__main__':
    main()