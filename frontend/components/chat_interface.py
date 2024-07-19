import streamlit as st
import requests

def chat_interface_component():
    st.header("Ask Your Data")
    user_query = st.text_input("Ask about your data...", key="chat_input")
    if st.button("Submit", key="chat_button"):
        response = requests.post("http://localhost:8000/query", json={"query": user_query})
        if response.status_code == 200:
            result = response.json()
            st.write(result)  # Print the entire response for debugging
            if result["status"] == "success":
                if "answer" in result:
                    st.write(result["answer"])
                if "code" in result:
                    st.code(result["code"])
                if "result" in result:
                    st.write("Result:")
                    st.write(result["result"])
            else:
                st.error(result.get("message", "Failed to process query"))
        else:
            st.error("Failed to process query")

