# ux.py
# Tiny UX helper module (keeps app.py cleaner)
# Author: Aisha Moussa
#
# What this file does:
# - Holds my CSS styling (cards, badges, spacing)
# - Holds colour logic for weakness (0–4)
# - Gives me small reusable UI helpers (hero card + badge)

import streamlit as st


CSS = """
<style>
/* Make the app feel less "default Streamlit" */
.block-container { padding-top: 2.0rem; max-width: 1150px; }

/* Soft card */
.card {
  background: #ffffff;
  border: 1px solid #E8EAF2;
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
  margin-bottom: 14px;
}

/* Small helper text */
.muted { color: rgba(15,23,42,0.72); }

/* Badge */
.badge {
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.85rem;
  border: 1px solid rgba(15,23,42,0.10);
}
</style>
"""


def apply_styles():
    """Inject global CSS once at the top of the app."""
    st.markdown(CSS, unsafe_allow_html=True)


def hero_card():
    """Simple header card so the app feels warmer + more 'charity-friendly'."""
    st.markdown("""
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:14px;">
        <div>
          <div style="font-size:2.2rem; font-weight:900; line-height:1.1;">
            Cyber Risk Assessment Tool (UK Charities)
          </div>
          <p class="muted" style="margin-top:8px;">
            A lightweight self-assessment to help charities prioritise cyber improvements — without jargon.
          </p>
        </div>
        <div style="font-size:38px;"> </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def weakness_color(v: float) -> str:
    """
    Map weakness score (0..4) to a friendly risk colour.
    Higher weakness = worse = warmer colour.
    """
    if v >= 3.5: return "#B91C1C"  # deep red
    if v >= 2.5: return "#F97316"  # orange
    if v >= 1.5: return "#EAB308"  # yellow
    return "#16A34A"               # green


def weakness_label(v: float) -> str:
    """Human label for weakness banding."""
    if v >= 3.5: return "Critical"
    if v >= 2.5: return "High"
    if v >= 1.5: return "Moderate"
    return "Low"


def badge(text: str, color: str):
    """Small coloured badge (used under sliders / in results)."""
    st.markdown(
        f"<span class='badge' style='background:{color}15; color:{color};'>{text}</span>",
        unsafe_allow_html=True
    )
