# UK Real Estate Leads Extractor 🚀

A professional-grade data extraction engine designed to scrape, audit, and export high-intent business leads from the Yelu.uk directory. This tool is built for resilience, handling pagination and data normalization for over 480+ target agencies.

## 📊 Business Value
Unlike basic scrapers, this tool includes a **Data Integrity Layer**. It doesn't just collect text; it audits the results to identify gaps in source-level data (e.g., missing Establish Dates or Employee counts), providing a "Data Density" report essential for lead qualification.

## 🛠️ Technical Features
* **Modular Architecture:** Logic is separated into extraction engines and helper utilities for easy maintenance.
* **Resilient Parsing:** Uses `BeautifulSoup4` with the `lxml` parser for high-speed, robust HTML traversal.
* **Data Pipeline:** Integrated `Pandas` workflow to clean raw HTML noise before exporting to structured formats.
* **Multi-Format Export:** Generates both `CSV` for raw database imports and `XLSX` (Excel) for client-ready viewing.

## 📂 Project Structure
* **`main.py`**: The central orchestrator. It manages the end-to-end workflow, from link discovery to final file export.
* **`AgencyLinksExtractor.py`**: The "Scout" module. Handles pagination and high-level directory navigation to gather target URLs.
* **`AgenciesDatasExtractor.py`**: The "Harvester" module. Performs deep-page parsing to extract granular agency details.
* **`AgencyStructure.py`**: The "Architect." Defines the data models and ensures the extracted data follows a consistent schema.
* **`helper_functions.py`**: The "Toolbox." Contains reusable logic for data cleaning, logging, and error management.
* **`requirements.txt`**: The "Manifest." Lists all dependencies required to build the environment.
* **`UK_RealEstate_leads_data_sample.xlsx`**: The "Proof." A verified export of the engine's output.

## 🚀 Quick Start

### 1. Clone & Navigate
```bash
git clone [https://github.com/aMoro21/UK-real-estate-leads-extractor.git](https://github.com/aMoro21/UK-real-estate-leads-extractor.git)
cd UK-real-estate-leads-extractor
