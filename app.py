# app.py
# Cyber Risk Assessment Tool (UK Charities)
# Author: Aisha Moussa

import json
import streamlit as st
import pandas as pd

from ux import apply_styles, hero_card
from questionnaire import QUESTIONNAIRE, DOMAIN_QUESTION_IDS
from charity_profile import default_charity_context
from data_loader import context_templates
from scoring import run_assessment


# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="Cyber Risk Assessment Tool", layout="wide")
apply_styles()
hero_card()

# -------------------------
# Session state
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "last_calculated" not in st.session_state:
    st.session_state.last_calculated = None


# -------------------------
# Tabs (main navigation)
# -------------------------
tab1, tab2, tab3 = st.tabs(["Assessment", "Results", "About"])

templates = context_templates()


# -------------------------
# Helper: build context from session state
# (so Results always uses latest inputs)
# -------------------------
def build_ctx_from_state() -> dict:
    ctx_local = default_charity_context()

    chosen = st.session_state.get("template_choice", "Custom (enter your own)")
    if chosen != "Custom (enter your own)" and chosen in templates:
        ctx_local.update(templates[chosen])

    ctx_local["charity_name"] = st.session_state.get("charity_name", ctx_local["charity_name"])
    ctx_local["data_sensitivity"] = st.session_state.get("data_sens", ctx_local["data_sensitivity"])
    ctx_local["operational_dependency"] = st.session_state.get("ops_dep", ctx_local["operational_dependency"])
    ctx_local["financial_exposure"] = st.session_state.get("fin_exp", ctx_local["financial_exposure"])
    ctx_local["reputational_risk"] = st.session_state.get("rep_risk", ctx_local["reputational_risk"])

    return ctx_local


# -------------------------
# Build responses dict from session_state
# -------------------------
responses = {}
for domain, questions in QUESTIONNAIRE.items():
    for q in questions:
        if q["id"] not in st.session_state:
            st.session_state[q["id"]] = 2  # default "partially in place"
        responses[q["id"]] = st.session_state[q["id"]]


# -------------------------
# TAB 1: Assessment (context + questionnaire)
# -------------------------
with tab1:
    st.header("Assessment")
    st.caption("Tip: answer honestly. This is an indicative self-assessment, not a compliance audit.")

    st.subheader("Charity context (Impact inputs)")
    with st.container(border=True):
        template_choice = st.selectbox(
            "Choose a template (optional)",
            ["Custom (enter your own)"] + list(templates.keys()),
            key="template_choice"
        )

        # Start with defaults, then apply template if chosen
        ctx_preview = default_charity_context()
        if template_choice != "Custom (enter your own)":
            ctx_preview.update(templates[template_choice])

        st.text_input("Charity name", value=ctx_preview["charity_name"], key="charity_name")

        c1, c2 = st.columns(2)
        with c1:
            st.slider(
                "Data sensitivity (0-4)",
                0, 4, int(ctx_preview["data_sensitivity"]),
                help="How sensitive is the data? (e.g., beneficiaries, donor details, finance)",
                key="data_sens"
            )
            st.slider(
                "Financial exposure (0-4)",
                0, 4, int(ctx_preview["financial_exposure"]),
                help="How much financial loss could result from an incident?",
                key="fin_exp"
            )
        with c2:
            st.slider(
                "Operational dependency (0-4)",
                0, 4, int(ctx_preview["operational_dependency"]),
                help="How badly would disruption affect daily operations?",
                key="ops_dep"
            )
            st.slider(
                "Reputational risk (0-4)",
                0, 4, int(ctx_preview["reputational_risk"]),
                help="How damaging would loss of trust be (donors, community, regulators)?",
                key="rep_risk"
            )

    st.divider()

    st.subheader("Questionnaire (0 = not in place, 4 = fully in place)")

    for domain, questions in QUESTIONNAIRE.items():
        with st.expander(domain, expanded=True):
            for q in questions:
                st.slider(
                    f"{q['id']} - {q['question']}",
                    0, 4,
                    value=int(st.session_state[q["id"]]),
                    key=q["id"]
                )


