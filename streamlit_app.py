import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Explainable Loan Approval Prediction System")
st.write(
    "This dashboard predicts whether a loan application is likely "
    "to be accepted or rejected."
)

MODEL_PATH = Path("exp6_api/best_loan_approval_model.joblib")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.sidebar.header("Loan Application Details")

loan_amount = st.sidebar.number_input(
    "Loan Amount",
    min_value=1000,
    max_value=100000,
    value=15000,
    step=1000
)

risk_score = st.sidebar.number_input(
    "Risk Score",
    min_value=300,
    max_value=850,
    value=720
)

dti = st.sidebar.number_input(
    "Debt-to-Income Ratio",
    min_value=0.0,
    max_value=100.0,
    value=18.5
)

employment_years = st.sidebar.number_input(
    "Employment Years",
    min_value=0.0,
    max_value=50.0,
    value=5.0
)

application_year = st.sidebar.selectbox(
    "Application Year",
    list(range(2007, 2019)),
    index=11
)

application_month = st.sidebar.selectbox(
    "Application Month",
    list(range(1, 13)),
    index=5
)

application_quarter = ((application_month - 1) // 3) + 1

purpose = st.sidebar.selectbox(
    "Loan Purpose",
    [
        "debt_consolidation",
        "credit_card",
        "home_improvement",
        "major_purchase",
        "small_business",
        "car",
        "medical",
        "moving",
        "vacation",
        "house",
        "other"
    ]
)

state = st.sidebar.selectbox(
    "State",
    [
        "CA", "NY", "TX", "FL", "IL", "NJ", "PA",
        "OH", "GA", "NC", "VA", "MA", "AZ", "WA",
        "MD", "CO", "MN", "MO", "CT", "TN"
    ]
)

input_data = pd.DataFrame(
    [{
        "loan_amount": loan_amount,
        "risk_score": risk_score,
        "dti": dti,
        "employment_years": employment_years,
        "application_year": application_year,
        "application_month": application_month,
        "application_quarter": application_quarter,
        "purpose": purpose,
        "state": state
    }]
)

st.subheader("Application Input")
st.dataframe(input_data, use_container_width=True)

if st.button("Predict Loan Approval"):

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("Loan Application: ACCEPTED")
    else:
        st.error("Loan Application: REJECTED")

    st.metric(
        "Approval Probability",
        f"{probability * 100:.2f}%"
    )

st.divider()

# ---------------------------------------------------------
# MODEL PERFORMANCE
# ---------------------------------------------------------

st.header("📊 Model Performance")

metrics_path = Path("reports/exp4/final_model_comparison.csv")

if metrics_path.exists():
    metrics_df = pd.read_csv(metrics_path)

    st.write(
        "Performance comparison of the machine-learning models "
        "evaluated during Experiment 4."
    )

    st.dataframe(
        metrics_df,
        use_container_width=True
    )
else:
    st.warning("Model performance file not found.")


# ---------------------------------------------------------
# SHAP EXPLAINABILITY
# ---------------------------------------------------------

st.header("🔍 SHAP Explainability")

st.write(
    "SHAP explains how different features influence the "
    "loan approval prediction."
)

shap_bar = Path(
    "reports/exp5/figures/shap_global_bar.png"
)

shap_beeswarm = Path(
    "reports/exp5/figures/shap_global_beeswarm.png"
)

shap_local = Path(
    "reports/exp5/figures/shap_local_waterfall.png"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Global Feature Importance")

    if shap_bar.exists():
        st.image(
            str(shap_bar),
            use_container_width=True
        )

with col2:
    st.subheader("SHAP Beeswarm Plot")

    if shap_beeswarm.exists():
        st.image(
            str(shap_beeswarm),
            use_container_width=True
        )

st.subheader("Local Prediction Explanation")

if shap_local.exists():
    st.image(
        str(shap_local),
        use_container_width=True
    )


st.divider()

# ---------------------------------------------------------
# DRIFT CHECK
# ---------------------------------------------------------

st.header("📈 Data Drift Check")

st.write(
    "The current application is compared with historical "
    "training-data statistics from Experiment 3."
)

summary_path = Path("reports/exp3/numeric_summary.csv")

if summary_path.exists():

    reference = pd.read_csv(
        summary_path,
        index_col=0
    )

    drift_features = {
        "loan_amount": loan_amount,
        "risk_score": risk_score,
        "dti": dti,
        "employment_years": employment_years
    }

    drift_results = []

    for feature, current_value in drift_features.items():

        ref_mean = reference.loc[feature, "mean"]
        ref_std = reference.loc[feature, "std"]

        z_score = abs(
            (current_value - ref_mean) / ref_std
        )

        if z_score < 1:
            status = "Normal"
        elif z_score < 2:
            status = "Moderate Shift"
        else:
            status = "Potential Drift"

        drift_results.append(
            {
                "Feature": feature,
                "Current Value": round(current_value, 2),
                "Reference Mean": round(ref_mean, 2),
                "Reference Std": round(ref_std, 2),
                "Drift Score": round(z_score, 2),
                "Status": status
            }
        )

    drift_df = pd.DataFrame(drift_results)

    st.dataframe(
        drift_df,
        use_container_width=True
    )

    max_drift = drift_df["Drift Score"].max()

    if max_drift < 1:
        st.success(
            "No significant input drift detected."
        )

    elif max_drift < 2:
        st.warning(
            "Moderate input shift detected."
        )

    else:
        st.error(
            "Potential data drift detected. "
            "The input contains values substantially different "
            "from historical training-data statistics."
        )

else:
    st.warning(
        "Historical reference statistics were not found."
    )

st.caption(
    "Academic project dashboard for loan application approval prediction."
)