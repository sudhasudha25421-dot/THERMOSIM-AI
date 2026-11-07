# ==========================================
# THERMOSIM AI
# DIGITAL TWIN DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from models.peltier_model import (
    simulate_thermal_response,
    calculate_tec_performance
)


def show_digital_twin_dashboard():

    st.title("🌡️ Digital Twin Dashboard")

    st.write(
        "Interactive virtual representation of "
        "a thermoelectric Peltier cooling system."
    )

    st.divider()

    # ======================================
    # 1. VIRTUAL SYSTEM PARAMETERS
    # ======================================

    st.subheader("Virtual Peltier System")

    col1, col2 = st.columns(2)

    with col1:

        current = st.slider(
            "Operating Current (A)",
            0.5,
            5.0,
            3.0,
            0.5
        )

        ambient = st.number_input(
            "Ambient Temperature (°C)",
            value=30.0
        )

        heat_load = st.number_input(
            "Internal Heat Load (W)",
            min_value=0.0,
            value=0.0
        )

    with col2:

        duration = st.slider(
            "Simulation Duration (seconds)",
            60,
            1800,
            600,
            60
        )

        initial_cold = st.number_input(
            "Initial Cold Temperature (°C)",
            value=30.0
        )

        initial_hot = st.number_input(
            "Initial Hot Temperature (°C)",
            value=30.0
        )

    st.divider()

    # ======================================
    # 2. RUN DIGITAL TWIN
    # ======================================

    if st.button(
        "🌐 RUN DIGITAL TWIN",
        use_container_width=True
    ):

        with st.spinner("Updating virtual Peltier system..."):

            results = simulate_thermal_response(

                current=current,

                ambient_temp=ambient,

                initial_cold_temp=initial_cold,

                initial_hot_temp=initial_hot,

                duration=duration,

                internal_heat_load=heat_load

            )

            time = np.asarray(results["time"])

            cold = np.asarray(
                results["cold_temperature"]
            )

            hot = np.asarray(
                results["hot_temperature"]
            )

            difference = hot - cold

            # ==================================
            # 3. CALCULATE PERFORMANCE AT EACH TIME
            # ==================================

            cooling_values = []

            power_values = []

            cop_values = []

            voltage_values = []

            for tc, th in zip(cold, hot):

                performance = calculate_tec_performance(

                    current=current,

                    cold_temp=tc,

                    hot_temp=th,

                    alpha=0.05,

                    resistance=2.0,

                    conductance=0.8

                )

                cooling_values.append(
                    performance["Cooling Capacity"]
                )

                power_values.append(
                    performance["Power"]
                )

                cop_values.append(
                    performance["COP"]
                )

                voltage_values.append(
                    performance["Voltage"]
                )

        st.success("Digital Twin Updated Successfully!")

        # ======================================
        # 4. SYSTEM STATUS
        # ======================================

        st.subheader("Virtual System Status")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Cold Side",
            f"{cold[-1]:.2f} °C"
        )

        col2.metric(
            "Hot Side",
            f"{hot[-1]:.2f} °C"
        )

        col3.metric(
            "Temperature Difference",
            f"{difference[-1]:.2f} °C"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Cooling Capacity",
            f"{cooling_values[-1]:.2f} W"
        )

        col5.metric(
            "Electrical Power",
            f"{power_values[-1]:.2f} W"
        )

        col6.metric(
            "COP",
            f"{cop_values[-1]:.3f}"
        )

        st.divider()

        # ======================================
        # 5. TEMPERATURE VISUALIZATION
        # ======================================

        st.subheader("Virtual Thermal Visualization")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=time,
                y=cold,
                mode="lines",
                name="Cold Side"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=time,
                y=hot,
                mode="lines",
                name="Hot Side"
            )
        )

        fig.update_layout(
            title="Virtual Peltier Temperature Behaviour",
            xaxis_title="Time (seconds)",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ======================================
        # 6. TEMPERATURE DIFFERENCE
        # ======================================

        st.subheader("Thermal Gradient")

        fig2 = go.Figure()

        fig2.add_trace(
            go.Scatter(
                x=time,
                y=difference,
                mode="lines",
                name="Temperature Difference"
            )
        )

        fig2.update_layout(
            template="plotly_dark",
            xaxis_title="Time (seconds)",
            yaxis_title="Temperature Difference (°C)"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ======================================
        # 7. PERFORMANCE VISUALIZATION
        # ======================================

        st.subheader("Virtual System Performance")

        fig3 = make_subplots(

            rows=3,

            cols=1,

            subplot_titles=(

                "Cooling Capacity",

                "Electrical Power",

                "Coefficient of Performance"

            ),

            vertical_spacing=0.12

        )

        fig3.add_trace(

            go.Scatter(
                x=time,
                y=cooling_values,
                name="Cooling Capacity"
            ),

            row=1,
            col=1

        )

        fig3.add_trace(

            go.Scatter(
                x=time,
                y=power_values,
                name="Power"
            ),

            row=2,
            col=1

        )

        fig3.add_trace(

            go.Scatter(
                x=time,
                y=cop_values,
                name="COP"
            ),

            row=3,
            col=1

        )

        fig3.update_layout(

            height=750,

            template="plotly_dark",

            showlegend=False

        )

        fig3.update_xaxes(
            title_text="Time (seconds)",
            row=3,
            col=1
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # ======================================
        # 8. DIGITAL TWIN DATASET
        # ======================================

        st.subheader("Digital Twin Dataset")

        df = pd.DataFrame({

            "Time (seconds)": time,

            "Cold Temperature (°C)": cold,

            "Hot Temperature (°C)": hot,

            "Temperature Difference (°C)": difference,

            "Cooling Capacity (W)": cooling_values,

            "Electrical Power (W)": power_values,

            "Voltage (V)": voltage_values,

            "COP": cop_values

        })

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            "📥 Download Digital Twin Data",

            data=csv,

            file_name="thermosim_digital_twin.csv",

            mime="text/csv"

        )