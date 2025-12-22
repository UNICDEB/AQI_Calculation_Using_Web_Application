import pandas as pd
import os
from datetime import datetime
from address_mapping import address_mapping

time_ranges = {
    '00:00-06:00': (0, 6),
    '06:00-12:00': (6, 12),
    '12:00-18:00': (12, 18),
    '18:00-24:00': (18, 24),
}

direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
env_cols = ['Temp (°C)', 'Humidity %']
ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

def smart_round(val):
    try:
        return round(float(val), 2)
    except:
        return None

def process_folder(folder_path):
    results = []

    for file in os.listdir(folder_path):
        if not file.endswith(".xlsx"):
            continue

        device = os.path.splitext(file)[0]
        location = address_mapping.get(device, "Unknown Location")
        df = pd.read_excel(os.path.join(folder_path, file), skiprows=6, header=None)

        df.columns = (
            ['Time'] +
            direct_ugm3_cols[:3] +
            [f'{g} (ug/m3)' for g in ppb_gases] +
            ['CO2 (ppm)'] +
            env_cols +
            [direct_ugm3_cols[-1]]
        )

        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        df.dropna(subset=['Time'], inplace=True)

        if df.empty:
            continue

        df['Hour'] = df['Time'].dt.hour
        date_val = df['Time'].dt.date.iloc[0]

        final_cols = df.columns.drop(['Time', 'Hour'])

        for slot, (s, e) in time_ranges.items():
            dslot = df[(df['Hour'] >= s) & (df['Hour'] < e)]
            if dslot.empty:
                continue

            row = {
                "Device": device,
                "Location": location,
                "Date": date_val,
                "Time Slot": slot
            }

            for col in final_cols:
                row[f"{col} Min"] = smart_round(dslot[col].min())
                row[f"{col} Max"] = smart_round(dslot[col].max())

            results.append(row)

    result_df = pd.DataFrame(results)
    out_name = f"GSPCB_{datetime.now().strftime('%Y%m%d')}.xlsx"
    result_df.to_excel(out_name, index=False)
    return out_name
