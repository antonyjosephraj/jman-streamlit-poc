import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
from streamlit_option_menu import option_menu
from pages.fund_level import agg_fund_summary


def main(): 

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 320px;
            background: linear-gradient(#19105b, #472067, #7c3375, #FF6196) !important;
            color: white;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 320px;
            margin-left: -400px;
        }
        body {
            font-family: "Arial";
        }
        
        [data-testid="stSidebarNavLink"] > span {
            color: white !important;
            font-size:20px;
        }

        """,
        unsafe_allow_html=True,
    )

    v_menu = ['Agg Fund Summary']

    with st.sidebar:
        st.markdown("<h3 style='color: white;'>Fund Level Reporting</h3>", unsafe_allow_html=True)

        selected = option_menu(
            menu_title = None,
            options = v_menu,
            icons = None,
            menu_icon = 'menu-down',
            default_index = 0,
            styles={
                    # "container": {"padding": "0!important", "background-color": "#fafafa"},
                    # "icon": {"color": "orange", "font-size": "25px"}, 
                    # "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#19105B"},
                }
        )

    if selected == 'Agg Fund Summary':
        agg_fund_summary.main()

if __name__ == '__main__':
    main()