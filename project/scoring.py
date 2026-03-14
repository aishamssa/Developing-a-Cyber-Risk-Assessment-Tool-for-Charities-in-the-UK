# scoring.py
# Risk scoring engine for the Cyber Risk Assessment Tool.
# Implements a simplified NIST SP 800-30 inspired model:
# Risk = Likelihood x Impact.
#
# Likelihood is derived from questionnaire maturity scores
# across the NIST CSF domains (Identify, Protect, Detect,
# Respond, Recover). Impact is estimated from organisational
# context factors such as data sensitivity, operational
# dependency, financial exposure, and reputational risk.

MAX_SCORE = 4
LOW_RISK_THRESHOLD = 4
MEDIUM_RISK_THRESHOLD = 9
TOP_WEAK_DOMAINS = 2

DOMAIN_RECOMMENDATIONS = {
    "Identify": [
        "Create and maintain a simple inventory of charity devices, accounts, systems, and sensitive data such as donor, beneficiary, and finance records.",
        "Define who is responsible for cyber-risk oversight and review which staff or volunteers can access important systems and data.",
        "Document where charity information is stored and whether personal devices or third-party accounts are being used to access it."
    ],
    "Protect": [
        "Strengthen access security by enabling multi-factor authentication on email, cloud storage, and other important charity systems where possible.",
        "Apply clear password and account management rules, including unique accounts, appropriate permissions, and regular access review.",
        "Provide short, practical phishing-awareness guidance for staff and volunteers, especially where donor or financial data is handled."
    ],
    "Detect": [
        "Enable basic alerts and monitoring for important accounts, particularly email and cloud platforms used for charity operations.",
        "Define simple checks for suspicious activity, such as reviewing unusual logins, verifying messages, and resetting compromised accounts.",
        "Ensure there is a clear reporting route so staff and volunteers know how to raise suspected cyber-security concerns quickly."
    ],
    "Respond": [
        "Create a short incident response checklist covering common scenarios such as phishing, account compromise, and data loss.",
        "Assign a named person or role to coordinate incident handling, escalation, and communication during a cyber event.",
        "Keep a basic incident record of what happened, what actions were taken, and what follow-up improvements are needed."
    ],
    "Recover": [
        "Ensure important charity data is backed up and that backup access is understood before an incident occurs.",
        "Define how key services such as email, donor systems, or finance records would be restored after disruption.",
        "Review incidents and near-misses to identify lessons learned, update responsibilities, and improve future recovery readiness."
    ]
}

def calculate_domain_scores(responses, domain_question_ids):
    """
    Calculates average maturity per CSF domain.
    responses: dict like {"ID1": 3, "PR1": 2, ...}
    domain_question_ids: dict like {"Identify": ["ID1","ID2"], ...}
    """
    domain_scores = {}
    for domain, qids in domain_question_ids.items():
        scores = [responses[qid] for qid in qids]
        domain_scores[domain] = round(sum(scores) / len(scores), 2)
    return domain_scores


def calculate_likelihood(domain_scores, domain_weights=None):
    """
    Converts maturity into a likelihood estimate on the same scale as the questionnaire.
    Weakness is calculated as MAX_SCORE minus maturity.
    A weighted average of weakness values produces the likelihood score.
    """
    if domain_weights is None:
        domain_weights = {d: 1 for d in domain_scores.keys()}

    total_weight = sum(domain_weights.values())
    weighted_weakness = 0

    for domain, maturity in domain_scores.items():
        weakness = MAX_SCORE - maturity
        weighted_weakness += weakness * domain_weights.get(domain, 1)

    likelihood = weighted_weakness / total_weight
    return round(likelihood, 2)


def calculate_impact(context):
    """
    Estimates impact from charity context factors.
    All context values use the same 0- MAX_SCORE scale and are averaged.
    """
    factors = [
        context["data_sensitivity"],
        context["operational_dependency"],
        context["financial_exposure"],
        context["reputational_risk"]
    ]
    impact = sum(factors) / len(factors)
    return round(impact, 2)


def calculate_risk(likelihood, impact):
    """
    Calculates the overall risk score as likelihood x impact.
    """
    return round(likelihood * impact, 2)


def risk_band(risk_score):
    """
    Categorises risk score into user-friendly bands.
    """
    if risk_score < LOW_RISK_THRESHOLD:
        return "Low"
    elif risk_score < MEDIUM_RISK_THRESHOLD:
        return "Medium"
    return "High"


def rank_weak_domains(domain_scores):
    """
    Returns list of (domain, weakness) sorted worst-first.
    """
    weaknesses = []
    for domain, score in domain_scores.items():
        weaknesses.append((domain, round(MAX_SCORE - score, 2)))

    weaknesses.sort(key=lambda x: x[1], reverse=True)
    return weaknesses


def generate_recommendations(domain_scores):
    """
    Generate structured recommendations based on the weakest domains.

    Rules:
    - Rank domains by weakness
    - If all domains are already strong, return no urgent recommendations
    - Otherwise return grouped recommendations for the two weakest domains
    """
    ranked = rank_weak_domains(domain_scores)

    # If the strongest recommendation need is very small, do not force priorities
    if not ranked:
        return []

    if ranked[0][1] <= 0.5:
        return []

    weakest_domains = ranked[:TOP_WEAK_DOMAINS]

    grouped_recommendations = []

    for priority, (domain, weakness) in enumerate(weakest_domains, start=1):
        grouped_recommendations.append({
            "priority": priority,
            "domain": domain,
            "weakness": weakness,
            "recommendations": DOMAIN_RECOMMENDATIONS.get(domain, [])
        })

    return grouped_recommendations


def run_assessment(responses, domain_question_ids, context, domain_weights=None):
    """
    Main function used by Streamlit (app.py).
    Returns a structured result dictionary for UI + reporting.
    """
    domain_scores = calculate_domain_scores(responses, domain_question_ids)
    likelihood = calculate_likelihood(domain_scores, domain_weights=domain_weights)
    impact = calculate_impact(context)
    risk = calculate_risk(likelihood, impact)

    result = {
        "domain_scores": domain_scores,
        "likelihood": likelihood,
        "impact": impact,
        "risk_score": risk,
        "risk_band": risk_band(risk),
        "weak_domain_ranking": rank_weak_domains(domain_scores),
        "recommendations": generate_recommendations(domain_scores)
    }
    return result
