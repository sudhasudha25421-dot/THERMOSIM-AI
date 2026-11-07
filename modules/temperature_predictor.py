# ==========================================
# THERMOSIM AI
# AI TEMPERATURE PREDICTOR
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os


def show_temperature_predictor():

    st.title("🤖 AI Temperature Predictor")

    st.write(
        "Predict future cold-side and hot-side "
        "temperatures using a trained Random Forest model."
    )

    st.divider()

    # ======================================
    # 1. LOAD TRAINED MODEL
    # ======================================

    model_path = os.path.join(
        "models",
        "temperature_model.joblib"
    )

    if not os.path.exists(model_path):

        st.error("Trained AI model not found.")

        st.info(
            "Run train_temperature_model.py first."
        )

        return

    package = joblib.load(model_path)

    model = package["model"]

    features = package["features"]

    validation = package["validation"]

    # ======================================
    # 2. DISPLAY MODEL PERFORMANCE
    # ======================================

    st.subheader("AI Model Performance")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Cold Side R²",
            f"{validation['cold_r2']:.4f}"
        )

        st.metric(
            "Cold Side MAE",
            f"{validation['cold_mae']:.3f} °C"
        )

    with col2:

        st.metric(
            "Hot Side R²",
            f"{validation['hot_r2']:.4f}"
        )

        st.metric(
            "Hot Side MAE",
            f"{validation['hot_mae']:.3f} °C"
        )

    st.divider()

    # ======================================
    # 3. USER INPUT PARAMETERS
    # ======================================

    st.subheader("Prediction Parameters")

    col1, col2 = st.columns(2)

    with col1:

        current = st.number_input(
            "Operating Current (A)",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.5
        )

        ambient_temp = st.number_input(
            "Ambient Temperature (°C)",
            min_value=20.0,
            max_value=35.0,
            value=30.0,
            step=1.0
        )

        heat_load = st.number_input(
            "Internal Heat Load (W)",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            step=0.5
        )

    with col2:

        initial_cold_temp = 30.0

        initial_hot_temp = 30.0

        st.number_input(
            "Initial Cold Temperature (°C)",
            value=30.0,
            disabled=True
        )

        st.number_input(
            "Initial Hot Temperature (°C)",
            value=30.0,
            disabled=True
        )

        duration = st.slider(
            "Prediction Duration (seconds)",
            min_value=60,
            max_value=600,
            value=600,
            step=60
        )

    st.caption(
        "Initial temperatures are fixed at 30°C because "
        "the current training dataset uses these starting values."
    )

    st.divider()

    # ======================================
    # 4. RUN AI PREDICTION
    # ======================================

    if st.button(
        "🚀 PREDICT TEMPERATURE",
        use_container_width=True
    ):

        with st.spinner("AI is predicting temperatures..."):

            time_values = np.arange(
                0,
                duration + 1,
                2
            )

            input_data = pd.DataFrame({

                "current": current,

                "ambient_temp": ambient_temp,

                "initial_cold_temp": initial_cold_temp,

                "initial_hot_temp": initial_hot_temp,

                "internal_heat_load": heat_load,

                "time": time_values

            })

            input_data = input_data[features]

            predictions = model.predict(input_data)

            cold_predictions = predictions[:, 0]

            hot_predictions = predictions[:, 1]

        st.success("AI Temperature Prediction Completed!")

        # ==================================
        # 5. FINAL PREDICTED TEMPERATURES
        # ==================================

        st.subheader("Predicted Temperature Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Predicted Cold Temperature",
            f"{cold_predictions[-1]:.2f} °C"
        )

        col2.metric(
            "Predicted Hot Temperature",
            f"{hot_predictions[-1]:.2f} °C"
        )

        col3.metric(
            "Temperature Difference",
            f"{hot_predictions[-1] - cold_predictions[-1]:.2f} °C"
        )

        st.divider()

        # ==================================
        # 6. PREDICTION GRAPH
        # ==================================

        st.subheader("AI Temperature Prediction Graph")

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=time_values,

                y=cold_predictions,

                name="Predicted Cold Side",

                mode="lines"

            )

        )

        fig.add_trace(

            go.Scatter(

                x=time_values,

                y=hot_predictions,

                name="Predicted Hot Side",

                mode="lines"

            )

        )

        fig.update_layout(

            title="AI Predicted Thermal Response",

            xaxis_title="Time (seconds)",

            yaxis_title="Temperature (°C)",

            template="plotly_dark",

            hovermode="x unified"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ==================================
        # 7. TEMPERATURE DIFFERENCE
        # ==================================

        st.subheader("Predicted Temperature Difference")

        difference = (
            hot_predictions - cold_predictions
        )

        difference_fig = go.Figure()

        difference_fig.add_trace(

            go.Scatter(

                x=time_values,

                y=difference,

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
        # 8. PREDICTION DATASET
        # ==================================

        st.subheader("AI Prediction Dataset")

        df = pd.DataFrame({

            "Time (seconds)": time_values,

            "Predicted Cold Temperature (°C)": cold_predictions,

            "Predicted Hot Temperature (°C)": hot_predictions,

            "Temperature Difference (°C)": difference

        })

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            "📥 Download AI Prediction Results",

            data=csv,

            file_name="thermosim_ai_predictions.csv",

            mime="text/csv"

        )