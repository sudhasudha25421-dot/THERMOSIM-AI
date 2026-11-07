# ==========================================
# THERMOSIM AI
# ENERGY OPTIMIZER
# ==========================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from models.peltier_model import calculate_tec_performance


def show_energy_optimizer():

    st.title("⚡ Energy Optimizer")

    st.write(
        "Find energy-efficient operating conditions "
        "for thermoelectric cooling systems."
    )

    st.divider()

    st.subheader("Optimization Parameters")

    col1, col2 = st.columns(2)

    with col1:

        required_cooling = st.number_input(
            "Required Cooling Capacity (W)",
            min_value=1.0,
            value=15.0,
            step=1.0
        )

        cold_temp = st.number_input(
            "Cold Side Temperature (°C)",
            value=20.0
        )

        hot_temp = st.number_input(
            "Hot Side Temperature (°C)",
            value=35.0
        )

        alpha = st.number_input(
            "Seebeck Coefficient (V/K)",
            value=0.05,
            format="%.4f"
        )

    with col2:

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

        duration = st.number_input(
            "Operating Duration (Hours)",
            min_value=0.1,
            value=2.0
        )

        max_current = st.slider(
            "Maximum Operating Current (A)",
            min_value=1.0,
            max_value=6.0,
            value=5.0,
            step=0.5
        )

    st.divider()

    if st.button(
        "⚡ OPTIMIZE ENERGY",
        use_container_width=True
    ):

        currents = np.linspace(
            0.1,
            max_current,
            500
        )

        records = []

        for current in currents:

            result = calculate_tec_performance(

                current=current,

                cold_temp=cold_temp,

                hot_temp=hot_temp,

                alpha=alpha,

                resistance=resistance,

                conductance=conductance

            )

            cooling = result["Cooling Capacity"]

            power = result["Power"]

            if cooling >= required_cooling and power > 0:

                energy = power * duration

                records.append({

                    "Current": current,

                    "Cooling Capacity": cooling,

                    "Power": power,

                    "COP": result["COP"],

                    "Voltage": result["Voltage"],

                    "Energy (Wh)": energy

                })

        if not records:

            st.error(
                "No feasible operating condition found. "
                "Try reducing the cooling requirement or "
                "increasing the maximum current."
            )

            return

        df = pd.DataFrame(records)

        # Minimum power operating condition

        optimal = df.loc[
            df["Power"].idxmin()
        ]

        st.success("Energy Optimization Completed!")

        st.subheader("Optimal Operating Conditions")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Optimal Current",
            f"{optimal['Current']:.2f} A"
        )

        c2.metric(
            "Minimum Power",
            f"{optimal['Power']:.2f} W"
        )

        c3.metric(
            "Optimal COP",
            f"{optimal['COP']:.3f}"
        )

        c4, c5 = st.columns(2)

        c4.metric(
            "Cooling Capacity",
            f"{optimal['Cooling Capacity']:.2f} W"
        )

        c5.metric(
            "Energy Consumption",
            f"{optimal['Energy (Wh)']:.2f} Wh"
        )

        st.divider()

        # Power vs Current

        st.subheader("Power vs Operating Current")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["Current"],
                y=df["Power"],
                mode="lines",
                name="Electrical Power"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[optimal["Current"]],
                y=[optimal["Power"]],
                mode="markers",
                name="Optimal Point",
                marker=dict(size=12)
            )
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Current (A)",
            yaxis_title="Power (W)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # COP vs Current

        st.subheader("COP vs Operating Current")

        cop_fig = go.Figure()

        cop_fig.add_trace(
            go.Scatter(
                x=df["Current"],
                y=df["COP"],
                mode="lines",
                name="COP"
            )
        )

        cop_fig.update_layout(
            template="plotly_dark",
            xaxis_title="Current (A)",
            yaxis_title="Coefficient of Performance"
        )

        st.plotly_chart(
            cop_fig,
            use_container_width=True
        )

        # Optimization dataset

        st.subheader("Optimization Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Optimization Results",
            data=csv,
            file_name="thermosim_optimization.csv",
            mime="text/csv"
        )