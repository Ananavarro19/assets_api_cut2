
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd

BASE_URL = "http://localhost:8000/api"

st.sidebar.title("Navigation")
with st.sidebar:
    selected = option_menu(
        "Insert Data",
        ["Employees", "Locations", "Asset Types", "Assets", "Brands", "Models", "Responsibilities", "Upload Excel"],
        icons=["person-plus", "map", "clipboard-plus", "box", "tag", "puzzle", "briefcase", "file-earmark-excel"],
        menu_icon="cast",
        default_index=0
    )

def create_employee():
    st.title("Register Employee")
    with st.form(key="employee_form"):
        name = st.text_input("Employee Name")
        document = st.text_input("Document")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submit_button = st.form_submit_button(label="Register Employee")
        if submit_button:
            employee_data = {
                "name": name,
                "document": document,
                "email": email,
                "phone": phone
            }
            try:
                response = requests.post(f"{BASE_URL}/employees/", json=employee_data)
                if response.status_code == 200:
                    st.success("Employee registered successfully!")
                else:
                    st.error(f"Error registering employee: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_location():
    st.title("Register Location")
    with st.form(key="location_form"):
        name = st.text_input("Location Name")
        submit_button = st.form_submit_button(label="Register Location")
        if submit_button:
            location_data = {"name": name}
            try:
                response = requests.post(f"{BASE_URL}/locations/", json=location_data)
                if response.status_code == 200:
                    st.success("Location registered successfully!")
                else:
                    st.error(f"Error registering location: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_asset_type():
    st.title("Register Asset Type")
    with st.form(key="asset_type_form"):
        type_name = st.text_input("Asset Type")
        submit_button = st.form_submit_button(label="Register Asset Type")
        if submit_button:
            asset_type_data = {"type": type_name}
            try:
                response = requests.post(f"{BASE_URL}/asset_types/", json=asset_type_data)
                if response.status_code == 200:
                    st.success("Asset Type registered successfully!")
                else:
                    st.error(f"Error registering asset type: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_asset():
    st.title("Register Asset")
    with st.form(key="asset_form"):
        asset_id = st.number_input("Asset ID", min_value=1)
        type_id = st.number_input("Type ID", min_value=1)
        location_id = st.number_input("Location ID", min_value=1)
        model_id = st.number_input("Model ID", min_value=1)
        part_number = st.text_input("Part Number")
        serial = st.text_input("Serial")
        processor = st.text_input("Processor")
        hard_drive = st.text_input("Hard Drive")
        ram = st.text_input("RAM")
        submit_button = st.form_submit_button(label="Register Asset")
        if submit_button:
            asset_data = {
                "asset_id": asset_id,
                "type_id": type_id,
                "location_id": location_id,
                "model_id": model_id,
                "part_number": part_number,
                "serial": serial,
                "processor": processor,
                "hard_drive": hard_drive,
                "ram": ram
            }
            try:
                response = requests.post(f"{BASE_URL}/assets/", json=asset_data)
                if response.status_code == 200:
                    st.success("Asset registered successfully!")
                else:
                    st.error(f"Error registering asset: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_brand():
    st.title("Register Brand")
    with st.form(key="brand_form"):
        brand_name = st.text_input("Brand Name")
        submit_button = st.form_submit_button(label="Register Brand")
        if submit_button:
            brand_data = {"brand": brand_name}
            try:
                response = requests.post(f"{BASE_URL}/brands/", json=brand_data)
                if response.status_code == 200:
                    st.success("Brand registered successfully!")
                else:
                    st.error(f"Error registering brand: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_model():
    st.title("Register Model")
    with st.form(key="model_form"):
        model_name = st.text_input("Model Name")
        brand_id = st.number_input("Brand ID", min_value=1)
        submit_button = st.form_submit_button(label="Register Model")
        if submit_button:
            model_data = {
                "model": model_name,
                "brand_id": brand_id
            }
            try:
                response = requests.post(f"{BASE_URL}/models/", json=model_data)
                if response.status_code == 200:
                    st.success("Model registered successfully!")
                else:
                    st.error(f"Error registering model: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def create_responsibility():
    st.title("Register Responsibility")
    with st.form(key="responsibility_form"):
        asset_id = st.number_input("Asset ID", min_value=1)
        employee_id = st.number_input("Employee ID", min_value=1)
        assignment_date = st.date_input("Assignment Date")
        end_date = st.date_input("End Date", value=None)
        submit_button = st.form_submit_button(label="Register Responsibility")
        if submit_button:
            responsibility_data = {
                "asset_id": asset_id,
                "employee_id": employee_id,
                "assignment_date": str(assignment_date),
                "end_date": str(end_date) if end_date else None
            }
            try:
                response = requests.post(f"{BASE_URL}/responsibilities/", json=responsibility_data)
                if response.status_code == 200:
                    st.success("Responsibility registered successfully!")
                else:
                    st.error(f"Error registering responsibility: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def upload_excel():
    st.title("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Excel File Content:")
        st.dataframe(df)
        table_options = ["employees", "locations", "asset_types", "assets", "brands", "models", "responsibilities"]
        selected_table = st.selectbox("Select the table to insert data:", table_options)
        if st.button("Upload Data"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{BASE_URL}/upload-excel/?table={selected_table}", files=files)
            if response.status_code == 200:
                st.success("Data uploaded successfully!")
            else:
                st.error(f"Error uploading data: {response.text}")

def validate_dataframe(df, table_name):
    if table_name == "employees":
        return set(df.columns) == {"name", "document", "email", "phone"}
    elif table_name == "locations":
        return set(df.columns) == {"name"}
    elif table_name == "asset_types":
        return set(df.columns) == {"type"}
    elif table_name == "assets":
        return set(df.columns) == {"asset_id", "type_id", "location_id", "model_id", "part_number", "serial", "processor", "hard_drive", "ram"}
    elif table_name == "brands":
        return set(df.columns) == {"brand"}
    elif table_name == "models":
        return set(df.columns) == {"model", "brand_id"}
    elif table_name == "responsibilities":
        return set(df.columns) == {"asset_id", "employee_id", "assignment_date", "end_date"}
    return False

if selected == "Employees":
    create_employee()
elif selected == "Locations":
    create_location()
elif selected == "Asset Types":
    create_asset_type()
elif selected == "Assets":
    create_asset()
elif selected == "Brands":
    create_brand()
elif selected == "Models":
    create_model()
elif selected == "Responsibilities":
    create_responsibility()
elif selected == "Upload Excel":
    upload_excel()
