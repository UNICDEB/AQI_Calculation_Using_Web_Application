# 🌏 AQI Data Processing Web Application

A premium, responsive web-based system developed using **FastAPI** for processing Air Quality Monitoring Excel data.  
The application allows users to upload multiple Excel files or a ZIP file, processes the data **in memory only**, and generates a consolidated **time-slot based AQI summary report**, which can be downloaded directly by the user.

---

## 📌 Key Features

- 📂 Upload multiple **Excel (.xlsx)** files  
- 🗜 Upload a **ZIP file** containing multiple Excel files  
- 🚫 **No uploaded files are saved on the server**  
- ⚙️ Data processing happens **entirely in memory**  
- 📊 Automatic generation of a consolidated Excel report  
- ⏱ 24-hour data divided into time slots  
- 📥 One-click download of the final result file  
- 📱 Fully responsive UI (Desktop, Laptop, Tablet, Mobile)  
- 🎨 Premium frontend using **Bootstrap 5**  
- 🏛 Suitable for government / scientific deployments  

---

## 🏗 Technology Stack

### Backend
- **Python 3.9+**
- **FastAPI**
- Pandas
- OpenPyXL
- Uvicorn

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (Fetch API)

---

## 📁 Project Folder Structure

AQI_Calculation_Using_Web_Application/
│
├── app/
│ ├── main.py # FastAPI application
│ ├── processing.py # Core AQI data processing logic
│ │
│ ├── templates/
│ │ └── index.html # Responsive frontend UI
│ │
│ └── static/
│ ├── css/
│ │ └── style.css # Premium responsive styles
│ └── js/
│ └── app.js # Frontend logic (upload & download)
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── run.sh / run.bat # Optional run script



---

## 🚀 Application Workflow

1. User opens the web application  
2. Uploads:
   - Multiple `.xlsx` files **OR**
   - One `.zip` file containing Excel files  
3. Clicks **Process Data**
4. Server:
   - Reads files **without saving**
   - Extracts Excel data (ZIP handled safely)
   - Performs time-slot based aggregation
5. User clicks **Download Final Excel**
6. File downloads directly to user's device

---

## ⏰ Time Slot Division

The AQI data is divided into four fixed time ranges:

| Time Slot | Hours |
|---------|------|
| 00:00–06:00 | Midnight to Early Morning |
| 06:00–12:00 | Morning |
| 12:00–18:00 | Afternoon |
| 18:00–24:00 | Evening & Night |

For each slot, **Min and Max values** are calculated.

---

## 📊 Parameters Processed

### Pollutants (µg/m³)
- PM10  
- PM2.5  
- PM1  
- NO₂  
- SO₂  
- CO  
- O₃  

### Gases
- CO₂ (ppm)

### Environmental
- Temperature (°C)  
- Humidity (%)  

### Index
- Air Quality Index (AQI)

---

## 🔐 Security & Data Handling

- ❌ No file is stored on server disk
- ❌ ZIP folder structure is ignored
- ✅ Only `.xlsx` files are read
- ✅ Safe in-memory processing
- ✅ Prevents path traversal and folder pollution

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/UNICDEB/AQI_Calculation_Using_Web_Application.git
cd AQI_Calculation_Using_Web_Application