# -------------------------
# TAB 2: Results (scoring + outputs)
# -------------------------
with tab2:
    st.header("Results")

    ctx = build_ctx_from_state()

    if st.button("Calculate risk score", key="calc_risk"):
        st.session_state.result = run_assessment(
            responses=responses,
            domain_question_ids=DOMAIN_QUESTION_IDS,
            context=ctx
        )
        st.session_state.last_calculated = pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    result = st.session_state.result

    if result is None:
        st.warning("Go to the Assessment tab, answer the questions, then click 'Calculate risk score'.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Risk band", result["risk_band"])
        col2.metric("Likelihood", result["likelihood"])
        col3.metric("Impact", result["impact"])
        col4.metric("Risk score", result["risk_score"])

        if st.session_state.last_calculated:
            st.caption(f"Last calculated: {st.session_state.last_calculated}")

        st.subheader("Cyber risk exposure by domain (higher = weaker)")
        st.caption("This chart visualises weakness = 4 - maturity. Higher weakness contributes to higher likelihood.")

        domain_df = pd.DataFrame.from_dict(
            result["domain_scores"],
            orient="index",
            columns=["Maturity (0-4)"]
        )
        domain_df.index.name = "Domain"

        weakness_df = domain_df.copy()
        weakness_df["Weakness (0-4)"] = 4 - weakness_df["Maturity (0-4)"]
        weakness_df = weakness_df[["Weakness (0-4)"]]

        st.bar_chart(weakness_df)

        combined_df = domain_df.join(weakness_df)
        st.dataframe(combined_df.style.format("{:.2f}"), use_container_width=True)

        st.subheader("Weakest areas (priority order)")
        weak_df = pd.DataFrame(result["weak_domain_ranking"], columns=["Domain", "Weakness (0–4)"])
        weak_df.index = range(1, len(weak_df) + 1)
        weak_df.index.name = "Priority"
        st.dataframe(weak_df.style.format({"Weakness (0–4)": "{:.2f}"}), use_container_width=True)

        top_domain = weak_df.iloc[0]["Domain"]
        st.info(
            f"Interpretation: your highest exposure is currently **{top_domain}**. "
            "Improving controls in the weakest domain(s) should reduce likelihood and overall risk score."
        )

        st.subheader("Recommendations")
        try:
            with st.container(border=True):
                for r in result["recommendations"]:
                    st.write(f"• {r}")
        except TypeError:
            for r in result["recommendations"]:
                st.info(r)

        st.subheader("Export evidence")
        export_payload = {
            "tool_name": "Cyber Risk Assessment Tool (UK Charities)",
            "last_calculated_utc": st.session_state.last_calculated,
            "charity_context": ctx,
            "responses": responses,
            "result": result
        }

        st.download_button(
            "Download results (JSON)",
            data=json.dumps(export_payload, indent=2),
            file_name="risk_assessment_result.json",
            mime="application/json",
            key="download_json"
        )


# -------------------------
# TAB 3: About
# -------------------------
with tab3:
    st.header("About this tool")
    st.write(
        """
This prototype helps UK charities estimate cyber risk using:

- **NIST CSF 2.0** domains (Identify, Protect, Detect, Respond, Recover) to structure the questionnaire  
- **NIST SP 800-30-inspired** logic: *Risk = Likelihood × Impact*

**How to interpret results**
- *Maturity (0-4)* reflects how much a control is in place.
- *Weakness = 4 - maturity* (higher weakness increases likelihood).
- *Impact* is based on charity context: sensitivity, operations, finance, reputation.

**Limitations (being honest)**
- Answers are self-reported (so results depend on honest inputs).
- The scoring model is intentionally lightweight to stay usable for small charities.
- Future work could add domain weights, red-flag rules (e.g., “no backups”), and deeper validation/testing.
"""
    )
