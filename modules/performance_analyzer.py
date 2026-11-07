# ==========================================
# THERMOSIM AI
# PERFORMANCE ANALYZER
# ==========================================

import streamlit as st

from models.peltier_model import calculate_tec_performance


def show_performance_analyzer():

    st.title("📊 Performance Analyzer")

    st.write(
        "Analyze the electrical and thermal "
        "performance of a thermoelectric cooling system."
    )

    st.divider()

    # USER INPUTS

    st.subheader("Operating Parameters")

    col1, col2 = st.columns(2)

    with col1:

        current = st.number_input(
            "Operating Current (A)",
            min_value=0.1,
            value=3.0,
            step=0.1
        )

        cold_temp = st.number_input(
            "Cold Side Temperature (°C)",
            value=20.0
        )

        alpha = st.number_input(
            "Seebeck Coefficient (V/K)",
            value=0.05,
            format="%.4f"
        )

    with col2:

        hot_temp = st.number_input(
            "Hot Side Temperature (°C)",
            value=35.0
        )

        resistance = st.number_input(
            "Electrical Resistance (Ohms)",
            min_value=0.01,
            value=2.0
        )

        conductance = st.number_input(
            "Thermal Conductance (W/K)",
            min_value=0.01,
            value=0.8
        )

    st.divider()

    # CALCULATE PERFORMANCE

    if st.button(
        "CALCULATE PERFORMANCE",
        use_container_width=True
    ):

        results = calculate_tec_performance(

            current=current,

            cold_temp=cold_temp,

            hot_temp=hot_temp,

            alpha=alpha,

            resistance=resistance,

            conductance=conductance

        )

        st.success("Performance Analysis Completed!")

        st.subheader("Performance Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Cooling Capacity",
            f"{results['Cooling Capacity']:.2f} W"
        )

        col2.metric(
            "Heat Rejection",
            f"{results['Heat Rejection']:.2f} W"
        )

        col3.metric(
            "Electrical Power",
            f"{results['Power']:.2f} W"
        )

        col4, col5 = st.columns(2)

        col4.metric(
            "Operating Voltage",
            f"{results['Voltage']:.2f} V"
        )

        col5.metric(
            "Coefficient of Performance",
            f"{results['COP']:.3f}"
        )

        st.divider()

        st.subheader("Engineering Interpretation")

        if results["Cooling Capacity"] > 0:

            st.success(
                "The Peltier module is providing "
                "positive cooling capacity."
            )

        else:

            st.warning(
                "The selected operating conditions "
                "do not provide positive cooling capacity."
            )

        st.info(
            "COP represents the cooling capacity "
            "obtained per unit of electrical power consumed."
        )