# Project Structure

## Root Directory

```
/
├── barber/                          # Race data for Barber Motorsports Park
│   ├── 03_*Results*.CSV            # Official race results
│   ├── 05_*Results by Class*.CSV   # Class-specific results
│   ├── 23_*AnalysisEndurance*.CSV  # Detailed lap/sector analysis
│   ├── 26_Weather*.CSV             # Weather conditions
│   ├── 99_*Best 10 Laps*.CSV       # Top lap times per driver
│   ├── R#_barber_lap_start.csv     # Lap start timestamps
│   ├── R#_barber_lap_end.csv       # Lap end timestamps
│   ├── R#_barber_lap_time.csv      # Lap timing data
│   └── R#_barber_telemetry_data.csv # Vehicle telemetry (large files)
└── Barber_Circuit_Map.pdf          # Track layout reference
```

## File Organization

### By Race Session
- **R1**: Race 1 data files
- **R2**: Race 2 data files

### By Data Type
- **Results**: Official classifications and standings
- **Timing**: Lap and sector times
- **Telemetry**: Real-time vehicle data streams
- **Analysis**: Processed performance metrics
- **Weather**: Environmental conditions

## Naming Conventions

- Race files prefixed with race number: `R1_`, `R2_`
- Official results numbered: `03_`, `05_`, `23_`, `26_`, `99_`
- All driver/team data is anonymized
- CSV extensions in uppercase for official results, lowercase for telemetry

## Data Relationships

- Link files using `vehicle_number` or `vehicle_id`
- Match race sessions using `meta_session` field
- Correlate timing using `timestamp` and `lap` fields
