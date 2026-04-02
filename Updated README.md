# Cyber Risk Assessment Tool for UK Charities

Final Year Project – Aisha Moussa  
University of Hertfordshire  

---

## Live Application
Streamlit App:  
[PASTE YOUR STREAMLIT LINK HERE]

---

## Source Code
GitHub Repository:  
[PASTE YOUR GITHUB LINK HERE]

---

## Project Overview
This project presents a lightweight cyber risk assessment tool designed for small UK charities operating with limited technical resources.

The tool adapts principles from:
- NIST Cybersecurity Framework (CSF)
- NIST SP 800-30 (Likelihood x Impact risk model)

It enables organisations to:
- assess cyber security control maturity
- estimate likelihood and impact of cyber incidents
- calculate an overall risk score
- identify weakest domains
- receive prioritised, actionable recommendations

The system is implemented in Python using Streamlit and designed to be accessible to non-technical users.

---

## How to Run Locally

1. Install Python 3.x  
2. Install dependencies:
   pip install -r requirements.txt  

3. Run the application:
   streamlit run app.py  

4. Run tests:
   pytest  

---

## Project Structure

- app.py – Streamlit interface  
- scoring.py – risk scoring engine  
- questionnaire.py – questionnaire structure  
- charity_profile.py – impact inputs  
- ux.py – UI styling  
- data_loader.py – JSON export  
- test file(s) – automated testing  

---

## Project Foundation (Aims and Objectives)

### Aims
1. To design and develop a lightweight, Python-based cyber risk assessment tool that helps UK charities identify and evaluate their exposure to cyber threats such as phishing and donor-data compromise.  
2. To strengthen technical and analytical understanding of risk assessment methodologies through implementation of the NIST Cybersecurity Framework and NIST SP 800-30 scoring logic.

### Objectives
1. Conduct comparative research on cybersecurity frameworks (NIST CSF, ISO 27005, CIS Controls, NCSC guidance) and development approaches.  
2. Design a non-technical risk-assessment questionnaire structured around NIST CSF domains.  
3. Implement the questionnaire and scoring model using Python and Streamlit.  
4. Test the tool using synthetic charity profiles to evaluate reliability and consistency.  
5. Document and critically evaluate findings and recommendations for future work.

### Targets
1. Delivery of a framework and tool comparison  
2. Completion of a structured NIST-based questionnaire  
3. Functional Streamlit application generating risk outputs  
4. Validation using synthetic charity datasets  
5. Documented evaluation and future recommendations  

---

## Notes
This is a prototype system developed for academic purposes.  
It is not intended as a formal compliance or certification tool.

The outputs are indicative and depend on self-reported input.
