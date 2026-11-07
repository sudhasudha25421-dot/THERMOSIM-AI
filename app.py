# ==========================================
# THERMOSIM AI
# MAIN APPLICATION
# ==========================================

import streamlit as st

from modules.thermal_simulator import (
    show_thermal_simulator
)

from modules.performance_analyzer import (
    show_performance_analyzer
)

from modules.temperature_predictor import (
    show_temperature_predictor
)

from modules.energy_optimizer import (
    show_energy_optimizer
)

from modules.digital_twin import (
    show_digital_twin_dashboard
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="THERMOSIM AI",

    page_icon="❄️",

    layout="wide"

)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""

<style>

.stApp {

    background-color: #0b1220;

    color: white;

}

h1, h2, h3 {

    color: #38bdf8;

}

[data-testid="stSidebar"] {

    background-color: #111c30;

}

</style>

""", unsafe_allow_html=True)


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("❄️ THERMOSIM AI")

st.subheader(

    "AI-Powered Thermoelectric Cooling "
    "Simulation and Optimization Platform"

)

st.markdown("---")


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("THERMOSIM AI")

page = st.sidebar.radio(

    "Navigation",

    [

        "Home Dashboard",

        "Thermal Simulator",

        "Performance Analyzer",

        "AI Temperature Predictor",

        "Energy Optimizer",

        "Digital Twin Dashboard"

    ]

)


# ==========================================
# HOME DASHBOARD
# ==========================================

if page == "Home Dashboard":

    st.header("System Overview")

    st.write(

        "Welcome to THERMOSIM AI. "
        "Simulate, analyze, predict and optimize "
        "thermoelectric cooling systems."

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "System Status",
            "Ready"
        )

    with col2:

        st.metric(
            "Simulation Engine",
            "Available"
        )

    with col3:

        st.metric(
            "AI Model",
            "Trained"
        )

    st.divider()

    st.header("Available Modules")

    col1, col2 = st.columns(2)

    with col1:

        st.info("❄️ Thermal Simulator")

        st.write(
            "Simulate hot-side and cold-side temperatures."
        )

        st.info("📊 Performance Analyzer")

        st.write(
            "Calculate cooling capacity, electrical power and COP."
        )

        st.info("🤖 AI Temperature Predictor")

        st.write(
            "Predict future thermal behaviour using machine learning."
        )

    with col2:

        st.info("⚡ Energy Optimizer")

        st.write(
            "Identify energy-efficient operating conditions."
        )

        st.info("🌡️ Digital Twin Dashboard")

        st.write(
            "Visualize the virtual Peltier cooling system."
        )

    st.divider()

    st.subheader("Project Technology Stack")

    st.write(

        """
        - Python
        - Streamlit
        - NumPy
        - SciPy
        - Pandas
        - Plotly
        - Scikit-learn
        - Random Forest Regression
        """

    )


# ==========================================
# THERMAL SIMULATOR
# ==========================================

elif page == "Thermal Simulator":

    show_thermal_simulator()


# ==========================================
# PERFORMANCE ANALYZER
# ==========================================

elif page == "Performance Analyzer":

    show_performance_analyzer()


# ==========================================
# AI TEMPERATURE PREDICTOR
# ==========================================

elif page == "AI Temperature Predictor":

    show_temperature_predictor()


# ==========================================
# ENERGY OPTIMIZER
# ==========================================

elif page == "Energy Optimizer":

    show_energy_optimizer()


# ==========================================
# DIGITAL TWIN DASHBOARD
# ==========================================

elif page == "Digital Twin Dashboard":

    show_digital_twin_dashboard()