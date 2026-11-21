
# AquaGuard Database Design

## 1. Database Overview

AquaGuard uses SQLite as its initial database.
SQLAlchemy is used for database operations.

The architecture supports future MySQL integration.

## 2. Database Tables

| Table | Description |
|---|---|
| users | Stores application users |
| locations | Stores monitored buildings |
| sensors | Stores sensor information |
| readings | Stores water flow readings |
| alerts | Stores detected abnormalities |
| inspections | Stores inspection activities |
| sensor_scenarios | Stores simulation scenarios |
| baselines | Stores expected consumption |
| system_settings | Stores application settings |
| audit_logs | Stores important user activities |

## 3. Relationships

- One location can have multiple sensors.
- One sensor can have multiple readings.
- One location can have multiple alerts.
- One alert can have multiple inspections.
- One user can perform multiple inspections.
- One sensor can have simulation scenarios.
- One location can have multiple hourly baselines.

## 4. Reading Data

Every reading contains:

- Sensor ID
- Timestamp
- Flow rate
- Data source
- Scenario
- Quality status

Flow rate is stored in litres per hour.

Timestamps are stored in UTC.

## 5. Data Integrity

The database uses:

- Primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- CHECK constraints
- Indexes

These help maintain reliable records.

## 6. Data Sources

AquaGuard supports:

- Virtual sensor
- CSV upload
- Manual entry
- Future physical sensors

## 7. Database Configuration

Default database: SQLite

Database file: instance/aquaguard.db

Future database option: MySQL

## 8. Database Maintenance

- Regular backups
- Database migrations
- Duplicate prevention
- Foreign key validation
- Transaction management
