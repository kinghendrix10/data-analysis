import streamlit as st
import requests
from components.data_visualization import data_visualization_component

def chat_interface_component():
    st.header("Chat Interface")
    st.subheader("Ask Your Data")

    if st.session_state["uploaded_file"] is None:
        st.write("Please upload a file to begin.")

    user_query = st.text_input("Ask about your data...", key="chat_input", help="Ask any question about your data")

    if st.button("Submit", key="chat_button"):
        if not user_query:
            st.warning("Please enter a query.")
            return

        if st.session_state["uploaded_file"] is None:
            st.warning("Please upload a file first.")
            return

        response = requests.post("http://localhost:8000/query", json={"query": user_query})
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                if "answer" in result:
                    st.write(result["answer"])
                if "code" in result:
                    st.code(result["code"])
                if "result" in result:
                    st.write("Result:")
                    st.write(result["result"])
                if "visualization_data" in result:
                    st.write("Visualization:")
                    data_visualization_component(result["visualization_data"])
            else:
                st.error(result.get("message", "Failed to process query"))
        else:
            st.error("Failed to process query")
