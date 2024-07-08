import streamlit as st
from streamlit_option_menu import option_menu
from pages.portco_reporting import portco_1, portco_2, portco_3
import streamlit_authenticator as stauth

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


def creds_edtered():
    if st.session_state['user'].strip() == 'JMAN-Client' and st.session_state['pass'].strip() == 'JMAN-PoC':
    # if st.session_state['user'].strip() == 'admin' and st.session_state['pass'].strip() == 'admin':

        st.session_state['authenticated'] = True
     
    else:
        st.session_state['authenticated'] = False
        if not st.session_state['pass']:
            st.warning('Please enter Password')
        elif not st.session_state['user']:
            st.warning('Please enter Username') 
        else:
            st.warning('Please enter Username & Password')

def authenticate_user():

    if 'authenticated' not in st.session_state:
        st.markdown("<h3 style='color: #19105B;'>Login</h3>", unsafe_allow_html=True)
        st.text_input(label='Username: ',value='', key='user', on_change=creds_edtered)
        st.text_input(label='Password: ',value='', key='pass', type="password", on_change=creds_edtered)

        return False

    else:
        if st.session_state['authenticated']:
            return True
        else:
            st.markdown("<h3 style='color: #19105B;'>Login</h3>", unsafe_allow_html=True)
            st.text_input(label='Username: ',value='', key='user', on_change=creds_edtered)
            st.text_input(label='Password: ',value='', key='pass', type="password", on_change=creds_edtered)
            return False

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

        [data-testid="collapsedControl"] > [data-testid="stLogo"]{
            width: 40px;
            height: 40px;
            border-radius:5px;
        }
        [data-testid="stSidebarHeader"] > [data-testid="stLogo"]{
            width: 100px;
            height: 50px;
        }

        [data-testid="baseButton-secondary"]{
            background-color: white;
            color: #19105b;
            font-weight:700;
            width:100px;
            height:20px;

        }
        [data-testid="stTextInput"]{
            width: 500px;
        }
        [data-testid="element-container"]{
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }


        [data-testid="stMarkdownContainer"] > p {
            color: #19105b;
            font-weight: 700;
        }

        """,
        unsafe_allow_html=True,
    )

        # [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]{
        #     margin-top:300px !important;
        # }


    if authenticate_user():

        v_menu = ['PortCo 1', 'PortCo 2', 'PortCo 3']

        with st.sidebar:
            st.markdown("<h3 style='color: white;'>Portfolio Reporting</h3>", unsafe_allow_html=True)

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

        
            # if st.button('Download'):
            #     print('Hello, Streamlit!')
            
            # if st.button('Upload'):
            #     print('Hello, Streamlit!')


        if selected == 'PortCo 1':
            portco_1.main()

        if selected == 'PortCo 2':
            portco_2.main()

        if selected == 'PortCo 3':
            portco_3.main()

if __name__ == '__main__':
    main()