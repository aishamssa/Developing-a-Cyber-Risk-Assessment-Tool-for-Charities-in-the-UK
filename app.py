# app.py
# Cyber Risk Assessment Tool (UK Charities)
# Author: Aisha Moussa
#
# What this file does (in plain English):
# - This is the UI/controller layer (Streamlit).
# - I collect questionnaire answers + charity context inputs (impact factors).
# - I pass those inputs into my scoring engine (scoring.py).
# - Then I display results (risk band, likelihood, impact, charts, tables) + export JSON evidence.
#
# Why I kept logic out of this file:
# - Streamlit reruns the script top-to-bottom each interaction.
# - So I keep the maths/scoring in scoring.py to maintain separation of concerns
#   (cleaner architecture + easier to test later with pytest).

import json
import streamlit as st
import pandas as pd
from ux import apply_styles, hero_card, weakness_color, badge


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
# Session state (super important in Streamlit)
# -------------------------
# Streamlit reruns the whole script when any widget changes.
# To stop results disappearing when I switch tabs / move sliders,
# I store computed results inside st.session_state.
if "result" not in st.session_state:
    st.session_state.result = None

# I also store a timestamp/version-ish marker (useful for evidence + “engineering vibes”)
if "last_calculated" not in st.session_state:
    st.session_state.last_calculated = None

# -------------------------
# Sidebar: charity context (Impact inputs)
# -------------------------
# I treat these as "Impact" factors (NIST SP 800-30 concept).
# They capture how damaging an incident would be depending on what the charity handles.
st.sidebar.header("Charity context (Impact inputs)")

templates = context_templates()

template_choice = st.sidebar.selectbox(
    "Choose a template (optional)",
    ["Custom (enter your own)"] + list(templates.keys()),
    key="template_choice"
)

ctx = default_charity_context()

if template_choice != "Custom (enter your own)":
    # apply template values onto ctx
    ctx.update(templates[template_choice])


ctx["charity_name"] = st.sidebar.text_input("Charity name", value=ctx["charity_name"], key="charity_name")
ctx["data_sensitivity"] = st.sidebar.slider(
    "Data sensitivity (0–4)",
    0, 4, int(ctx["data_sensitivity"]),
    help="How sensitive is the data? (e.g., beneficiaries, donor details, finance)",
    key="data_sens"
)
ctx["operational_dependency"] = st.sidebar.slider(
    "Operational dependency (0–4)",
    0, 4, int(ctx["operational_dependency"]),
    help="How badly would disruption affect daily operations?",
    key="ops_dep"
)
ctx["financial_exposure"] = st.sidebar.slider(
    "Financial exposure (0–4)",
    0, 4, int(ctx["financial_exposure"]),
    help="How much financial loss could result from an incident?",
    key="fin_exp"
)
ctx["reputational_risk"] = st.sidebar.slider(
    "Reputational risk (0–4)",
    0, 4, int(ctx["reputational_risk"]),
    help="How damaging would the loss of trust be (donors, community, regulators)?",
    key="rep_risk"
)

# -------------------------
# Tabs (main navigation)
# -------------------------
tab1, tab2, tab3 = st.tabs(["Assessment", "Results", "About"])

# -------------------------
# Build responses dict from session_state
# -------------------------
# I store each question slider using its ID as the widget key (e.g. "ID1", "PR2").
# Streamlit automatically keeps widget values in st.session_state by key.
responses = {}
for domain, questions in QUESTIONNAIRE.items():
    for q in questions:
        if q["id"] not in st.session_state:
            # Default = 2 means "partially in place"
            st.session_state[q["id"]] = 2
        responses[q["id"]] = st.session_state[q["id"]]

