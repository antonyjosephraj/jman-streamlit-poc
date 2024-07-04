import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
from streamlit_option_menu import option_menu
from pages.fund_level import agg_fund_summary

st.set_page_config(
    page_title="JMAN App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)


HORIZONTAL_RED = "images/jman-logo.png"
ICON_RED = "images/jman-logo2.jpg"

def main(): 
    st.logo(HORIZONTAL_RED, icon_image=ICON_RED)

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            # width: 320px;
            background: linear-gradient(#19105b, #472067, #7c3375, #FF6196) !important;
            color: white;
        }
        # [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        #     width: 320px;
        #     margin-left: -400px;
        # }
        body {
            font-family: "Arial";
        }
        
        [data-testid="stSidebarNavLink"] > span {
            color: white !important;
            font-size:22px;
        }

        [data-testid="stSidebarNavSeparator"]{
            background-color: white;
            height: 1px;
        }
        [data-testid="stLogo"]{
            width: 100px;
            height: 50px;
        }
        [data-testid="stMarkdownContainer"] > p {
            color: #19105b;
            font-weight: 700;
        }

        """,
        unsafe_allow_html=True,
    )

    LOGO_URL_LARGE = "images\jman-logo.png"
    # st.logo(LOGO_URL_LARGE, link="https://streamlit.io/gallery", icon_image=LOGO_URL_LARGE)
    
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