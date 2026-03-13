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

MAX_SCORE = 4
LOW_RISK_THRESHOLD = 4
MEDIUM_RISK_THRESHOLD = 9
TOP_WEAK_DOMAINS = 2

DOMAIN_RECOMMENDATIONS = {
    "Identify": [
        "Create and maintain a simple asset and data inventory covering key accounts, devices, systems, and sensitive information.",
        "Define and review access responsibilities so the charity knows who can access which systems and data.",
        "Document the use of personal devices and external accounts where they are used to access charity resources."
    ],
    "Protect": [
        "Apply stronger account protections, including unique accounts, password guidance, and multi-factor authentication where available.",
        "Introduce short, repeatable phishing-awareness guidance for staff and volunteers.",
        "Use access controls, permissions, and secure storage practices to reduce exposure of donor, beneficiary, and financial data."
    ],
    "Detect": [
        "Enable basic monitoring and alerting for important accounts, especially email and cloud platforms.",
        "Define simple checking procedures when suspicious activity is reported, such as reviewing logins or resetting passwords.",
        "Establish a clear and visible reporting route for suspected cyber-security issues."
    ],
    "Respond": [
        "Develop a short incident response checklist covering phishing, account compromise, and data-loss scenarios.",
        "Assign a named incident coordinator who can organise actions and escalation during an event.",
        "Record incident actions and decisions to support evidence, review, and learning."
    ],
    "Recover": [
        "Ensure important data is backed up and that backups can be accessed when needed.",
        "Define how essential services would be restored after an incident, including realistic recovery priorities.",
        "Review incidents and near-misses after they occur and update practices accordingly."
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
    Generate practical recommendations based on the weakest domains.
    """
    ranked = rank_weak_domains(domain_scores)
    weakest_domains = [domain for domain, _ in ranked[:TOP_WEAK_DOMAINS]]

    recs = []
    for domain in weakest_domains:
        recs.extend(DOMAIN_RECOMMENDATIONS.get(domain, []))

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
