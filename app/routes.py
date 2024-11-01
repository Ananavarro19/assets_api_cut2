# app/routes.py
from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.models import (
    EmployeeCreate, LocationCreate, AssetTypeCreate, AssetCreate,
    BrandCreate, ModelCreate, ResponsibilityCreate
)
from fastapi.responses import JSONResponse
from typing import List
from fastapi import Query

router = APIRouter()

@router.post("/employees/")
def create_employee(employee: EmployeeCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO funcionarios (nombre, documento, correo, telefono) VALUES (%s, %s, %s, %s)", 
                   (employee.name, employee.document, employee.email, employee.phone))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Employee created"})

@router.post("/locations/")
def create_location(location: LocationCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ubicaciones (nombre) VALUES (%s)", (location.name,))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Location created"})

@router.post("/asset_types/")
def create_asset_type(asset_type: AssetTypeCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tipos_activo (tipo) VALUES (%s)", (asset_type.type,))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Asset type created"})

@router.post("/assets/")
def create_asset(asset: AssetCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO activos (id_tipo, id_ubicacion, id_modelo, n_parte, serial, 
           procesador, disco_duro, memoria_ram)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                   (asset.type_id, asset.location_id, asset.model_id,
                    asset.part_number, asset.serial, asset.processor,
                    asset.hard_drive, asset.ram))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Asset created"})

@router.post("/brands/")
def create_brand(brand: BrandCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO marcas (marca) VALUES (%s)", (brand.brand,))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Brand created"})

@router.post("/models/")
def create_model(model: ModelCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO modelos (modelo, id_marca) VALUES (%s, %s)", (model.model, model.brand_id))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Model created"})

@router.post("/responsibilities/")
def create_responsibility(responsibility: ResponsibilityCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO responsabilidades (id_activo, id_funcionario, fecha_asignacion, fecha_fin) VALUES (%s, %s, %s, %s)", 
                   (responsibility.asset_id, responsibility.employee_id, responsibility.assignment_date, responsibility.end_date))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={"message": "Responsibility created"})

@router.get("/queries/{query_id}")
def execute_query(query_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    queries = {
        1: """
            SELECT ta.tipo, COUNT(a.id_activo) as total
            FROM tipos_activo ta
            LEFT JOIN activos a ON ta.id_tipo = a.id_tipo
            GROUP BY ta.tipo
            ORDER BY total DESC
        """,
        2: """
            SELECT f.nombre as employee, a.serial, ta.tipo as asset_type
            FROM responsabilidades r
            JOIN funcionarios f ON r.id_funcionario = f.id_funcionario
            JOIN activos a ON r.id_activo = a.id_activo
            JOIN tipos_activo ta ON a.id_tipo = ta.id_tipo
            WHERE r.fecha_fin IS NULL
        """,
        3: """
            SELECT a.serial, ta.tipo, m.modelo
            FROM activos a
            LEFT JOIN responsabilidades r ON a.id_activo = r.id_activo
            JOIN tipos_activo ta ON a.id_tipo = ta.id_tipo
            JOIN modelos m ON a.id_modelo = m.id_modelo
            WHERE r.id_responsabilidad IS NULL
        """,
        4: """
            SELECT u.nombre as location, COUNT(a.id_activo) as total
            FROM ubicaciones u
            LEFT JOIN activos a ON u.id_ubicacion = a.id_ubicacion
            GROUP BY u.nombre
        """,
        5: """
            SELECT f.nombre as employee, a.serial, r.fecha_asignacion, r.fecha_fin
            FROM responsabilidades r
            JOIN funcionarios f ON r.id_funcionario = f.id_funcionario
            JOIN activos a ON r.id_activo = a.id_activo
            ORDER BY f.nombre, r.fecha_asignacion
        """,
        6: """
            SELECT mar.marca, m.modelo, COUNT(a.id_activo) as total
            FROM marcas mar
            JOIN modelos m ON mar.id_marca = m.id_marca
            LEFT JOIN activos a ON m.id_modelo = a.id_modelo
            GROUP BY mar.marca, m.modelo
        """,
        7: """
            SELECT f.nombre, a.serial, r.fecha_fin
            FROM responsabilidades r
            JOIN funcionarios f ON r.id_funcionario = f.id_funcionario
            JOIN activos a ON r.id_activo = a.id_activo
            WHERE r.fecha_fin < CURDATE()
        """,
        8: """
            SELECT procesador, COUNT(*) as total
            FROM activos
            WHERE procesador IS NOT NULL
            GROUP BY procesador
        """,
        9: """
            SELECT memoria_ram, COUNT(*) as total
            FROM activos
            WHERE memoria_ram IS NOT NULL
            GROUP BY memoria_ram
        """,
        10: """
            SELECT disco_duro, COUNT(*) as total
            FROM activos
            WHERE disco_duro IS NOT NULL
            GROUP BY disco_duro
        """,
        11: """
            SELECT f.nombre, COUNT(r.id_activo) as total_assets
            FROM funcionarios f
            JOIN responsabilidades r ON f.id_funcionario = r.id_funcionario
            WHERE r.fecha_fin IS NULL
            GROUP BY f.nombre
            HAVING total_assets > 1
        """,
        12: """
            SELECT u.nombre, COUNT(a.id_activo) as total
            FROM ubicaciones u
            LEFT JOIN activos a ON u.id_ubicacion = a.id_ubicacion
            GROUP BY u.nombre
            ORDER BY total DESC
            LIMIT 1
        """,
        13: """
            SELECT ta.tipo, COUNT(a.id_activo) as total
            FROM tipos_activo ta
            LEFT JOIN activos a ON ta.id_tipo = a.id_tipo
            GROUP BY ta.tipo
            ORDER BY total DESC
            LIMIT 1
        """,
        14: """
            SELECT DATE_FORMAT(r.fecha_asignacion, '%Y-%m') as month,
                   COUNT(*) as total_assignments
            FROM responsabilidades r
            GROUP BY month
            ORDER BY month
        """,
        15: """
            SELECT mar.marca, COUNT(a.id_activo) as total,
                   ROUND(COUNT(a.id_activo) * 100.0 / (SELECT COUNT(*) FROM activos), 2) as percentage
            FROM marcas mar
            JOIN modelos m ON mar.id_marca = m.id_marca
            LEFT JOIN activos a ON m.id_modelo = a.id_modelo
            GROUP BY mar.marca
            ORDER BY total DESC
        """
    }
    
    if query_id not in queries:
        raise HTTPException(status_code=404, detail="Query not found")
        
    try:
        cursor.execute(queries[query_id])
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
