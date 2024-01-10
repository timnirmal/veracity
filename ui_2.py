from openai import OpenAI
import streamlit as st
import io

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": "Welcome to the chat!"})

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Initialize extracted_text as an empty string
extracted_text = ""

# Use st.form to add the file upload button
with st.form(key="file_upload_form"):
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
    submit_button = st.form_submit_button(label="Submit")

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Process the uploaded PDF file and extract text
        pdf_bytes = uploaded_file.read()
        extracted_text = extract_text_from_pdf(pdf_bytes)

        # Save the extracted text to a text file
        text_file_path = "extracted_text.txt"
        with open(text_file_path, "w") as text_file:
            text_file.write(extracted_text)

        st.write(f"Uploaded file contents: {text_file_path}")

    else:
        st.write("Unsupported file format. Please upload a PDF file.")

# Check if there's extracted text available
if extracted_text:
    # Allow the user to send a query to ChatGPT
    query = st.text_input("Ask a question:")
    if query:
        # Send the user's question to ChatGPT
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Send the extracted text as context to ChatGPT
        st.session_state.messages.append({"role": "system", "content": extracted_text})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def extract_text_from_pdf(pdf_bytes):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage

    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    pdf_file = io.BytesIO(pdf_bytes)
    for page in PDFPage.get_pages(pdf_file):
        page_interpreter.process_page(page)

    extracted_text = fake_file_handle.getvalue()

    return extracted_text
