''' Answer Mapping and Data Preparation
This module contains the logic that transforms human-readable responses (e.g., “Yes”, “Partially”, “No”) into numerical or categorical values used by the scoring engine. 
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