''' Answer Mapping and Data Preparation
This module contains the logic that transforms human-readable responseS into numerical or categorical values used by the scoring engine. 
It also groups questions by cybersecurity domain (e.g., Identify, Protect, Detect, Respond, Recover), reflecting the structure of the NIST CSF. 
The module ensures that user input is interpreted consistently and accurately, which is essential in a risk-assessment tool where subjective answers must be converted into objective scoring inputs. 
This script essentially acts as the bridge between the qualitative questionnaire and the quantitative scoring model. '''

# -------------------------
# IDENTIFY DOMAIN
# -------------------------
# This section assesses how well the charity understands its assets,
# data, access arrangements, and cyber risk responsibilities.
# Poor visibility in this area increases both the likelihood and
# potential impact of cyber incidents.

identify_questions = [
    {
        "id": "ID1",
        "question": (
            "Does the charity have a clear understanding of the types "
            "of sensitive data it holds (e.g. donor, beneficiary, or "
            "financial information)?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID2",
        "question": (
            "Is the charity aware of who has access to sensitive data "
            "and systems, including staff and volunteers?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID3",
        "question": (
            "Does the charity have visibility over which systems or "
            "personal devices are used to access its data and accounts?"
        ),
        "scale": "0-4"
    },
    {
        "id": "ID4",
        "question": (
            "Is responsibility for managing cyber or data-related risk "
            "clearly understood within the charity, even if informally?"
        ),
        "scale": "0-4"
    }
    
]

# -------------------------
# PROTECT DOMAIN
# -------------------------
# This section assesses the safeguards in place to reduce the likelihood
# of a cyber incident occurring. The focus is on access control, staff
# awareness, data protection, and basic system security measures.

protect_questions = [
    {
        "id": "PR1",
        "question": (
            "Are user accounts and passwords managed in a consistent way "
            "for staff and volunteers who access charity systems?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR2",
        "question": (
            "Do staff and volunteers receive basic guidance or training "
            "on recognising phishing emails or suspicious messages?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR3",
        "question": (
            "Is sensitive charity data (such as donor or beneficiary data) "
            "stored securely, for example using passwords or restricted access?"
        ),
        "scale": "0-4"
    },
    {
        "id": "PR4",
        "question": (
            "Are devices and systems used by the charity kept up to date "
            "with software or security updates?"
        ),
        "scale": "0-4"
    }
]

# -------------------------
# DETECT DOMAIN
# -------------------------
# This section assesses how effectively the charity can notice
# unusual activity or potential cyber incidents.

detect_questions = [
    {
        "id": "DE1",
        "question": (
            "Would the charity be likely to notice unusual activity "
            "such as unexpected emails, account lockouts, or system errors?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE2",
        "question": (
            "Are there any basic checks in place to review account activity "
            "or system access when something seems wrong?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE3",
        "question": (
            "Is there a clear way for staff or volunteers to report "
            "suspected cyber issues or suspicious activity?"
        ),
        "scale": "0-4"
    },
    {
        "id": "DE4",
        "question": (
            "Does the charity use any tools or services (even basic ones) "
            "to monitor emails, accounts, or devices for security issues?"
        ),
        "scale": "0-4"
    }
]

# -------------------------
# RESPOND DOMAIN
# -------------------------
# This section evaluates how prepared the charity is to respond
# if a cyber incident is confirmed.

respond_questions = [
    {
        "id": "RS1",
        "question": (
            "Does the charity know what steps to take if a cyber incident "
            "such as phishing or data loss is confirmed?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS2",
        "question": (
            "Is there someone responsible for coordinating actions "
            "during a cyber incident, even informally?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS3",
        "question": (
            "Would the charity know who needs to be informed internally "
            "or externally if a cyber incident occurred?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RS4",
        "question": (
            "Are actions taken during a cyber incident recorded or "
            "documented in any way?"
        ),
        "scale": "0-4"
    }
]

# -------------------------
# RECOVER DOMAIN
# -------------------------
# This section assesses the charity’s ability to restore operations
# and learn from a cyber incident.

recover_questions = [
    {
        "id": "RC1",
        "question": (
            "Does the charity have backups of important data that could "
            "be used if systems or files were lost?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC2",
        "question": (
            "Would the charity be able to restore normal operations "
            "within a reasonable time after a cyber incident?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC3",
        "question": (
            "Is responsibility for recovery tasks clearly understood, "
            "even if there is no formal recovery plan?"
        ),
        "scale": "0-4"
    },
    {
        "id": "RC4",
        "question": (
            "After an incident, would the charity be likely to review "
            "what went wrong and make improvements?"
        ),
        "scale": "0-4"
    }
]

# questionnaire.py (at the bottom)

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

