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
* `main.py`: The central execution script and workflow controller.
* `AgenciesDatasExtractor.py`: The core scraping logic and HTML parsing engine.
* `helper_functions.py`: Utility functions for data cleaning and formatting.
* `UK_RealEstate_leads_data_sample.xlsx`: A verified sample of 480+ extracted leads.

## 🚀 Quick Start

### 1. Clone & Navigate
```bash
git clone [https://github.com/aMoro21/UK-real-estate-leads-extractor.git](https://github.com/aMoro21/UK-real-estate-leads-extractor.git)
cd UK-real-estate-leads-extractor
