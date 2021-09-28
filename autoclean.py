import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
st.title('Auto_clean your csv file for data exploration')


# @st.cache(allow_output_mutation=True)
def load_data(file):
    df = pd.read_csv(file)
    return df


@st.cache
# IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(file):
    return file.to_csv().encode('utf-8')


upload_file = st.file_uploader("Upload a file", type=("csv"))
if upload_file is not None:
    df1 = load_data(upload_file)
    is_check = st.checkbox("View Full data")
    if is_check:
        st.dataframe(df1)
    total_records = df1.shape[0]*df1.shape[1]
    df1_shape = df1.shape
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Total Records :", df1.shape[0]*df1.shape[1])
    with col2:
        st.write("Shape of Data :", df1_shape)
    with col3:
        st.write("No. of Duplicated Rows :", df1.duplicated().sum())
    with col4:
        st.write("Missing Rows:", df1.isnull().sum().sum())

    is_duplicated = df1.duplicated().sum()
    if is_duplicated > 0:
        is_extract_duplciate = st.checkbox("Extract duplicate rows")
        if is_extract_duplciate:
            st.write("Duplcaited Rows")
            st.dataframe(df1.loc[df1.duplicated(), :])
            is_radio = st.radio("Which Duplciate to Delete",
                                ("First", "Last", "Keep Duplicates", "Drop All", "Custom Columns to drop"))

            if st.button("Submit"):

                if is_radio == "First":
                    st.write("Total records before removing Duplciates: ",
                             total_records)
                    df1_new = df1.drop_duplicates(inplace=True)
                    st.write("Removed", df1_new.shape)
                    df1_total_records = df1_new.shape[0]*df1_new.shape[1]
                    st.write("Total records after removing Duplciates::",
                             df1_total_records)

                if is_radio == "Last":
                    st.write("Total records before removing Duplciates: ",
                             total_records)
                    df1_new = df1.drop_duplicates(keep='last', inplace=True)
                    st.write("Removed")
                    df1_total_records = df1_new.shape[0]*df1_new.shape[1]
                    st.write("Total records after removing Duplciates::",
                             df1_total_records)

                if is_radio == "Keep Duplicates":
                    df1_new = df1.copy(deep=True)
                    df1_total_records = df1_new.shape[0]*df1_new.shape[1]
                    st.write("No Data is removed, total records: ",
                             df1_total_records)

                if is_radio == "Drop All":
                    st.write("Total records before removing Duplciates: ",
                             total_records)
                    df1_new = df1.drop_duplicates(keep=False, inplace=True)
                    st.write("Removed")
                    df1_total_records = df1_new.shape[0]*df1_new.shape[1]
                    st.write("Total records after removing Duplciates::",
                             df1_total_records)

                csv = convert_df(df1_new)
                st.download_button(
                    label="Download revised file as CSV",
                    data=csv,
                    file_name='df1_new.csv',
                    mime='text/csv'
                )
