# questionnaire.py
# Questionnaire model for the tool
# - Defines the 0–4 maturity scale
# - Defines question banks per NIST CSF function
# - Exposes QUESTIONNAIRE and DOMAIN_QUESTION_IDS for the UI + scoring engine

# questionnaire.py

SCALE_LABELS = {
    0: "Not in place (no evidence, not done)",
    1: "Ad hoc (done sometimes, inconsistent, depends on individuals)",
    2: "Partial (some controls exist, but gaps + not standardised)",
    3: "Mostly (implemented for most areas, minor gaps remain)",
    4: "Fully (consistent, documented, reviewed/improved)",
}

identify_questions = [
    {
        "id": "ID1",
        "question": (
            "Is there an agreed understanding of what sensitive data the charity holds "
            "(e.g., donor, beneficiary, financial) and where it is stored?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID2",
        "question": (
            "Is access to sensitive data/systems defined and reviewed when staff/volunteers join or leave?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID3",
        "question": (
            "Is there visibility of which devices and accounts are used to access charity systems "
            "(including personal/BYOD), even if recorded informally?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID4",
        "question": (
            "Is cyber/data risk responsibility assigned (e.g., named person/role) and understood across the charity?"
        ),
        "scale": "0-4"
    },
]

protect_questions = [
    {
        "id": "PR1",
        "question": (
            "Are accounts and passwords managed using consistent rules "
            "(e.g., unique accounts, password guidance, MFA where possible)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR2",
        "question": (
            "Is phishing awareness guidance or training provided and refreshed "
            "(even lightweight: briefing, checklist, short session)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR3",
        "question": (
            "Is sensitive data protected through access restrictions and/or secure storage practices "
            "(e.g., limited sharing, permissions, encryption where available)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR4",
        "question": (
            "Are devices and key software kept updated using a routine process "
            "(automatic updates or scheduled checks)?"
        ),
        "scale": "0-4"
    },
]

detect_questions = [
    {
        "id": "DE1",
        "question": (
            "Are there routine ways to spot suspicious activity "
            "(e.g., monitoring alerts, unusual login notifications, checking account access)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE2",
        "question": (
            "When something seems wrong, are defined checks carried out "
            "(e.g., password resets, reviewing logins, verifying emails)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE3",
        "question": (
            "Is there a clear reporting route for suspected cyber issues "
            "(e.g., named contact, dedicated email, simple process)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE4",
        "question": (
            "Are any protective tools or services used "
            "(even basic: spam filtering, antivirus, device security, managed email protections)?"
        ),
        "scale": "0-4"
    },
]

respond_questions = [
    {
        "id": "RS1",
        "question": (
            "Are response steps defined for common incidents (phishing, account compromise, data loss), "
            "even as a short checklist?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS2",
        "question": (
            "Is a coordinator identified to manage incident actions and decisions during an event?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS3",
        "question": (
            "Are notification requirements understood "
            "(internal escalation and external reporting where applicable)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS4",
        "question": (
            "Are incident actions recorded in any way (notes, timeline, what was done, outcomes) "
            "to support learning and evidence?"
        ),
        "scale": "0-4"
    },
]

recover_questions = [
    {
        "id": "RC1",
        "question": (
            "Are backups in place for important data, and can the charity access them if systems/files are lost?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC2",
        "question": (
            "Is there a realistic plan to restore key operations after an incident "
            "(e.g., email, donor systems, finance), including time expectations?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC3",
        "question": (
            "Are recovery responsibilities allocated "
            "(who restores systems, who communicates, who verifies data integrity)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC4",
        "question": (
            "After an incident or near-miss, does the charity review what happened and update practices accordingly?"
        ),
        "scale": "0-4"
    },
]

QUESTIONNAIRE = {
    "Identify": identify_questions,
    "Protect": protect_questions,
    "Detect": detect_questions,
    "Respond": respond_questions,
    "Recover": recover_questions
}

DOMAIN_QUESTION_IDS = {
    domain: [q["id"] for q in questions]
    for domain, questions in QUESTIONNAIRE.items()
}


