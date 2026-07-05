import numpy as np
import pandas as pd
from scipy.optimize import least_squares


# This function calculates error between actual and predicted values
def calculate_error(params, x_vals, y_vals):
    theta, M, X = params

    # Shift points
    x_shift = x_vals - X
    y_shift = y_vals - 42

    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # Rotate points back
    t_vals = x_shift * cos_t + y_shift * sin_t
    B_vals = -x_shift * sin_t + y_shift * cos_t

    # Expected curve part
    predicted_B = np.exp(M * np.abs(t_vals)) * np.sin(0.3 * t_vals)

    return B_vals - predicted_B


def find_parameters(file_name):
    data = pd.read_csv(file_name)

    x = data["x"].values
    y = data["y"].values

    # Define limits
    theta_range = (np.radians(0.01), np.radians(49.99))
    M_range = (-0.0499, 0.0499)
    X_range = (0.01, 99.99)

    best_error = float("inf")
    best_params = None

    # Try different starting values (simple grid search)
    for theta_guess in np.linspace(theta_range[0], theta_range[1], 10):
        for M_guess in np.linspace(M_range[0], M_range[1], 4):
            for X_guess in np.linspace(X_range[0], X_range[1], 4):

                result = least_squares(
                    calculate_error,
                    [theta_guess, M_guess, X_guess],
                    args=(x, y),
                    bounds=(
                        [theta_range[0], M_range[0], X_range[0]],
                        [theta_range[1], M_range[1], X_range[1]]
                    )
                )

                current_error = np.sum(result.fun ** 2)

                if current_error < best_error:
                    best_error = current_error
                    best_params = result.x

    # Final refinement
    final_result = least_squares(
        calculate_error,
        best_params,
        args=(x, y),
        bounds=(
            [theta_range[0], M_range[0], X_range[0]],
            [theta_range[1], M_range[1], X_range[1]]
        )
    )

    theta, M, X = final_result.x
    max_error = np.max(np.abs(final_result.fun))

    return theta, M, X, max_error


if __name__ == "__main__":
    theta, M, X, error = find_parameters("xy_data.csv")

    print("Final Values:")
    print("Theta (radians):", round(theta, 6))
    print("Theta (degrees):", round(np.degrees(theta), 4))
    print("M:", round(M, 6))
    print("X:", round(X, 6))
    print("Max Error:", error)

    # Simple LaTeX output
    latex = (
        f"(t*cos({theta:.4f}) - e^({M:.4f}|t|)*sin(0.3t)*sin({theta:.4f}) + {X:.4f}, "
        f"42 + t*sin({theta:.4f}) + e^({M:.4f}|t|)*sin(0.3t)*cos({theta:.4f}))"
    )

    print("\nEquation:")
    print(latex)