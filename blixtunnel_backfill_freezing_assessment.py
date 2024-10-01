import numpy as np

# Material properties and dimensions
k_concrete, k_grout = 1.7, 1.5
L_concrete, L_grout = 0.4, 0.2

def thermal_resistance(k, L, A=1.0):
    return L / (k * A)

def calculate_temperatures(T_internal, T_external, A=1.0):
    R_concrete = thermal_resistance(k_concrete, L_concrete, A)
    R_grout = thermal_resistance(k_grout, L_grout, A)
    R_total = R_concrete + R_grout
    Q_dot = (T_internal - T_external) / R_total
    T_cg = T_internal - Q_dot * R_concrete
    T_mid_grout = T_internal - Q_dot * (R_concrete + R_grout / 2)
    return Q_dot, T_cg, T_mid_grout, T_external

def assess_freezing(T_cg, T_mid_grout, T_gr):
    def status(T):
        return "Above freezing" if T > 0 else "Risk of freezing"
    return {
        "Concrete-Grout Interface": status(T_cg),
        "Middle of Grout": status(T_mid_grout),
        "Grout-Rock Interface": status(T_gr)
    }

if __name__ == "__main__":
    T_internal_with_traffic, T_internal_without_traffic, T_external = -8.0, -10.0, 8.0
    A = 1.0

    results_with_traffic = calculate_temperatures(T_internal_with_traffic, T_external, A)
    results_without_traffic = calculate_temperatures(T_internal_without_traffic, T_external, A)

    print("Analytical Assessment of Freezing Potential in the Blixtunnelen Tunnel")
    print("----------------------------------------------------------------------")
    for label, results in [("With High-Speed Railway Traffic", results_with_traffic), 
                           ("Without High-Speed Railway Traffic", results_without_traffic)]:
        Q_dot, T_cg, T_mid_grout, T_gr = results
        print(f"\n{label}:")
        print(f"Heat Transfer Rate: {Q_dot:.2f} W")
        print(f"Temperature at Concrete-Grout Interface: {T_cg:.2f} °C")
        print(f"Temperature at Middle of Grout: {T_mid_grout:.2f} °C")
        print(f"Temperature at Grout-Rock Interface: {T_gr:.2f} °C")
        freezing_assessment = assess_freezing(T_cg, T_mid_grout, T_gr)
        for location, status in freezing_assessment.items():
            print(f"- {location}: {status}")