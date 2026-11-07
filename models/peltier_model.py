# ==========================================
# THERMOSIM AI
# Thermoelectric Mathematical Model
# ==========================================

import numpy as np
from scipy.integrate import solve_ivp


# Celsius to Kelvin conversion

def celsius_to_kelvin(temp_c):
    return temp_c + 273.15


# ==========================================
# 1. PELTIER PERFORMANCE CALCULATIONS
# ==========================================

def calculate_tec_performance(
    current,
    cold_temp,
    hot_temp,
    alpha,
    resistance,
    conductance
):

    Tc = celsius_to_kelvin(cold_temp)
    Th = celsius_to_kelvin(hot_temp)

    delta_T = Th - Tc

    Qc = (
        alpha * current * Tc
        - 0.5 * current**2 * resistance
        - conductance * delta_T
    )

    Qh = (
        alpha * current * Th
        + 0.5 * current**2 * resistance
        - conductance * delta_T
    )

    voltage = alpha * delta_T + current * resistance

    power = voltage * current

    COP = Qc / power if power > 0 else 0

    return {
        "Cooling Capacity": Qc,
        "Heat Rejection": Qh,
        "Voltage": voltage,
        "Power": power,
        "COP": COP
    }


# ==========================================
# 2. THERMAL DYNAMIC SIMULATION
# ==========================================

def simulate_thermal_response(

    current=3.0,
    ambient_temp=30.0,
    initial_cold_temp=30.0,
    initial_hot_temp=30.0,
    duration=600,

    alpha=0.05,
    resistance=2.0,
    conductance=0.8,

    cold_capacity=300.0,
    hot_capacity=500.0,

    cold_thermal_resistance=5.0,
    hot_thermal_resistance=0.5,

    internal_heat_load=0.0

):

    initial_conditions = [
        initial_cold_temp,
        initial_hot_temp
    ]

    # Thermal differential equations

    def thermal_equations(time, temperatures):

        Tc, Th = temperatures

        Tc_K = celsius_to_kelvin(Tc)
        Th_K = celsius_to_kelvin(Th)

        delta_T = Th_K - Tc_K

        # Cooling capacity

        Qc = (
            alpha * current * Tc_K
            - 0.5 * current**2 * resistance
            - conductance * delta_T
        )

        # Heat rejected

        Qh = (
            alpha * current * Th_K
            + 0.5 * current**2 * resistance
            - conductance * delta_T
        )

        # Heat entering cold side

        Qload = (
            (ambient_temp - Tc)
            / cold_thermal_resistance
            + internal_heat_load
        )

        # Heat removed by heatsink

        Qrejected = (
            (Th - ambient_temp)
            / hot_thermal_resistance
        )

        # Temperature changes per second

        dTc_dt = (
            Qload - Qc
        ) / cold_capacity

        dTh_dt = (
            Qh - Qrejected
        ) / hot_capacity

        return [dTc_dt, dTh_dt]

    # Numerical solution

    time_points = np.linspace(0, duration, 301)

    solution = solve_ivp(

        thermal_equations,

        [0, duration],

        initial_conditions,

        t_eval=time_points,

        method="RK45",

        max_step=2.0

    )

    if not solution.success:
        raise RuntimeError(solution.message)

    # Return simulation results

    return {

        "time": solution.t,

        "cold_temperature": solution.y[0],

        "hot_temperature": solution.y[1],

        "temperature_difference":
            solution.y[1] - solution.y[0]

    }