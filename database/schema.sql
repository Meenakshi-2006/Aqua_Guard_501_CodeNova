
-- 7. SENSOR SCENARIOS
CREATE TABLE IF NOT EXISTS sensor_scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    scenario_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 0,
    simulation_speed INTEGER NOT NULL DEFAULT 1,
    started_at DATETIME,

    FOREIGN KEY (sensor_id)
        REFERENCES sensors(id)
        ON DELETE CASCADE,

    CHECK (simulation_speed > 0)
);


-- 8. BASELINES
CREATE TABLE IF NOT EXISTS baselines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    weekday_type VARCHAR(20) NOT NULL,
    hour_of_day INTEGER NOT NULL,
    expected_flow FLOAT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (location_id)
        REFERENCES locations(id)
        ON DELETE CASCADE,

    UNIQUE (location_id, weekday_type, hour_of_day),

    CHECK (hour_of_day >= 0 AND hour_of_day <= 23),
    CHECK (expected_flow >= 0)
);


-- 9. SYSTEM SETTINGS
CREATE TABLE IF NOT EXISTS system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value VARCHAR(255) NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- 10. AUDIT LOGS
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


-- Useful additional indexes
CREATE INDEX IF NOT EXISTS idx_readings_timestamp
ON readings(timestamp);

CREATE INDEX IF NOT EXISTS idx_alerts_status
ON alerts(status);

CREATE INDEX IF NOT EXISTS idx_scenarios_sensor
ON sensor_scenarios(sensor_id);
