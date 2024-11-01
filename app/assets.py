import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd

BASE_URL = "http://localhost:8000/api"

st.sidebar.title("Navigation")
with st.sidebar:
    selected = option_menu(
        "Insert Data",
        ["Employees", "Locations", "Asset Types", "Assets", "Brands", "Models", "Responsibilities", "Upload Excel", "Queries"],
        icons=["person-plus", "map", "clipboard-plus", "box", "tag", "puzzle", "briefcase", "file-earmark-excel", "search"],
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
                if response.status_code in [200, 201]: 
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
                if response.status_code in [200, 201]: 
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
    

    table_options = {
        "employees": {
            "Required": ["nombre", "documento"],
            "Optional": ["correo", "telefono"],
            "Mapping": {
                "nombre": "name",
                "documento": "document",
                "correo": "email",
                "telefono": "phone"
            }
        },
        "locations": {
            "Required": ["nombre"],
            "Optional": [],
            "Mapping": {"nombre": "name"}
        },
        "asset_types": {
            "Required": ["tipo"],
            "Optional": [],
            "Mapping": {"tipo": "type"}
        },
        "assets": {
            "Required": ["id_tipo", "id_ubicacion", "id_modelo"],
            "Optional": ["n_parte", "serial", "procesador", "disco_duro", "memoria_ram"],
            "Mapping": {
                "id_tipo": "type_id",
                "id_ubicacion": "location_id",
                "id_modelo": "model_id",
                "n_parte": "part_number",
                "serial": "serial",
                "procesador": "processor",
                "disco_duro": "hard_drive",
                "memoria_ram": "ram"
            }
        },
        "brands": {
            "Required": ["marca"],
            "Optional": [],
            "Mapping": {"marca": "brand"}
        },
        "models": {
            "Required": ["modelo", "id_marca"],
            "Optional": [],
            "Mapping": {
                "modelo": "model",
                "id_marca": "brand_id"
            }
        },
        "responsibilities": {
            "Required": ["id_activo", "id_funcionario", "fecha_asignacion"],
            "Optional": ["fecha_fin"],
            "Mapping": {
                "id_activo": "asset_id",
                "id_funcionario": "employee_id",
                "fecha_asignacion": "assignment_date",
                "fecha_fin": "end_date"
            }
        }
    }
    
    selected_table = st.selectbox(
        "Select target table:",
        options=list(table_options.keys()),
        format_func=lambda x: x.capitalize()
    )
    
    if selected_table:
        st.info(f"""
        Required columns: {', '.join(table_options[selected_table]['Required'])}
        Optional columns: {', '.join(table_options[selected_table]['Optional'])}
        """)
    
    uploaded_file = st.file_uploader("Choose Excel file", type="xlsx")

    if uploaded_file:
        
        df = pd.read_excel(uploaded_file)
        if 'telefono' in df.columns:
            df['telefono'] = df['telefono'].astype(str)
        
        st.write("Preview of uploaded data:")
        st.dataframe(df)
        
        if st.button("Upload Data"):
            df_columns = set(df.columns)
            required_columns = set(table_options[selected_table]['Required'])
            
            if not required_columns.issubset(df_columns):
                missing_cols = required_columns - df_columns
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.info(f"""
                Please ensure your Excel file has these column names in Spanish:
                Required: {', '.join(table_options[selected_table]['Required'])}
                Optional: {', '.join(table_options[selected_table]['Optional'])}
                """)
                return
            
            try:
                mapping = table_options[selected_table]['Mapping']
                df_mapped = df.rename(columns=mapping)
                records = df_mapped.to_dict('records')
                
                success_count = 0
                error_count = 0
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, record in enumerate(records):
                    record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
                    
                    try:
                        response = requests.post(f"{BASE_URL}/{selected_table}/", json=record)
                        if response.status_code in [200, 201]:
                            success_count += 1
                        else:
                            error_count += 1
                            st.error(f"Error in row {i+1}: {response.text}")
                    except requests.RequestException as e:
                        error_count += 1
                        st.error(f"Connection error in row {i+1}: {str(e)}")
                    
                    progress_bar.progress((i+1) / len(records))
                    status_text.text(f"Uploaded {i+1} rows, {success_count} successful, {error_count} errors")
                
                st.success(f"Data uploaded successfully to {selected_table}!")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

def show_queries():
    st.title("Asset Management Queries")
    
    queries = [
        "1. Total assets by type",
        "2. Assets currently assigned to employees",
        "3. Unassigned assets",
        "4. Assets by location",
        "5. Employee assignment history",
        "6. Assets by brand and model",
        "7. Expired assignments",
        "8. Assets by processor type",
        "9. Assets by RAM capacity",
        "10. Assets by hard drive capacity",
        "11. Employees with multiple assets",
        "12. Location with most assets",
        "13. Most common asset type",
        "14. Assets by assignment date",
        "15. Brand distribution analysis"
    ]
    
    selected_query = st.selectbox("Select a query:", queries)
    
    if st.button("Execute Query"):
        try:
            response = requests.get(f"{BASE_URL}/queries/{queries.index(selected_query) + 1}")
            if response.status_code == 200:
                data = response.json()
                st.write("Query Results:")
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.error(f"Error executing query: {response.text}")
        except requests.RequestException as e:
            st.error(f"Connection error: {str(e)}")

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
elif selected == "Queries":
    show_queries()
