
import streamlit as st
import pandas as pd

from main import newton_raphson


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Newton-Raphson Calculator",
    page_icon="√",
    layout="wide"
)


# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #2874E8;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 16px;
}

.result-box {
    background: #EAF2FF;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
}

.result-value {
    font-size: 38px;
    font-weight: bold;
    color: #2463C7;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    '<div class="main-title">√ Newton-Raphson Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Finding Square Roots Using Numerical Methods'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------
# PROJECT INFORMATION
# -----------------------------------

with st.expander("About This Project"):

    st.write("""
    This project demonstrates the Newton-Raphson Method,
    an iterative numerical technique used to find roots
    of mathematical equations.
    
    It calculates square roots without using built-in
    square root functions.
    """)

    st.latex(
        r"x_{n+1} = \frac{1}{2}"
        r"\left(x_n + \frac{N}{x_n}\right)"
    )


# -----------------------------------
# USER INPUT
# -----------------------------------

st.subheader("Calculate Square Root")

col1, col2 = st.columns([3, 1])

with col1:

    number = st.number_input(
        "Enter a number",
        min_value=-1000000.0,
        value=25.0,
        step=1.0
    )

with col2:

    st.write("")
    st.write("")

    calculate = st.button(
        "Calculate √",
        type="primary",
        use_container_width=True
    )


# -----------------------------------
# SAMPLE NUMBERS
# -----------------------------------

st.caption("Example numbers: 25, 2, 100, 144, 0.25")


# -----------------------------------
# CALCULATION
# -----------------------------------

if calculate:

    if number < 0:

        st.error("Please enter a non-negative number.")

    else:

        result, history = newton_raphson(number)

        st.divider()

        st.subheader("Calculation Results")

        # Handle zero separately
        if number == 0:

            st.success("Square Root = 0")

            st.metric("Input Number", "0")
            st.metric("Iterations", "0")

        else:

            # Result cards
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Input Number", f"{number:g}")

            with col2:
                st.metric("Square Root", f"{result:.8f}")

            with col3:
                st.metric("Total Iterations", len(history))

            st.success("Calculation completed successfully!")

            # -----------------------------------
            # ITERATION TABLE
            # -----------------------------------

            st.subheader("Iteration History")

            df = pd.DataFrame(history)

            st.dataframe(
                df.style.format({
                    "Current Value": "{:.8f}",
                    "New Approximation": "{:.8f}",
                    "Error": "{:.8e}"
                }),
                use_container_width=True,
                hide_index=True
            )

            # -----------------------------------
            # CONVERGENCE GRAPH
            # -----------------------------------

            st.subheader("Convergence Graph")

            graph_data = pd.DataFrame({
                "Iteration": [0] + df["Iteration"].tolist(),
                "Approximation": [
                    history[0]["Current Value"]
                ] + df["New Approximation"].tolist()
            })

            st.line_chart(
                graph_data.set_index("Iteration"),
                y="Approximation"
            )

            # -----------------------------------
            # FINAL ANSWER
            # -----------------------------------

            st.markdown(
                f"""
                <div class="result-box">
                    <p>FINAL SQUARE ROOT</p>
                    <div class="result-value">
                        {result:.8f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # -----------------------------------
            # DOWNLOAD REPORT
            # -----------------------------------

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Iteration Report",
                data=csv,
                file_name="iteration_results.csv",
                mime="text/csv"
            )


# -----------------------------------
# HOW IT WORKS
# -----------------------------------

st.divider()

st.subheader("How Does It Work?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 01")
    st.write("**Initial Guess**")
    st.write("Select an initial approximation.")

with col2:
    st.markdown("### 02")
    st.write("**Iteration**")
    st.write("Apply the Newton-Raphson formula repeatedly.")

with col3:
    st.markdown("### 03")
    st.write("**Convergence**")
    st.write("Stop when the required accuracy is reached.")


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "Computational Methods Laboratory | "
    "Newton-Raphson Method"
)
