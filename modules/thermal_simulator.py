# ==========================================
# THERMOSIM AI
# THERMAL SIMULATOR MODULE
# ==========================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from models.peltier_model import simulate_thermal_response


def show_thermal_simulator():

    st.title("❄️ Thermal Simulator")

    st.write(
        "Simulate the cold-side and hot-side "
        "temperature variations of a Peltier system."
    )

    st.divider()

    # ======================================
    # 1. USER INPUT PARAMETERS
    # ======================================

    st.subheader("Simulation Parameters")

    col1, col2 = st.columns(2)

    with col1:

        current = st.number_input(
            "Operating Current (A)",
            min_value=0.1,
            max_value=6.0,
            value=3.0,
            step=0.1
        )

        ambient_temp = st.number_input(
            "Ambient Temperature (°C)",
            value=30.0
        )

        initial_cold_temp = st.number_input(
            "Initial Cold Temperature (°C)",
            value=30.0
        )

    with col2:

        initial_hot_temp = st.number_input(
            "Initial Hot Temperature (°C)",
            value=30.0
        )

        duration = st.slider(
            "Simulation Duration (seconds)",
            min_value=60,
            max_value=1800,
            value=600,
            step=60
        )

        internal_heat_load = st.number_input(
            "Internal Heat Load (W)",
            min_value=0.0,
            value=0.0,
            step=0.5
        )

    st.divider()

    # ======================================
    # 2. RUN SIMULATION
    # ======================================

    if st.button("🚀 RUN SIMULATION", use_container_width=True):

        with st.spinner("Running thermal simulation..."):

            results = simulate_thermal_response(

                current=current,

                ambient_temp=ambient_temp,

                initial_cold_temp=initial_cold_temp,

                initial_hot_temp=initial_hot_temp,

                duration=duration,

                internal_heat_load=internal_heat_load

            )

        st.success("Simulation completed successfully!")

        # ==================================
        # 3. DISPLAY TEMPERATURE RESULTS
        # ==================================

        cold_final = results["cold_temperature"][-1]

        hot_final = results["hot_temperature"][-1]

        temperature_difference = hot_final - cold_final

        st.subheader("Final Temperature Results")

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Cold Side",
            f"{cold_final:.2f} °C"
        )

        metric2.metric(
            "Hot Side",
            f"{hot_final:.2f} °C"
        )

        metric3.metric(
            "Temperature Difference",
            f"{temperature_difference:.2f} °C"
        )

        st.divider()

        # ==================================
        # 4. TEMPERATURE GRAPH
        # ==================================

        st.subheader("Temperature vs Time")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=results["time"],
                y=results["cold_temperature"],
                name="Cold Side",
                mode="lines"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=results["time"],
                y=results["hot_temperature"],
                name="Hot Side",
                mode="lines"
            )
        )

        fig.update_layout(

            xaxis_title="Time (seconds)",

            yaxis_title="Temperature (°C)",

            title="Peltier Thermal Response",

            template="plotly_dark",

            hovermode="x unified"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==================================
        # 5. TEMPERATURE DIFFERENCE GRAPH
        # ==================================

        st.subheader("Temperature Difference vs Time")

        difference_fig = go.Figure()

        difference_fig.add_trace(
            go.Scatter(
                x=results["time"],
                y=results["temperature_difference"],
                name="Temperature Difference",
                mode="lines"
            )
        )

        difference_fig.update_layout(

            xaxis_title="Time (seconds)",

            yaxis_title="Temperature Difference (°C)",

            template="plotly_dark"

        )

        st.plotly_chart(
            difference_fig,
            use_container_width=True
        )

        # ==================================
        # 6. DOWNLOAD SIMULATION DATA
        # ==================================

        st.subheader("Simulation Dataset")

        df = pd.DataFrame({

            "Time (seconds)": results["time"],

            "Cold Temperature (°C)": results["cold_temperature"],

            "Hot Temperature (°C)": results["hot_temperature"],

            "Temperature Difference (°C)": results["temperature_difference"]

        })

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(

            label="📥 Download Simulation Results",

            data=csv,

            file_name="thermosim_results.csv",

            mime="text/csv"

        )