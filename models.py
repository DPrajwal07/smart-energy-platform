# Database Models for Smart Energy Platform
# This file defines the structure of database tables

# Import SQLAlchemy components for creating database models
from sqlalchemy import Column, Integer, String, Float, DateTime, Index, CheckConstraint
from sqlalchemy.sql import func
from database import Base

# ============================================================================
# EnergyReading Model - Industrial Energy Data Table
# ============================================================================
# This SQLAlchemy model represents the energy_readings table in PostgreSQL
# It stores power consumption readings from industrial machines
class EnergyReading(Base):
    """
    Database model for industrial energy consumption readings.
    
    Table: energy_readings
    Description: Stores timestamped energy data from machines
    Purpose: Track power usage and energy consumption across the platform
    """
    
    # ========================================================================
    # Table Configuration
    # ========================================================================
    __tablename__ = "energy_readings"
    
    # ========================================================================
    # Column Definitions
    # ========================================================================
    
    # COLUMN 1: id (Primary Key)
    # Type: Integer (auto-incrementing)
    # Purpose: Unique identifier for each energy reading
    # Index: Yes (automatic for primary keys)
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    # COLUMN 2: machine_id (Foreign Key Reference)
    # Type: String(50)
    # Purpose: Identifies which machine/device this reading came from
    # Index: Yes (for fast queries filtering by machine)
    # Constraint: Cannot be null
    # Example: "MACHINE-001", "PUMP-A5", "COMPRESSOR-B2"
    machine_id = Column(
        String(50),
        nullable=False,
        index=True
    )
    
    # COLUMN 3: power_kw (Measurement Data)
    # Type: Float
    # Purpose: Current instantaneous power consumption in kilowatts
    # Constraint: Must be non-negative (power cannot be negative)
    # Range: 0.0 to millions of KW
    # Example: 45.5, 1000.25, 0.0
    power_kw = Column(
        Float,
        nullable=False
    )
    
    # COLUMN 4: energy_consumed_kwh (Measurement Data)
    # Type: Float
    # Purpose: Total cumulative energy consumed in kilowatt-hours
    # Constraint: Must be non-negative (energy is always positive or zero)
    # Range: 0.0 to millions of KWh
    # Example: 1250.75, 50000.5
    energy_consumed_kwh = Column(
        Float,
        nullable=False
    )
    
    # COLUMN 5: timestamp (Temporal Data)
    # Type: DateTime
    # Purpose: Records when this reading was captured
    # Default: Current database time (server_default)
    # Index: Yes (for range queries on time periods)
    # Used for: Time-series analysis, trend reports
    timestamp = Column(
        DateTime,
        nullable=False,
        index=True,
        server_default=func.now()
    )
    
    # ========================================================================
    # Table Constraints
    # ========================================================================
    
    # Constraint: Power must be non-negative
    __table_args__ = (
        CheckConstraint('power_kw >= 0', name='check_power_non_negative'),
        CheckConstraint('energy_consumed_kwh >= 0', name='check_energy_non_negative'),
        # Composite index for efficient queries by machine_id and timestamp
        Index('idx_machine_timestamp', 'machine_id', 'timestamp'),
    )
# ============================================================================
# Usage Examples
# ============================================================================

# 1. CREATE THE TABLE IN DATABASE
# --------------------------------
# from database import Base, engine
# Base.metadata.create_all(bind=engine)

# 2. QUERY ALL READINGS
# --------------------------------
# from sqlalchemy.orm import Session
# readings = db.query(EnergyReading).all()

# 3. QUERY READINGS FOR A SPECIFIC MACHINE
# --------------------------------
# readings = db.query(EnergyReading).filter(
#     EnergyReading.machine_id == "MACHINE-001"
# ).all()

# 4. QUERY READINGS FROM LAST 24 HOURS
# --------------------------------
# from datetime import datetime, timedelta
# yesterday = datetime.now() - timedelta(hours=24)
# recent_readings = db.query(EnergyReading).filter(
#     EnergyReading.timestamp >= yesterday
# ).all()

# 5. INSERT A NEW READING
# --------------------------------
# new_reading = EnergyReading(
#     machine_id="MACHINE-001",
#     power_kw=45.5,
#     energy_consumed_kwh=1250.75
# )
# db.add(new_reading)
# db.commit()

# 6. GET AVERAGE POWER FOR A MACHINE
# --------------------------------
# from sqlalchemy import func
# avg_power = db.query(func.avg(EnergyReading.power_kw)).filter(
#     EnergyReading.machine_id == "MACHINE-001"
# ).scalar()

# ============================================================================
# Database Schema Summary
# ============================================================================
# 
# Table Name: energy_readings
# 
# Columns:
#   1. id (INT, PRIMARY KEY, AUTO-INCREMENT)
#      - Unique identifier for each record
#      - Automatically assigned
#   
#   2. machine_id (VARCHAR(50), NOT NULL, INDEXED)
#      - Machine/device identifier
#      - Used for grouping and filtering
#   
#   3. power_kw (FLOAT, NOT NULL, CHECK >= 0)
#      - Current power consumption in kilowatts
#      - Validated to be non-negative
#   
#   4. energy_consumed_kwh (FLOAT, NOT NULL, CHECK >= 0)
#      - Total energy consumed in kilowatt-hours
#      - Validated to be non-negative
#   
#   5. timestamp (DATETIME, NOT NULL, INDEXED, DEFAULT NOW())
#      - When the reading was recorded
#      - Automatically set to current time if not provided
#
# Indexes:
#   - PRIMARY KEY on id (automatic)
#   - Single index on machine_id
#   - Single index on timestamp
#   - Composite index on (machine_id, timestamp) for efficient filtering
#
# Constraints:
#   - All columns except timestamp have defaults: NOT NULL
#   - power_kw >= 0 (non-negative)
#   - energy_consumed_kwh >= 0 (non-negative)
