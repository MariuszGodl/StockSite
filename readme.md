# 📈 GPW Stock Data Scraper & Dashboard  

This project provides a complete system for scraping, storing, and visualizing data from the Warsaw Stock Exchange (GPW – Giełda Papierów Wartościowych w Warszawie).  
It combines **Python ETL pipelines**, **MySQL database**, **Selenium web scraping**, and a **Django web application** for interactive visualization.  

---

## 🚀 Features  

- **Web Scraper (Selenium)**  
  - Downloads daily and historical GPW stock data.  
  - Extracts company details (sector, CEO, shares, description, etc.).  
  - Automatically handles cookies, downloads, and retries.  

- **ETL (Extract – Transform – Load)**  
  - Cleans raw files and loads data into a structured database.  
  - Standardizes company names and removes Polish diacritics.  

- **Database (MySQL)**  
  - Stores companies, daily values, and metadata.  
  - SQL schema with constraints to ensure data consistency.  

- **Django Web App**  
  - Interactive charts of historical prices.  
  - Search by company name or ticker.  
  - Random company suggestions for exploration.  
  - Detail view with ratios, capitalization, and comparisons.  

- **Additional Integrations**  
  - **ChatGPT API**: optional AI-based insights.  
  - **Docker (planned)** for easy deployment.  

---

## 🛠️ Tech Stack  

- 🐍 **Python** – ETL, scraping, backend logic  
- 🕷️ **Selenium** – stock market web scraping  
- 🐬 **MySQL** – main database  
- 🌐 **Django + HTML/CSS/JS** – web application  
- 🐧 **Linux server** – deployment environment  
- 📦 **venv** – dependency isolation  
- 📦 **Docker** – future containerization  

---

