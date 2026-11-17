# Newton-Raphson Interest Rate Calculator

A Streamlit app that estimates the annual compound interest rate from Present Value,
Future Value, and investment duration using Newton-Raphson.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
Upload `app.py` and `requirements.txt` to the root of a GitHub repository.
Create an app and set **Main file path** to `app.py`.

Assumption: annual compounding. PV and FV must be positive, and the number of years
must be a positive whole number. Newton-Raphson convergence depends on the initial guess.