# -------------------------
# TAB 1: Assessment (questionnaire)
# -------------------------
with tab1:
    st.header("Questionnaire (0 = not in place, 4 = fully in place)")
    st.caption("Tip: answer honestly. This is an indicative self-assessment, not a compliance audit.")

    # I grouped questions by NIST CSF functions (Identify, Protect, Detect, Respond, Recover)
    # so the output can show strengths/weaknesses by domain.
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

    # I calculate the score only when user clicks the button.
    # (This avoids re-scoring on every slider change.)
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
        # -------------------------
        # Top metrics (quick summary)
        # -------------------------
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Risk band", result["risk_band"])
        col2.metric("Likelihood", result["likelihood"])
        col3.metric("Impact", result["impact"])
        col4.metric("Risk score", result["risk_score"])

        if st.session_state.last_calculated:
            st.caption(f"Last calculated: {st.session_state.last_calculated}")

        # -------------------------
        # Domain analysis (chart + tables)
        # -------------------------
        st.subheader("Cyber risk exposure by domain (higher = weaker)")
        st.caption("This chart visualises weakness = 4 − maturity. Higher weakness contributes to higher likelihood.")

        # Domain maturity dataframe
        domain_df = pd.DataFrame.from_dict(
            result["domain_scores"],
            orient="index",
            columns=["Maturity (0–4)"]
        )
        domain_df.index.name = "Domain"

        # Weakness dataframe (Streamlit likes a simple numeric column + index)
        weakness_df = domain_df.copy()
        weakness_df["Weakness (0–4)"] = 4 - weakness_df["Maturity (0–4)"]
        weakness_df = weakness_df[["Weakness (0–4)"]]

        # Bar chart
        st.bar_chart(weakness_df)

        # Table: show maturity + weakness together (more “final year” than raw JSON)
        combined_df = domain_df.join(weakness_df)
        st.dataframe(combined_df.style.format("{:.2f}"), use_container_width=True)

        # -------------------------
        # Weakest areas (priority order)
        # -------------------------
        st.subheader("Weakest areas (priority order)")
        weak_df = pd.DataFrame(result["weak_domain_ranking"], columns=["Domain", "Weakness (0–4)"])
        weak_df.index = range(1, len(weak_df) + 1)
        weak_df.index.name = "Priority"
        st.dataframe(weak_df.style.format({"Weakness (0–4)": "{:.2f}"}), use_container_width=True)

        # A short “interpretation” paragraph (helps non-technical users + helps your report narrative)
        top_domain = weak_df.iloc[0]["Domain"]
        st.info(
            f"Interpretation: your highest exposure is currently **{top_domain}**. "
            "Improving controls in the weakest domain(s) should reduce likelihood and overall risk score."
        )

        # -------------------------
        # Recommendations
        # -------------------------
        st.subheader("Recommendations")
        # I keep recommendations rule-based for now (simple expert system),
        # tied to the weakest domains.
        try:
            with st.container(border=True):
                for r in result["recommendations"]:
                    st.write(f"• {r}")
        except TypeError:
            # Fallback for older Streamlit versions without border containers
            for r in result["recommendations"]:
                st.info(r)

        # -------------------------
        # Export evidence (for report + testing)
        # -------------------------
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
# TAB 3: About (method + justification)
# -------------------------
with tab3:
    st.header("About this tool")

    # I keep the About page short in the UI, but this maps directly to the report sections.
    st.write(
        """
This prototype helps UK charities estimate cyber risk using:

- **NIST CSF 2.0** domains (Identify, Protect, Detect, Respond, Recover) to structure the questionnaire  
- **NIST SP 800-30-inspired** logic: *Risk = Likelihood × Impact*

**How to interpret results**
- *Maturity (0–4)* reflects how much a control is in place.
- *Weakness = 4 − maturity* (higher weakness increases likelihood).
- *Impact* is based on charity context: sensitivity, operations, finance, reputation.

**Limitations (being honest)**
- Answers are self-reported (so results depend on honest inputs).
- The scoring model is intentionally lightweight to stay usable for small charities.
- Future work could add domain weights, red-flag rules (e.g., “no backups”), and deeper validation/testing.
"""
    )
