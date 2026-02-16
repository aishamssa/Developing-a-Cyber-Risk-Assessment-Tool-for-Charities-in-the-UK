# NIST-Aligned Risk Calculation Engine
# This script contains the core mathematical and logical functions of your tool. It operationalises the NIST SP 800-30 risk model by computing likelihood, impact, and an overall risk score. 
# The scoring engine will eventually integrate domain weights, question importance, and customised recommendations. 
# Early in the project, this script will simply apply basic formulas to demonstrate system functionality. 
# As the implementation matures, the scoring logic will be refined and documented. 
# This module represents the analytical heart of the project and demonstrates your ability to translate theoretical cybersecurity frameworks into a functioning computational system.


# scoring.py
# NIST SP 800-30 inspired scoring engine (likelihood + impact -> risk)
# This module operationalises your risk logic:
# - Questionnaire maturity (0-4) approximates control strength per CSF function
# - Likelihood is higher when maturity is lower (more weaknesses)
# - Impact is derived from organisational context (data sensitivity, ops dependency etc.)
# Risk score = Likelihood × Impact

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
    Converts maturity into likelihood (0-4).
    Weakness = 4 - maturity.
    Weighted average weakness = likelihood estimate.
    """
    if domain_weights is None:
        domain_weights = {d: 1 for d in domain_scores.keys()}

    total_weight = sum(domain_weights.values())
    weighted_weakness = 0

    for domain, maturity in domain_scores.items():
        weakness = 4 - maturity
        weighted_weakness += weakness * domain_weights.get(domain, 1)

    likelihood = weighted_weakness / total_weight
    return round(likelihood, 2)


def calculate_impact(context):
    """
    Impact magnitude estimated from charity context.
    Values are 0-4, averaged to produce 0-4 impact score.
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
    Overall risk score (0-16) since both are 0-4.
    """
    return round(likelihood * impact, 2)


def risk_band(risk_score):
    """
    Simple banding for user-friendly outputs.
    """
    if risk_score < 4:
        return "Low"
    elif risk_score < 9:
        return "Medium"
    else:
        return "High"


def rank_weak_domains(domain_scores):
    """
    Returns list of (domain, weakness) sorted worst-first.
    """
    weaknesses = []
    for domain, score in domain_scores.items():
        weaknesses.append((domain, round(4 - score, 2)))

    weaknesses.sort(key=lambda x: x[1], reverse=True)
    return weaknesses


def generate_recommendations(domain_scores):
    """
    Lightweight recommendations tied to CSF functions.
    Picks the 2 weakest domains and suggests practical next steps.
    """
    ranked = rank_weak_domains(domain_scores)
    weakest_domains = [ranked[0][0], ranked[1][0]] if len(ranked) >= 2 else [ranked[0][0]]

    recs = []

    for d in weakest_domains:
        if d == "Identify":
            recs.append("Create a simple inventory of key accounts, devices, and the types of sensitive data held (donor/beneficiary/finance).")
            recs.append("Clarify who can access what (even a basic spreadsheet of roles and access helps).")

        elif d == "Protect":
            recs.append("Enable multi-factor authentication on email, cloud storage and finance systems.")
            recs.append("Introduce short phishing awareness guidance for staff/volunteers and basic device hygiene (screen locks, updates).")

        elif d == "Detect":
            recs.append("Set up basic alerts (e.g., email login alerts) and encourage reporting of suspicious emails immediately.")
            recs.append("Check key accounts weekly for unusual activity (manual monitoring is still monitoring).")

        elif d == "Respond":
            recs.append("Write a one-page incident checklist: who to contact, how to reset passwords, how to isolate affected accounts.")
            recs.append("Decide who leads incident response (named person/role) and when to escalate to external IT help.")

        elif d == "Recover":
            recs.append("Ensure backups exist, are protected, and test a basic restore process (even once a month).")
            recs.append("After any incident/near-miss, record what happened and one improvement action for next time.")

    return recs


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
