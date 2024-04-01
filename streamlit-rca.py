import streamlit as st
from PIL import Image
import openai
import os
import base64 # Import base64 module

# Set up OpenAI API key
openai.api_type = "azure"
openai.api_base = "https://coe-openai-instance.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "d079f278137e44a8812fc39fe85449eb"
                 
st.set_page_config(page_title="SAP SuccessFactors Customer Office", page_icon="301103_da_blue.png", layout='wide')

# Load SAP SuccessFactors Logo
logo_filename = "SFSF-CO-Logo.png"
logo_path = os.path.join(os.getcwd(), logo_filename)

def image_to_base64(image_path):
    if not os.path.exists(image_path):
       st.error(f"Image file '{image_path}' not found.")
       return None
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded_image = base64.b64encode(image_data).decode()
        return base64_encoded_image
 

@st.cache_data
def analyze_summary(input_summary):
    prompt = f"Provide a high-level summary of the following SAP system summary report that is anonymized for customer consumption in a concise single paragraph following the above rules:\n{input_summary}\n"
    response = openai.ChatCompletion.create(
        engine="coe-gpt-4-32k",
        messages=[
            {"role": "system", "content": "Rules: \n"},
            {"role": "system", "content": """
                Generate a 3-sentence customer-facing post-incident summary of a cloud service incident. Sentence 1 should begin with [SAP technical teams investigated and observed that…]. Sentence 2 should begin with [The teams identified an issue with...]. Sentence 3 should begin with [The issue was resolved by…]. Do not include any timestamps or service names. Use the following information as an incident log to compile the summary:\n
                When analyzing the summary, follow these rules:\n
                1. Remove any reference to personal names. Replace with roles when possible to summarize.\n
                2. Replace any software product names with the it's function.\n
                3. Replace acronyms where possible with the actual description when first referenced\n
                4. Protect the SAP Brand when describing the incident summary.\n
                5. Write the summary for a non-technical customer audience.\n
            """
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return str(response.choices[0].message.content)

@st.cache_data
def analyze_rca(input_summary):
    prompt = f"Provide a high-level summary of the following SAP system incident probable root cause report that is anonymized for customer consumption in a concise single paragraph following the above rules:\n{input_summary}\n"
    response = openai.ChatCompletion.create(
        engine="coe-gpt-4-32k",
        messages=[
            {"role": "system", "content": "Rules: \n"},
            {"role": "system", "content": """
                When analyzing the summary, follow these rules:\n
                1. Remove any reference to personal names. Replace with roles when possible to summarize.\n
                2. Replace any software product names with the it's function.\n
                3. Replace acronyms where possible with the actual description when first referenced\n
                4. Protect the SAP Brand when describing the incident summary.\n
                5. Write the summary for a non-technical customer audience.\n
            """
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return str(response.choices[0].message.content)


# Convert logo image to base64
 
logo_base64 = image_to_base64(logo_path)
if logo_base64:
    # Markdown code to display the logo image in the upper right corner
    logo_html = f'<div style="position: absolute; top: 0; left: 0;"><img src="data:image/png;base64,{logo_base64}"></div>'
    st.markdown(logo_html, unsafe_allow_html=True)
else:
    st.error("Failed to load logo image.")

st.write("\n\n\n\n\n\n")
st.title("&nbsp;")
st.subheader("\nPost-Incident Communication Enhancement with AI")

impact = st.text_area("**Incident Impact:**")
summary = st.text_area("**Incident Summary:**")
root_cause = st.text_area("**Probable Root Cause:**")

if st.button("Submit"):
    impact_result = analyze_summary(impact)
    summary_result = analyze_summary(summary)
    root_cause_result = analyze_rca(root_cause)
    
    st.write("**Incident Impact:**")
    st.write(impact_result)

    st.write("**Incident Summary:**")
    st.write(summary_result)

    st.write("**Probable Root Cause:**")
    st.write(root_cause_result)

    #kbc st.write("Content copied to clipboard!")
