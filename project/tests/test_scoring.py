
import pytest

from scoring import (
    calculate_domain_scores,
    calculate_likelihood,
    calculate_impact,
    calculate_risk,
    risk_band,
    rank_weak_domains,
    generate_recommendations,
    run_assessment,
)


def test_domain_score_calculation():
    responses = {"Q1": 4, "Q2": 2}
    domain_question_ids = {"Identify": ["Q1", "Q2"]}

    result = calculate_domain_scores(responses, domain_question_ids)

    assert result["Identify"] == 3.0


def test_likelihood_calculation():
    domain_scores = {
        "Identify": 4,
        "Protect": 2,
    }

    likelihood = calculate_likelihood(domain_scores)

    assert likelihood == 1.0


def test_likelihood_with_weights():
    domain_scores = {
        "Identify": 4,
        "Protect": 2,
    }
    domain_weights = {
        "Identify": 1,
        "Protect": 3,
    }

    likelihood = calculate_likelihood(domain_scores, domain_weights=domain_weights)

    assert likelihood == 1.5


def test_impact_calculation():
    context = {
        "data_sensitivity": 3,
        "operational_dependency": 4,
        "financial_exposure": 2,
        "reputational_risk": 3,
    }

    impact = calculate_impact(context)

    assert impact == 3.0


def test_risk_calculation():
    risk = calculate_risk(3, 3)

    assert risk == 9


def test_risk_band_low():
    assert risk_band(2) == "Low"


def test_risk_band_medium():
    assert risk_band(6) == "Medium"


def test_risk_band_high():
    assert risk_band(12) == "High"


def test_rank_weak_domains():
    domain_scores = {
        "Identify": 4,
        "Protect": 1,
        "Detect": 2,
    }

    ranked = rank_weak_domains(domain_scores)

    assert ranked[0][0] == "Protect"
    assert ranked[0][1] == 3.0


def test_generate_recommendations_returns_output():
    domain_scores = {
        "Identify": 4,
        "Protect": 1,
        "Detect": 2,
        "Respond": 3,
        "Recover": 4,
    }

    recs = generate_recommendations(domain_scores)

    assert len(recs) > 0


def test_generate_recommendations_uses_top_two_domains():
    domain_scores = {
        "Identify": 4,
        "Protect": 0,
        "Detect": 1,
        "Respond": 4,
        "Recover": 4,
    }

    recs = generate_recommendations(domain_scores)

    assert len(recs) == 2
    assert recs[0]["domain"] == "Protect"
    assert recs[0]["priority"] == 1
    assert recs[0]["weakness"] == 4
    assert len(recs[0]["recommendations"]) == 3

    assert recs[1]["domain"] == "Detect"
    assert recs[1]["priority"] == 2
    assert recs[1]["weakness"] == 3
    assert len(recs[1]["recommendations"]) == 3


def test_run_assessment_returns_expected_keys():
    responses = {
        "ID1": 2, "ID2": 2, "ID3": 2, "ID4": 2,
        "PR1": 2, "PR2": 2, "PR3": 2, "PR4": 2,
        "DE1": 2, "DE2": 2, "DE3": 2, "DE4": 2,
        "RS1": 2, "RS2": 2, "RS3": 2, "RS4": 2,
        "RC1": 2, "RC2": 2, "RC3": 2, "RC4": 2,
    }

    domain_question_ids = {
        "Identify": ["ID1", "ID2", "ID3", "ID4"],
        "Protect": ["PR1", "PR2", "PR3", "PR4"],
        "Detect": ["DE1", "DE2", "DE3", "DE4"],
        "Respond": ["RS1", "RS2", "RS3", "RS4"],
        "Recover": ["RC1", "RC2", "RC3", "RC4"],
    }

    context = {
        "charity_name": "Test Charity",
        "data_sensitivity": 2,
        "operational_dependency": 2,
        "financial_exposure": 2,
        "reputational_risk": 2,
    }

    result = run_assessment(responses, domain_question_ids, context)

    assert "domain_scores" in result
    assert "likelihood" in result
    assert "impact" in result
    assert "risk_score" in result
    assert "risk_band" in result
    assert "weak_domain_ranking" in result
    assert "recommendations" in result


def test_run_assessment_with_balanced_inputs():
    responses = {
        "ID1": 4, "ID2": 4, "ID3": 4, "ID4": 4,
        "PR1": 4, "PR2": 4, "PR3": 4, "PR4": 4,
        "DE1": 4, "DE2": 4, "DE3": 4, "DE4": 4,
        "RS1": 4, "RS2": 4, "RS3": 4, "RS4": 4,
        "RC1": 4, "RC2": 4, "RC3": 4, "RC4": 4,
    }

    domain_question_ids = {
        "Identify": ["ID1", "ID2", "ID3", "ID4"],
        "Protect": ["PR1", "PR2", "PR3", "PR4"],
        "Detect": ["DE1", "DE2", "DE3", "DE4"],
        "Respond": ["RS1", "RS2", "RS3", "RS4"],
        "Recover": ["RC1", "RC2", "RC3", "RC4"],
    }

    context = {
        "charity_name": "Low Risk Charity",
        "data_sensitivity": 1,
        "operational_dependency": 1,
        "financial_exposure": 1,
        "reputational_risk": 1,
    }


    result = run_assessment(responses, domain_question_ids, context)

    assert result["likelihood"] == 0.0
    assert result["impact"] == 1.0
    assert result["risk_score"] == 0.0
    assert result["risk_band"] == "Low"