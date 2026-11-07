import matplotlib.pyplot as plt

from models.peltier_model import simulate_thermal_response


# Run thermal simulation

results = simulate_thermal_response(

    current=3,

    ambient_temp=30,

    initial_cold_temp=30,

    initial_hot_temp=30,

    duration=600

)


# Display final temperatures

print("\nTHERMOSIM AI - THERMAL SIMULATION")

print(
    "Final Cold Temperature:",
    round(results["cold_temperature"][-1], 2),
    "°C"
)

print(
    "Final Hot Temperature:",
    round(results["hot_temperature"][-1], 2),
    "°C"
)


# Plot temperature variations

plt.figure(figsize=(10, 5))

plt.plot(
    results["time"],
    results["cold_temperature"],
    label="Cold Side"
)

plt.plot(
    results["time"],
    results["hot_temperature"],
    label="Hot Side"
)

plt.xlabel("Time (seconds)")

plt.ylabel("Temperature (°C)")

plt.title("THERMOSIM AI - Thermal Response")

plt.legend()

plt.grid(True)

plt.show()


# Plot temperature difference

plt.figure(figsize=(10, 5))

plt.plot(
    results["time"],
    results["temperature_difference"]
)

plt.xlabel("Time (seconds)")

plt.ylabel("Temperature Difference (°C)")

plt.title("Temperature Difference vs Time")

plt.grid(True)

plt.show()