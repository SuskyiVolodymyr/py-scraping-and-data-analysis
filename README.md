# Python Vacancies Scraper on DOU and Data Analysis
## Project Description
This project is designed for scraping Python job vacancies from the DOU website, collecting data, and conducting analysis. The data collected includes:

- Job Title
- City
- Salary
- List of technologies mentioned in the job description

The scraping process is carried out in the vacancies_scraping/parse.py file. After running this file, a technologies.csv file will be created in the data directory, containing the collected data for further analysis.

## Project Structure
- vacancies_scraping/parse.py: The file for scraping data from the DOU website.
- data/: Directory where the collected data (technologies.csv) and generated graphs in PNG format are stored.
- data_analysis/main.ipynb: Jupyter Notebook that performs data analysis:
  - Finds the top 10 most frequently mentioned technologies.
  - Creates a pie chart of all technologies and their frequency of mentions.
  - Creates a bar chart of the average minimum salary relative to cities.
  - Creates a bar chart of the average maximum salary relative to cities.

## Technologies Used
- aiohttp: For asynchronous requests to web pages.
- BeautifulSoup: For parsing the HTML content of the pages.
- Selenium: For interacting with the pages and loading all job vacancies on the website.
- pandas: For data processing and analysis.
- numpy: For numerical computations.
- matplotlib: For creating visualizations.

## How to Run the Project

1. **Clone the repository:**
```bash
git clone <repository-url>
cd py-scraping-and-data-analysis
```
2. **Set up the virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install the dependencies:**
```bash
pip install -r requirements.txt
```

### Scraping Vacancies:

Navigate to the vacancies_scraping/ directory.

Run the parse.py file:

```bash
python vacancies_scraping/parse.py
```

After the script completes, the technologies.csv file will be created in the data/ directory.
### Data Analysis:

Open data_analysis/main.ipynb in Jupyter Notebook or any other environment that supports Jupyter Notebooks.
Execute all cells in the notebook to perform data analysis.
The resulting graphs will be saved in the data/ directory in PNG format.

## Results
- technologies.csv: A file containing the collected data on Python job vacancies from DOU.
- A pie chart of top 10 technologies by their frequency of mentions.
- A bar chart of all technologies and their frequency of mentions.
- A bar chart of the average minimum salary relative to cities.
- A bar chart of the average maximum salary relative to cities.

## Notes
- Ensure you have a web driver for Selenium installed (e.g., ChromeDriver) that matches the version of your browser.
- Depending on your internet connection speed and system performance, some parameters (e.g., page load wait times) in the scripts may need adjustment for successful execution.
