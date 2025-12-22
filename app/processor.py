# import pandas as pd
# import os
# from io import BytesIO
# from datetime import datetime
# from address_mapping import address_mapping

# time_ranges = {
#     '00:00-06:00': (0, 6),
#     '06:00-12:00': (6, 12),
#     '12:00-18:00': (12, 18),
#     '18:00-24:00': (18, 24),
# }

# direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
# env_cols = ['Temp (°C)', 'Humidity %']
# ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

# def smart_round(val):
#     try:
#         return round(float(val), 2)
#     except:
#         return None

# def process_folder_in_memory(folder_path):
#     results = []

#     for file in os.listdir(folder_path):
#         if not file.endswith(".xlsx"):
#             continue

#         device = os.path.splitext(file)[0]
#         location = address_mapping.get(device, "Unknown Location")

#         df = pd.read_excel(os.path.join(folder_path, file), skiprows=6, header=None)

#         df.columns = (
#             ['Time']
#             + direct_ugm3_cols[:3]
#             + [f'{g} (ug/m3)' for g in ppb_gases]
#             + ['CO2 (ppm)']
#             + env_cols
#             + [direct_ugm3_cols[-1]]
#         )

#         df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
#         df.dropna(subset=['Time'], inplace=True)
#         if df.empty:
#             continue

#         df['Hour'] = df['Time'].dt.hour
#         date_val = df['Time'].dt.date.iloc[0]

#         for slot, (s, e) in time_ranges.items():
#             dslot = df[(df['Hour'] >= s) & (df['Hour'] < e)]
#             if dslot.empty:
#                 continue

#             row = {
#                 "Device": device,
#                 "Location": location,
#                 "Date": date_val,
#                 "Time Slot": slot
#             }

#             for col in df.columns.drop(['Time', 'Hour']):
#                 row[f"{col} Min"] = smart_round(dslot[col].min())
#                 row[f"{col} Max"] = smart_round(dslot[col].max())

#             results.append(row)

#     result_df = pd.DataFrame(results)

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine="openpyxl") as writer:
#         result_df.to_excel(writer, index=False)

#     output.seek(0)
#     filename = f"GSPCB_{datetime.now().strftime('%Y%m%d')}.xlsx"

#     return output, filename


import pandas as pd
from io import BytesIO
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


def process_excel_streams(excel_files: dict):
    """
    excel_files = {
        'MCT2408041.xlsx': BytesIO(),
        'MCT2408046.xlsx': BytesIO()
    }
    """

    results = []

    for filename, file_stream in excel_files.items():
        device = filename.replace(".xlsx", "")
        location = address_mapping.get(device, "Unknown Location")

        df = pd.read_excel(file_stream, skiprows=6, header=None)

        df.columns = (
            ['Time']
            + direct_ugm3_cols[:3]
            + [f'{g} (ug/m3)' for g in ppb_gases]
            + ['CO2 (ppm)']
            + env_cols
            + [direct_ugm3_cols[-1]]
        )

        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        df.dropna(subset=['Time'], inplace=True)
        if df.empty:
            continue

        df['Hour'] = df['Time'].dt.hour
        date_val = df['Time'].dt.date.iloc[0]

        for slot, (s, e) in time_ranges.items():
            slot_df = df[(df['Hour'] >= s) & (df['Hour'] < e)]
            if slot_df.empty:
                continue

            row = {
                "Device": device,
                "Location": location,
                "Date": date_val,
                "Time Slot": slot
            }

            for col in df.columns.drop(['Time', 'Hour']):
                row[f"{col} Min"] = smart_round(slot_df[col].min())
                row[f"{col} Max"] = smart_round(slot_df[col].max())

            results.append(row)

    result_df = pd.DataFrame(results)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        result_df.to_excel(writer, index=False)

    output.seek(0)
    filename = f"GSPCB_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return output, filename
