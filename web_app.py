import streamlit as st
import requests
from requests.exceptions import RequestException

# Configure page
st.set_page_config(
    page_title="Cervical Cancer Risk Assessment",
    layout="wide",
    page_icon="🩺"
)
st.title("🩺 Cervical Cancer Risk Prediction")

# Constants
API_URL = "https://cervical-cancer-classifier-8q4n.onrender.com/predict"
RISK_CATEGORIES = {
    "Very low": (0, 20),
    "Low": (20, 40),
    "Moderate": (40, 60),
    "High": (60, 80),
    "Very high": (80, 100)
}

def get_risk_category(probability):
    """Categorize risk based on probability percentage"""
    for category, (lower, upper) in RISK_CATEGORIES.items():
        if lower <= probability < upper:
            return category
    return "Very high" if probability >= 100 else "Very low"

def display_recommendations(risk_level):
    """Display recommendations based on risk level"""
    if risk_level in ["High", "Very high"]:
        st.error("🚨 High Risk of Cervical Cancer")
        st.markdown("""
        **Recommendations:**
        - Immediate consultation with gynecologist recommended
        - Schedule follow-up diagnostic tests
        - Review risk factors and prevention strategies
        """)
    else:
        st.success("✅ Low Risk of Cervical Cancer")
        st.markdown("""
        **Recommendations:**
        - Continue regular screenings as recommended
        - Maintain healthy lifestyle practices
        - Annual check-ups advised
        """)

