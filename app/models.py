from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    id_funcionario: Optional[int] = None
    name: str
    document: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class LocationCreate(BaseModel):
    name: str

class AssetTypeCreate(BaseModel):
    type: str

class AssetCreate(BaseModel):
    asset_id: Optional[int] = None
    type_id: int
    location_id: int
    model_id: int
    part_number: Optional[str] = None
    serial: Optional[str] = None
    processor: Optional[str] = None
    hard_drive: Optional[str] = None
    ram: Optional[str] = None

class BrandCreate(BaseModel):
    brand: str

class ModelCreate(BaseModel):
    model: str
    brand_id: int

class ResponsibilityCreate(BaseModel):
    asset_id: int
    employee_id: int
    assignment_date: date
    end_date: Optional[date] = None
