# Technical Stack

## Data Format

- **Primary Format**: CSV files
- **Delimiter**: Semicolon (`;`) for official results, comma (`,`) for telemetry data
- **Encoding**: UTF-8

## Data Categories

### Race Results Files
- Naming pattern: `##_Description_Race #_Anonymized.CSV`
- Examples: `03_Provisional Results`, `05_Results by Class`, `99_Best 10 Laps By Driver`

### Telemetry Files
- Naming pattern: `R#_barber_[data_type].csv`
- Types: `lap_start`, `lap_end`, `lap_time`, `telemetry_data`

### Analysis Files
- Pattern: `##_Analysis[Type]_Race #_Anonymized.CSV`
- Contains sector times, improvements, and detailed lap analysis

## Common Data Fields

- **Vehicle Identification**: `vehicle_id`, `vehicle_number`, `original_vehicle_id`
  - Format: `GR86-[chassis]-[car_number]` (e.g., GR86-004-78)
  - Chassis number uniquely identifies vehicle
  - Car number 000 = not yet assigned to ECU
- **Timing**: `timestamp`, `lap`, `LAP_TIME`, sector times (S1, S2, S3)
  - `meta_time`: Message received time (accurate)
  - `timestamp`: ECU time (may be inaccurate)
  - `lap`: May be lost or show error value 32768
- **Metadata**: `meta_event`, `meta_session`, `meta_source`
- **Performance**: `TOP_SPEED`, `KPH`, lap improvements

## Telemetry Parameters

### Speed & Drivetrain
- `Speed`: Vehicle speed (km/h)
- `Gear`: Current gear selection
- `nmotor`: Engine RPM

### Throttle & Braking
- `ath`: Throttle blade position (0-100%)
- `aps`: Accelerator pedal position (0-100%)
- `pbrake_f`: Front brake pressure (bar)
- `pbrake_r`: Rear brake pressure (bar)

### Acceleration & Steering
- `accx_can`: Forward/backward acceleration (G's, + = accel, - = brake)
- `accy_can`: Lateral acceleration (G's, + = left, - = right)
- `Steering_Angle`: Wheel angle (degrees, 0 = straight, - = CCW, + = CW)

### Position & Lap Data
- `VBOX_Long_Minutes`: GPS longitude (degrees)
- `VBOX_Lat_Min`: GPS latitude (degrees)
- `Laptrigger_lapdist_dls`: Distance from start/finish (meters)

## Processing Notes

- All vehicles are Toyota GR86 in the "Am" class
- Timestamps are in ISO 8601 format
- Race sessions labeled as R1, R2, etc.
- Data includes both real-time (kafka:gr-raw) and processed results

## Known Data Issues

- **Lap count errors**: Lap may show as 32768 when lost; use time values to determine actual lap
- **ECU timestamp drift**: Prefer `meta_time` for accurate timing
- **Vehicle ID changes**: Car numbers may update between races; use chassis number for consistency
