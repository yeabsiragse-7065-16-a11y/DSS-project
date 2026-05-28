import streamlit as st
from streamlit_option_menu import option_menu

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Fuel Management DSS",
    page_icon="⛽",
    layout="wide"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* HIDE STREAMLIT DEFAULT ITEMS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* TITLE STYLE */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #1f4e79;
    margin-top: -20px;
    margin-bottom: 10px;
}

/* NAVIGATION BAR */
.nav-link {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# SYSTEM TITLE
# ---------------------------------

st.markdown(
    """
    <div class="main-title">
        Fuel Management Decision Support System
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# TOP NAVIGATION
# ---------------------------------

selected = option_menu(
    menu_title=None,
    options=[
        "Dashboard",
        "Prediction",
        "Analytics",
        "Alerts"
            ],
    icons=[
        "speedometer2",
        "cpu",
        "bar-chart",
        "exclamation-triangle"
       
    ],
    orientation="horizontal",
    default_index=0,
)

# ---------------------------------
# PAGE ROUTING
# ---------------------------------

if selected == "Dashboard":
    exec(open("Dashboard.py").read())

elif selected == "Prediction":
    exec(open("Prediction.py").read())

elif selected == "Analytics":
    exec(open("Analytics.py").read())

elif selected == "Alerts":
    exec(open("Alerts.py").read())


# ---------------------------------
# FOOTER
# ---------------------------------

st.markdown("""
<hr style="margin-top:40px;">

<div style='text-align: center; color: gray; font-size: 14px;'>

AACBSE Fuel Management DSS Prototype |
MSc Information Systems Thesis Project

</div>
""", unsafe_allow_html=True)   
