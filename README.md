# 🔍 Engineering Error Code Lookup

A lightweight, local web application built with [Streamlit](https://streamlit.io/) and SQLite to help engineering teams log, search, and manage testing error codes across different test units and chambers.

## Features
- **Fast Search:** Look up error codes or test units instantly.
- **Add New Codes:** Easily log new error codes along with descriptions, test types, chambers, and remediation steps.
- **Import / Export Sync:** Seamlessly transfer your database to another computer. Export data as a CSV, and import it elsewhere to merge databases without losing unique entries!
- **Cross-Platform Scripts:** One-click startup scripts available for both Windows and Mac/Linux.
- **Docker Ready:** Completely containerized for consistent deployment.

---

## 🚀 How to Run Locally

You don't need any terminal experience to get started. Just ensure you have Python installed on your system.

### For Windows Users
1. Open this folder.
2. Double-click the **`run_windows.bat`** script.
3. The script will automatically create a virtual environment, install the required dependencies (`streamlit`, `pandas`), and open the app in your default web browser.

### For Mac / Linux Users
1. Open this folder.
2. Double-click the **`run_mac.command`** script.
   *(If it's your first time or it says permission denied, you may need to open your terminal and run `chmod +x run_mac.command` once).*
3. The script handles the virtual environment, installs dependencies, and launches the app.

---

## 🐳 How to Run via Docker

If you prefer using Docker to keep your system clean, this app is fully Dockerized and uses a volume mount to ensure your `error_codes.db` database is never lost.

1. Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. Open your terminal or command prompt in this folder.
3. Run the following command to build and start the app in the background:
   ```bash
   docker-compose up -d
   ```
4. Open your web browser and go to: `http://localhost:8501`
5. To stop the app when you're done, run:
   ```bash
   docker-compose down
   ```

---

## 📖 How to Use the App

### 1. Searching for Errors
Use the main text box in the center of the screen to search. You can search by **Error Code** (e.g., "E404") or by **Unit Name** (e.g., "SensorA"). The table will filter instantly.

### 2. Adding a New Error
On the left-hand sidebar, fill out the **Add New Error** form with the relevant details:
- **Test Unit:** The name of the unit under test.
- **Test Type:** The kind of test being run (e.g., Thermal, Vibration).
- **Chamber:** The chamber or station where the test occurred.
- **Error Code:** The specific alphanumeric code triggered.
- **Description:** What the error actually means.
- **Remediation:** How to fix it or what steps to take next.
Click **Submit** to instantly add it to your local SQLite database.

### 3. Syncing Data Across Computers
If you want to move your app to a new computer, or merge your codes with a coworker's codes:
1. On **Computer A**, go to the sidebar, expand **Import / Export Data**, and click **Download Data (CSV)**.
2. Transfer that CSV file (e.g., via email or flash drive) to **Computer B**.
3. On **Computer B**, open the app, expand **Import / Export Data**, and upload the CSV file using the **Upload CSV** box. 
4. Click **Sync Data**. The app will safely merge the data—adding any brand new codes and updating the descriptions of existing ones. Your unique local codes will remain untouched!