# Input form
with st.form("patient_form"):
    st.header("Patient Information")
    
    # Section 1: Demographics
    c1, c2, c3 = st.columns(3)
    with c1:
        Age = st.number_input("Age", min_value=15, max_value=100, value=30)
    with c2:
        Number_of_sexual_partners = st.number_input("Number of sexual partners", min_value=0, value=1)
    with c3:
        First_sexual_intercourse = st.number_input("Age at first sexual intercourse", 
                                                 min_value=10, max_value=50, value=18)
    
    # Section 2: Pregnancy & Contraception
    st.subheader("Pregnancy & Contraception")
    c1, c2, c3 = st.columns(3)
    with c1:
        Num_of_pregnancies = st.number_input("Number of pregnancies", min_value=0, value=0)
    with c2:
        Hormonal_Contraceptives = st.radio("Hormonal Contraceptives", [0, 1], 
                                          format_func=lambda x: "No" if x == 0 else "Yes")
    with c3:
        Hormonal_Contraceptives_years = st.number_input("Years of hormonal contraceptives use", 
                                                      min_value=0.0, value=0.0, step=0.1)
    
    # Section 3: IUD
    c1, c2 = st.columns(2)
    with c1:
        IUD = st.radio("IUD Use", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    with c2:
        IUD_years = st.number_input("Years of IUD use", min_value=0.0, value=0.0, step=0.1)
    
    # Section 4: Smoking
    st.subheader("Smoking History")
    c1, c2, c3 = st.columns(3)
    with c1:
        Smokes = st.radio("Smoker", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    with c2:
        Smokes_years = st.number_input("Years smoked", min_value=0, value=0)
    with c3:
        Smokes_packs_year = st.number_input("Packs per year", min_value=0.0, value=0.0, step=0.1)
    
    # Section 5: STDs
    st.subheader("STD History")
    c1, c2 = st.columns(2)
    with c1:
        STDs = st.radio("History of STDs", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    with c2:
        STDs_number = st.number_input("Number of STD diagnoses", min_value=0, value=0)
    
    # Specific STD conditions
    st.markdown("**Specific STD Conditions**")
    cols = st.columns(4)
    std_conditions = [
        ('STDs_vaginal_condylomatosis', 'Vaginal Condylomatosis'),
        ('STDs_vulvo_perineal_condylomatosis', 'Vulvo-Perineal Condylomatosis'),
        ('STDs_syphilis', 'Syphilis'),
        ('STDs_pelvic_inflammatory_disease', 'Pelvic Inflammatory Disease'),
        ('STDs_genital_herpes', 'Genital Herpes'),
        ('STDs_molluscum_contagiosum', 'Molluscum Contagiosum'),
        ('STDs_HIV', 'HIV'),
        ('STDs_Hepatitis_B', 'Hepatitis B'),
        ('STDs_HPV', 'HPV')
    ]
    
    for i, (var_name, label) in enumerate(std_conditions):
        with cols[i % 4]:
            globals()[var_name] = st.radio(label, [0, 1], 
                                         format_func=lambda x: "No" if x == 0 else "Yes",
                                         horizontal=True)
    
    # Section 6: Diagnostics
    st.subheader("Diagnostic Results")
    c1, c2, c3 = st.columns(3)
    with c1:
        STDs_Number_of_diagnosis = st.number_input("Total STD diagnoses", min_value=0, value=0)
    with c2:
        Dx_Cancer = st.radio("Cancer Diagnosis", [0, 1], 
                           format_func=lambda x: "No" if x == 0 else "Yes",
                           horizontal=True)
    with c3:
        Dx_CIN = st.radio("CIN Diagnosis", [0, 1], 
                         format_func=lambda x: "No" if x == 0 else "Yes",
                         horizontal=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        Dx_HPV = st.radio("HPV Diagnosis", [0, 1], 
                         format_func=lambda x: "No" if x == 0 else "Yes",
                         horizontal=True)
    with c2:
        Dx = st.radio("General Diagnosis", [0, 1], 
                     format_func=lambda x: "No" if x == 0 else "Yes",
                     horizontal=True)
    with c3:
        Hinselmann = st.radio("Hinselmann Test", [0, 1], 
                            format_func=lambda x: "Negative" if x == 0 else "Positive",
                            horizontal=True)
    
    c1, c2 = st.columns(2)
    with c1:
        Schiller = st.radio("Schiller Test", [0, 1], 
                          format_func=lambda x: "Negative" if x == 0 else "Positive",
                          horizontal=True)
    with c2:
        Citology = st.radio("Cytology Test", [0, 1], 
                          format_func=lambda x: "Negative" if x == 0 else "Positive",
                          horizontal=True)
    
    submitted = st.form_submit_button("Predict Risk")

# Handle form submission
if submitted:
    patient_data = {
        "Age": float(Age),
        "Number_of_sexual_partners": float(Number_of_sexual_partners),
        "First_sexual_intercourse": float(First_sexual_intercourse),
        "Num_of_pregnancies": float(Num_of_pregnancies),
        "Smokes": float(Smokes),
        "Smokes_years": float(Smokes_years),
        "Smokes_packs_year": float(Smokes_packs_year),
        "Hormonal_Contraceptives": float(Hormonal_Contraceptives),
        "Hormonal_Contraceptives_years": float(Hormonal_Contraceptives_years),
        "IUD": float(IUD),
        "IUD_years": float(IUD_years),
        "STDs": float(STDs),
        "STDs_number": float(STDs_number),
        "STDs_vaginal_condylomatosis": float(STDs_vaginal_condylomatosis),
        "STDs_vulvo_perineal_condylomatosis": float(STDs_vulvo_perineal_condylomatosis),
        "STDs_syphilis": float(STDs_syphilis),
        "STDs_pelvic_inflammatory_disease": float(STDs_pelvic_inflammatory_disease),
        "STDs_genital_herpes": float(STDs_genital_herpes),
        "STDs_molluscum_contagiosum": float(STDs_molluscum_contagiosum),
        "STDs_HIV": float(STDs_HIV),
        "STDs_Hepatitis_B": float(STDs_Hepatitis_B),
        "STDs_HPV": float(STDs_HPV),
        "STDs_Number_of_diagnosis": float(STDs_Number_of_diagnosis),
        "Dx_Cancer": float(Dx_Cancer),
        "Dx_CIN": float(Dx_CIN),
        "Dx_HPV": float(Dx_HPV),
        "Dx": float(Dx),
        "Hinselmann": float(Hinselmann),
        "Schiller": float(Schiller),
        "Citology": float(Citology)
    }
    
    try:
        with st.spinner("Calculating risk..."):
            response = requests.post(
                API_URL,
                json=patient_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
        
        # Display results
        st.subheader("Risk Assessment Results")
        
        # Create columns for metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Probability", f"{result.get('probability_percent', 0):.1f}%")
        
        with col2:
            risk_category = get_risk_category(result.get('probability_percent', 0))
            st.metric("Risk Category", risk_category)
        
        # Visual indicator
        st.progress(result.get('probability_percent', 0) / 100)
        
        # Display recommendations
        display_recommendations(risk_category)
        
        # Show detailed interpretation if available
        if 'interpretation' in result:
            st.info(f"**Interpretation:** {result['interpretation']}")
            
    except RequestException as e:
        st.error("🔴 Connection Error: Could not reach the prediction service")
        st.info("Please ensure:")
        st.info("1. The prediction API server is running")
        st.info("2. You're using the correct API URL")
        st.info(f"Technical details: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("""
**Note:** This tool is for professional use only. Always verify results with clinical assessment.
The predictions are based on statistical models and should not replace medical judgment.

""")
