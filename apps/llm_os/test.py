import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    'DocID': [1, 2, 3],
    'Title': ['Document A', 'Document B', 'Document C'],
    'PostDate': ['2021-06-01', '2021-06-02', '2021-06-03']
}
df = pd.DataFrame(data)

def main():
    st.title('Interactive HTML Table with Embedded Actions in Streamlit')

    # Function to display HTML table with buttons that modify query parameters
    def display_html_table():
        html_content = "<table style='width:100%; border-collapse: collapse;'>"
        html_content += "<tr style='background-color: #f1f1f1;'>"
        html_content += "".join([f"<th style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{col}</th>" for col in df.columns])
        html_content += "<th>Action</th></tr>"

        for _, row in df.iterrows():
            html_content += f"<tr>"
            for col in df.columns:
                html_content += f"<td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{row[col]}</td>"
            # Each button sets the doc_id parameter in the query string
            html_content += f"<td><button onclick='window.location.href = \"?doc_id={row['DocID']}\"'>Analyze</button></td>"
            html_content += "</tr>"
        html_content += "</table>"
        st.markdown(html_content, unsafe_allow_html=True)

    display_html_table()

    # Check if a doc_id is present in the query parameters and process it
    if 'doc_id' in st.query_params:
        doc_id = st.query_params['doc_id'][0]  # Get the first (or only) doc_id value
        st.write(f"Processing document with DocID: {doc_id}")
        # Here you can add your processing function or any action

if __name__ == "__main__":
    main()
