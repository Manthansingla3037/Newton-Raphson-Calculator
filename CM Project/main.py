
def newton_raphson(number, tolerance=0.000001):
    """
    Calculate square root using Newton-Raphson Method.

    Parameters:
        number: Number whose square root is required.
        tolerance: Required accuracy.

    Returns:
        result: Calculated square root.
        history: List of iteration details.
    """

    if number < 0:
        raise ValueError("Negative numbers are not supported.")

    if number == 0:
        return 0.0, []

    # Initial approximation
    x = number if number >= 1 else 1.0

    history = []
    iteration = 0

    # Newton-Raphson formula
    while iteration < 100:

        new_x = 0.5 * (x + number / x)

        iteration += 1

        error = abs(new_x - x)

        history.append({
            "Iteration": iteration,
            "Current Value": x,
            "New Approximation": new_x,
            "Error": error
        })

        # Check convergence
        if error < tolerance:
            return new_x, history

        x = new_x

    raise RuntimeError("Method did not converge within 100 iterations.")


# Test the function independently
if __name__ == "__main__":

    number = 25

    result, history = newton_raphson(number)

    print("Input Number:", number)
    print("Square Root:", result)
    print("Total Iterations:", len(history))
