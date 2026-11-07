from models.peltier_model import calculate_tec_performance

results = calculate_tec_performance(

    current=3,

    cold_temp=20,

    hot_temp=35,

    alpha=0.05,

    resistance=2,

    conductance=0.8

)

print("\nTHERMOSIM AI - PELTIER PERFORMANCE")

for parameter, value in results.items():

    print(f"{parameter}: {value:.2f}")