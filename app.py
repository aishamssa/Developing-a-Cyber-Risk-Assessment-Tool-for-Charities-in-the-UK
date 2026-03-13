# app.py
# Cyber Risk Assessment Tool (UK Charities)
# Author: Aisha Moussa

import json
import streamlit as st
import pandas as pd
import altair as alt

from ux import apply_styles, hero_card
from questionnaire import QUESTIONNAIRE, DOMAIN_QUESTION_IDS, SCALE_LABELS
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
            st.session_state[q["id"]] = 0  # default "not in place" to avoid biased demo outputs
        responses[q["id"]] = st.session_state[q["id"]]


# -------------------------
# TAB 1: Assessment
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
    st.caption("Scores represent organisational maturity (not individual staff performance).")

    with st.expander("What do the scores mean? (0-4)", expanded=False):
        for k in range(0, 5):
            st.write(f"**{k}** — {SCALE_LABELS[k]}")

    for domain, questions in QUESTIONNAIRE.items():
        with st.expander(domain, expanded=True):
            for q in questions:
                value = st.slider(
                    f"{q['id']} - {q['question']}",
                    0, 4,
                    value=int(st.session_state[q["id"]]),
                    step=1,
                    key=q["id"]
                )
                st.caption(f"**Selected:** {value} — {SCALE_LABELS[value]}")


# -------------------------
# TAB 2: Results
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

        chart_df = weakness_df.reset_index()
        chart_df.columns = ["Domain", "Weakness"]

        chart = (
            alt.Chart(chart_df)
            .mark_bar()
            .encode(
                x=alt.X("Domain:N", sort="-y"),
                y=alt.Y("Weakness:Q", scale=alt.Scale(domain=[0, 4])),
                color=alt.Color(
                    "Weakness:Q",
                    scale=alt.Scale(
                        domain=[0, 1.5, 2.5, 3.5, 4],
                        range=["#16A34A", "#EAB308", "#F97316", "#B91C1C", "#7F1D1D"],
                    ),
                    legend=alt.Legend(title="Weakness"),
                ),
                tooltip=["Domain:N", "Weakness:Q"],
            )
        )

        st.altair_chart(chart, use_container_width=True)

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
This prototype was developed to support **small UK charities** in identifying cyber risk in a way that is structured, accessible, and practical for organisations with limited technical resources.

Many charities face growing exposure to threats such as **phishing, credential compromise, ransomware, and unauthorised access to donor or beneficiary data**, yet often operate without dedicated cyber-security staff. In these environments, complex enterprise frameworks may be difficult to apply directly. This tool therefore translates key cyber-risk concepts into a lightweight self-assessment that can support early prioritisation of improvements.

### Purpose of the tool
The aim of the tool is to help a charity, trustee, senior manager, or assessor form an indicative view of the organisation’s current cyber-risk posture by combining:
- **control maturity** across five core cyber-security functions
- **organisational impact context**
- a simple **risk scoring model** that turns responses into prioritised outputs

### Framework basis
The questionnaire is structured around the five core functions of **NIST CSF 2.0**:
- **Identify**
- **Protect**
- **Detect**
- **Respond**
- **Recover**

These functions were used as a conceptual structure for the questionnaire rather than as a formal compliance checklist.

The scoring logic is **inspired by NIST SP 800-30**, using the principle that:

**Risk = Likelihood x Impact**

In this prototype:
- **maturity** is scored from 0-4
- **weakness = 4 - maturity**
- higher weakness contributes to higher **likelihood**
- **impact** is estimated from charity context: data sensitivity, operational dependency, financial exposure, and reputational risk

### Why this tool is organisational rather than employee-based
The questionnaire is written from an **organisational assessment perspective**. It is intended to reflect the maturity of charity-wide controls, responsibilities, and practices rather than the confidence or awareness of a single staff member.

This decision was made because, in small and scaling charities, responses can vary significantly between staff and volunteers, especially where **BYOD**, informal processes, and turnover are common. An organisational perspective improves consistency and aligns more closely with governance-focused risk assessment.

### Why Streamlit was used
**Streamlit** was selected because it supports rapid prototyping, clear visual presentation, and interactive input collection with relatively low development overhead. This made it suitable for building a lightweight academic prototype that could display scores, charts, rankings, and downloadable evidence in a simple browser-based interface.

### How to interpret results
- **0–4 maturity scale** indicates how far a control is in place
- lower maturity produces higher weakness
- higher weakness increases estimated likelihood
- the weakest domains are ranked to help prioritise improvement efforts

### Limitations
This tool is an **indicative prototype**, not a compliance audit or formal certification mechanism.
Its limitations include:
- self-reported inputs
- simplified scoring logic
- equal weighting across domains in the current version
- recommendations that are rule-based rather than fully context-adaptive

### Future development
Future work could extend the tool by:
- adding **domain weighting**
- introducing **red-flag rules** for critical missing controls
- supporting **multiple respondents within a charity**
- aggregating responses to highlight perception gaps and governance inconsistencies
- strengthening automated testing and recommendation personalisation
"""
    )
