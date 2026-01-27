# Request/Response Data Models for Smart Energy Platform
# These Pydantic models validate and document API request/response data

# Import Pydantic for data validation
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ============================================================================
# Request Data Models (Input Validation)
# ============================================================================
# These models define what data the API expects from clients

class EnergyReadingCreate(BaseModel):
    """
    Request model for creating a new energy reading.
    
    This model validates JSON input and provides documentation for API clients.
    Pydantic automatically converts and validates JSON to this Python object.
    
    Attributes:
        machine_id: Unique identifier for the machine (required)
        power_kw: Current power consumption in kilowatts (required)
        energy_consumed_kwh: Total energy consumed in kilowatt-hours (required)
    """
    
    # Machine identifier - required field
    machine_id: str = Field(
        ...,  # ... means this field is required
        min_length=1,  # At least 1 character
        max_length=50,  # Maximum 50 characters
        description="Unique identifier for the machine",
        example="MACHINE-001"
    )
    
    # Power in kilowatts - required field
    power_kw: float = Field(
        ...,  # Required
        ge=0,  # Greater than or equal to 0 (non-negative)
        description="Current power consumption in kilowatts",
        example=45.5
    )
    
    # Energy consumed in kilowatt-hours - required field
    energy_consumed_kwh: float = Field(
        ...,  # Required
        ge=0,  # Greater than or equal to 0 (non-negative)
        description="Total energy consumed in kilowatt-hours",
        example=1250.75
    )
    
    # Configuration for the model
    class Config:
        # Example JSON for documentation in Swagger UI
        schema_extra = {
            "example": {
                "machine_id": "MACHINE-001",
                "power_kw": 45.5,
                "energy_consumed_kwh": 1250.75
            }
        }

# ============================================================================
# Response Data Models (Output Format)
# ============================================================================
# These models define what data the API returns to clients

class EnergyReadingResponse(BaseModel):
    """
    Response model for energy reading creation/retrieval.
    
    This model defines the format of JSON responses returned by the API.
    """
    
    # Reading ID - returned by the database
    id: int = Field(description="Unique identifier (auto-generated)")
    
    # Machine identifier - echoed from request
    machine_id: str = Field(description="Machine identifier")
    
    # Power measurement
    power_kw: float = Field(description="Power consumption in kilowatts")
    
    # Energy measurement
    energy_consumed_kwh: float = Field(description="Energy consumed in kilowatt-hours")
    
    # Timestamp - set by database
    timestamp: datetime = Field(description="When the reading was recorded")
    
    # Pydantic configuration for ORM compatibility
    class Config:
        from_attributes = True  # Allow creation from SQLAlchemy models

class ErrorResponse(BaseModel):
    """
    Response model for error messages.
    
    This model defines the format of error responses.
    """
    
    # HTTP status code
    status_code: int = Field(description="HTTP status code")
    
    # Error message
    detail: str = Field(description="Error description")
    
    # Timestamp of the error
    timestamp: datetime = Field(description="When the error occurred")
