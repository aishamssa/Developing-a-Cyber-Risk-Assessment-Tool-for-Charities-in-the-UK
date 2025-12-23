# Main Application Controller
# This is the central script that coordinates the overall functioning of the tool. 
# It does not contain business logic itself; instead, it acts as the entry point that imports and calls functions from the other modules. 
# In the final version, this script will handle user interaction via a Streamlit interface, enabling the charity to answer the questionnaire and receive a risk score. 
# During the early stages, it simply loads data, calls the scoring functions, and prints results to the console. 
# The purpose of this script is to ensure that the system follows a clear separation between interface logic and computational logic, which improves maintainability and aligns with good software-engineering practice.
