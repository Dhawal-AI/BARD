import streamlit as st
import pandas as pd
from bardapi import Bard
import hashlib
# Initialize Bard API
bard_token = 'Xwj5sVDzqYsdp-biewkbpM26kz7DmFI1KENySgrFflnFoGaD3SnrP6EMvUYTYOpuWI4qkw.'
bard = Bard(token=bard_token,proxies={'http':'http://127.0.0.1:1080', 'https':'http://0.0.0.0:1080'}, timeout=10)
PASSWORD_HASH = "c0a16a726686f7c44f99536443e6b942ba4cd80e5bd81a739ab63698a4368302"
# Generate program based on PICOS criteria, title, and abstract
def generate_program(picos_criteria, title, abstract):
    return f"Given the PICOS criteria: {picos_criteria}\n\nTitle: {title}\nAbstract: {abstract}"

# Streamlit app
def main():
    st.image(
    'Eversana_Logo_H_RGB.png',
    width=500,
)
    
    CURRENT_THEME = "blue"
    IS_DARK_THEME = True
    # Check if the user is authorized to access the app
    if not check_credentials():
        return
    st.title("Systematic Literature Reviewer")
    st.write("Upload a CSV file to perform the systematic literature review.")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='latin-1', on_bad_lines='skip')

        # User input for PICOS criteria
        st.subheader("PICOS Criteria")
        # Convert PICOS criteria input to a list
        picos_input = st.text_input("Enter PICOS criteria (comma-separated)", "")
        picos_criteria = [c.strip() for c in picos_input.split(",")]

        # User input for number of rows to process
        num_rows = st.number_input("Number of Rows to Process", min_value=1, max_value=len(df), value=2, step=1)

        # Button to trigger result generation
        if st.button("Generate Results"):
            df_subset = df.head(num_rows)
            df_subset['resultsbard'] = ''

            # Perform literature review for each row in the DataFrame subset
            progress_bar = st.progress(0)
            progress_text = st.empty()

            for i, row in df_subset.iterrows():
                title = row['Title']
                abstract = row['Abstract']
                message='''act as an automatic Systematic literature reviewer, I will give you a picos criteria and based on that you have to accept or reject a study based on its title and abstract,be strict with picos,
'''+str(generate_program(picos_criteria,df['Title'][i],df['Abstract'][i]))+"Keep your answer concise upto 250 words"
                response = bard.get_answer(message)
                result = response['content']
                df_subset.at[i, 'resultsbard'] = result

                # Update progress bar and text
                progress = (i + 1) / num_rows
                progress_bar.progress(progress)
                progress_text.text(f"Progress: {int(progress * 100)}%")

            # Display results
            st.write("Results:")
            st.dataframe(df_subset)

            # Option to download results as CSV
            if st.button('Save Predictions'):
                save_to_csv(df)
            
def save_to_csv(df):
    # Save the DataFrame to a CSV file in the "Downloads" directory
    st.download_button(
        label="Download Predictions CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='predictions.csv',
        mime='text/csv'
    )
def check_credentials():
    password = st.sidebar.text_input("Enter password", value="", type="password")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != PASSWORD_HASH:
        st.sidebar.error("Invalid password. Access denied.")
        return False
    return True
if __name__ == "__main__":
    main()
