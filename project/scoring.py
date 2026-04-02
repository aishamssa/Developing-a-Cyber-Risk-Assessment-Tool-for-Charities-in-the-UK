# scoring.py

# risk scoring engine for the tool
# this is where questionnaire maturity gets turned into likelihood, impact, and overall risk

# i kept the scoring logic separate from the streamlit app so it could be
# tested independently and changed without breaking the ui

MAX_SCORE = 4
LOW_RISK_THRESHOLD = 4
MEDIUM_RISK_THRESHOLD = 9
TOP_WEAK_DOMAINS = 2

# current thresholds are intentionally simple for interpretability in the prototype version

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
    """
    # averaging at domain level makes the output easier to interpret than
    # treating every question as a separate result
    domain_scores = {}
    for domain, qids in domain_question_ids.items():
        scores = [responses[qid] for qid in qids]
        domain_scores[domain] = round(sum(scores) / len(scores), 2)
    return domain_scores


def calculate_likelihood(domain_scores, domain_weights=None):
    """
    Converts maturity into a likelihood estimate.
    """
    # for this prototype i kept weights optional because equal weighting keeps
    # the model simple + easier to explain, but it could be extended later
    if domain_weights is None:
        domain_weights = {d: 1 for d in domain_scores.keys()}

    total_weight = sum(domain_weights.values())
    weighted_weakness = 0

    for domain, maturity in domain_scores.items():
        # lower maturity should increase likelihood, so i invert it into weakness
        weakness = MAX_SCORE - maturity
        weighted_weakness += weakness * domain_weights.get(domain, 1)

    likelihood = weighted_weakness / total_weight
    return round(likelihood, 2)


def calculate_impact(context):
    """
    Estimates impact from charity context factors.
    """
    # impact is kept separate because two charities can have similar gaps
    # but very different consequences if something goes wrong
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
    Calculates overall risk score.
    """
    # simplified version of nist sp 800-30:
    # not full threat modelling, but enough for a usable prototype
    return round(likelihood * impact, 2)


def risk_band(risk_score):
    """
    Categorises risk into bands.
    """
    # bands make results easier to understand in the ui
    if risk_score < LOW_RISK_THRESHOLD:
        return "Low"
    elif risk_score < MEDIUM_RISK_THRESHOLD:
        return "Medium"
    return "High"


def rank_weak_domains(domain_scores):
    """
    Sorts domains by weakness (worst first).
    """
    weaknesses = []
    for domain, score in domain_scores.items():
        weaknesses.append((domain, round(MAX_SCORE - score, 2)))

    # sorting worst-first helps prioritise action
    weaknesses.sort(key=lambda x: x[1], reverse=True)
    return weaknesses


def generate_recommendations(domain_scores):
    """
    Generate recommendations based on weakest domains.
    """
    ranked = rank_weak_domains(domain_scores)

    if not ranked:
        return []

    # if everything is already strong, do not force recommendations
    if ranked[0][1] <= 0.5:
        return []

    # only focus on top 2 weakest domains to keep output realistic
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
    Main scoring pipeline used by the app.
    """
    # keeping one main function made it easier to plug into streamlit
    # and also easier to test the full flow with pytest
    domain_scores = calculate_domain_scores(responses, domain_question_ids)
    likelihood = calculate_likelihood(domain_scores, domain_weights=domain_weights)
    impact = calculate_impact(context)
    risk = calculate_risk(likelihood, impact)

    return {
        "domain_scores": domain_scores,
        "likelihood": likelihood,
        "impact": impact,
        "risk_score": risk,
        "risk_band": risk_band(risk),
        "weak_domain_ranking": rank_weak_domains(domain_scores),
        "recommendations": generate_recommendations(domain_scores)
    }