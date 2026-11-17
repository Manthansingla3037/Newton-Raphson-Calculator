import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Interest Rate Calculator | Newton-Raphson", page_icon="📈", layout="wide")

def newton_raphson_interest_rate(pv, fv, years, initial_rate_percent=10.0,
                                 tolerance=1e-10, max_iterations=100):
    """Find annual rate r from FV = PV(1+r)^n using Newton-Raphson."""
    if pv <= 0 or fv <= 0:
        raise ValueError("Present Value and Future Value must be greater than zero.")
    if years <= 0:
        raise ValueError("Investment period must be at least 1 year.")

    rate = initial_rate_percent / 100.0
    if rate <= -1:
        raise ValueError("Initial guess must be greater than -100%.")

    history = []

    def f(r):
        return pv * ((1.0 + r) ** years) - fv

    def df(r):
        return pv * years * ((1.0 + r) ** (years - 1))

    for iteration in range(1, max_iterations + 1):
        f_value, derivative = f(rate), df(rate)
        if not np.isfinite(f_value) or not np.isfinite(derivative):
            raise RuntimeError("Numerical overflow occurred. Try a different initial guess.")
        if abs(derivative) < 1e-15:
            raise RuntimeError("Derivative is too close to zero. Try a different initial guess.")

        raw_new_rate = rate - f_value / derivative
        new_rate = raw_new_rate

        # Keep each estimate in the mathematical domain r > -1.
        damping = 1.0
        while new_rate <= -0.999999999 and damping > 1e-8:
            damping *= 0.5
            new_rate = rate + damping * (raw_new_rate - rate)
        if new_rate <= -0.999999999 or not np.isfinite(new_rate):
            raise RuntimeError("Could not find a valid next estimate. Try another initial guess.")

        residual = abs(f(new_rate))
        change_percent = abs(new_rate - rate) * 100.0
        history.append({
            "Iteration": iteration,
            "Current Rate (%)": rate * 100.0,
            "Function Value": f_value,
            "Derivative": derivative,
            "New Rate (%)": new_rate * 100.0,
            "Change (%)": change_percent,
            "Absolute Error in FV": residual
        })
        rate = new_rate

        if change_percent < tolerance * 100.0 and residual < max(1e-8, fv * 1e-10):
            return rate, history

    raise RuntimeError("Method did not converge within 100 iterations. Try another initial guess.")

st.title("📈 Interest Rate Calculator")
st.caption("Find the unknown annual interest rate using the Newton–Raphson numerical method.")
st.divider()

with st.expander("Project concept and formula", expanded=False):
    st.write("Given the initial investment, future value, and number of years, this app estimates the annual compound interest rate.")
    st.latex(r"FV = PV(1+r)^n")
    st.write("Convert the equation into a root-finding problem:")
    st.latex(r"f(r)=PV(1+r)^n-FV=0")
    st.write("Newton–Raphson iteration:")
    st.latex(r"r_{k+1}=r_k-\frac{PV(1+r_k)^n-FV}{nPV(1+r_k)^{n-1}}")
    st.caption("PV = Present Value, FV = Future Value, n = years, r = annual rate as a decimal.")

st.subheader("Enter investment details")
left, right = st.columns(2)
with left:
    pv = st.number_input("Initial Investment / Present Value (₹)", min_value=0.01, value=10000.0, step=500.0, format="%.2f")
    years = st.number_input("Investment Period (years)", min_value=1, max_value=100, value=5, step=1)
with right:
    fv = st.number_input("Future Value (₹)", min_value=0.01, value=15000.0, step=500.0, format="%.2f")
    initial_guess = st.number_input("Initial Interest Rate Guess (%)", min_value=-99.0, max_value=500.0, value=10.0, step=1.0)

st.info("Assumption: interest is compounded once per year. The initial guess changes the iteration path, not the final mathematical answer.")

if st.button("Calculate Interest Rate", type="primary", use_container_width=True):
    try:
        rate, history = newton_raphson_interest_rate(pv, fv, int(years), initial_guess)
        calculated_fv = pv * (1 + rate) ** int(years)
        df = pd.DataFrame(history)

        st.divider()
        st.subheader("Calculation Result")
        a, b, c, d = st.columns(4)
        a.metric("Annual Interest Rate", f"{rate * 100:.6f}%")
        b.metric("Present Value", f"₹{pv:,.2f}")
        c.metric("Future Value", f"₹{fv:,.2f}")
        d.metric("Iterations", str(len(history)))
        st.success(f"Estimated annual interest rate: **{rate * 100:.6f}%**")

        x, y = st.columns(2)
        x.metric("Total Investment Gain", f"₹{fv - pv:,.2f}")
        y.metric("Reconstructed Future Value", f"₹{calculated_fv:,.2f}")

        st.subheader("Iteration History")
        st.dataframe(df.style.format({
            "Current Rate (%)": "{:.10f}",
            "Function Value": "{:.8e}",
            "Derivative": "{:.8e}",
            "New Rate (%)": "{:.10f}",
            "Change (%)": "{:.10f}",
            "Absolute Error in FV": "{:.8e}"
        }), use_container_width=True, hide_index=True)

        st.subheader("Convergence Graph")
        graph = pd.DataFrame({
            "Iteration": list(range(len(history) + 1)),
            "Estimated Interest Rate (%)": [initial_guess] + df["New Rate (%)"].tolist()
        }).set_index("Iteration")
        st.line_chart(graph, use_container_width=True)

        st.subheader("Verification")
        st.latex(r"FV = PV(1+r)^n")
        st.write(f"₹{pv:,.2f} × (1 + {rate:.10f})^{int(years)} = **₹{calculated_fv:,.2f}**")

        st.download_button(
            "⬇️ Download Iteration Report (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="interest_rate_iteration_report.csv",
            mime="text/csv"
        )
    except (ValueError, RuntimeError, OverflowError) as error:
        st.error(str(error))

with st.expander("Limitations and notes"):
    st.markdown("""
    - Assumes annual compounding.
    - Present Value and Future Value must be positive.
    - Investment duration must be a positive whole number of years.
    - The annual interest rate must be greater than -100%.
    - Newton–Raphson may fail with an unsuitable initial guess; try another guess if needed.
    - This is an educational calculator, not financial advice.
    """)

st.divider()
st.caption("Computational Methods Laboratory Project • Newton–Raphson Method")
