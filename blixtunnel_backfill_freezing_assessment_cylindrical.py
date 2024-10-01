import numpy as np

# Material properties and dimensions
k_concrete, k_grout = 1.7, 1.5
t_concrete, t_grout = 0.4, 0.2
r_inner = 10.0 / 2
r_concrete_outer = r_inner + t_concrete
r_grout_outer = r_concrete_outer + t_grout
L = 1.0

def thermal_resistance_cylinder(r1, r2, k, L):
    return np.log(r2 / r1) / (2 * np.pi * k * L)

R_concrete = thermal_resistance_cylinder(r_inner, r_concrete_outer, k_concrete, L)
R_grout = thermal_resistance_cylinder(r_concrete_outer, r_grout_outer, k_grout, L)
R_total = R_concrete + R_grout

def calculate_temperatures(T_internal, T_external):
    Q_dot = (T_internal - T_external) / R_total
    T_cg = T_internal - Q_dot * R_concrete
    r_mid_grout = r_concrete_outer + t_grout / 2
    R_grout_mid = thermal_resistance_cylinder(r_concrete_outer, r_mid_grout, k_grout, L)
    T_mid_grout = T_internal - Q_dot * (R_concrete + R_grout_mid)
    return {
        'Heat Transfer Rate (W/m)': Q_dot,
        'Temperature at Concrete-Grout Interface (°C)': T_cg,
        'Temperature at Middle of Grout (°C)': T_mid_grout,
        'Temperature at Grout-Rock Interface (°C)': T_external
    }

def assess_freezing(temperatures):
    for key, value in temperatures.items():
        if 'Temperature' in key:
            status = "Above freezing" if value > 0 else "Risk of freezing"
            print(f"{key}: {value:.2f} °C ({status})")
        else:
            print(f"{key}: {value:.2f} W/m")

if __name__ == "__main__":
    T_internal_with_traffic, T_internal_without_traffic, T_external = -8.0, -10.0, 8.0
    results_with_traffic = calculate_temperatures(T_internal_with_traffic, T_external)
    results_without_traffic = calculate_temperatures(T_internal_without_traffic, T_external)

    print("Analytical Assessment of Freezing Potential in the Blixtunnelen Tunnel")
    print("----------------------------------------------------------------------")
    print("With High-Speed Railway Traffic:")
    assess_freezing(results_with_traffic)
    print("\nWithout High-Speed Railway Traffic:")
    assess_freezing(results_without_traffic)