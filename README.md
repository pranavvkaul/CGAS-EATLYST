# Eatlyst

## Project Structure
 
```
CGAS-EATLYST/
├── index.html              # Landing page and primary navigation
├── home.html               # Recipe of the Day view
├── suggest.html            # Nutritional filtering view
├── code.ipynb               # Python scraping script (source of recipe data)
├── recipedata.csv          # Final, cleaned recipe data
├── recipedata.json         # JSON used by home.html
├── nutritiondata.csv       # Nutritional data
├── nutritiondata.json      # JSON used by suggest.html
└── images/                 # Directory containing all locally cached recipe image files

```

---

## Project Description

**Eatlyst** is an interactive web application developed as part of a Computational Gastronomy course (BIO544). The platform is designed to make healthy food discovery effortless and fun by leveraging scraped data and structured nutritional information. 

The website is running on the link: https://pranavvkaul.github.io/CGAS-EATLYST/

The application offers two primary features:

1. **Recipe of the Day:** Displays a randomly selected recipe upon every page refresh.

2. **Suggest a Food:** Allows users to find personalized food suggestions by filtering a dataset based on custom nutritional ranges (Carbohydrates, Protein, Fats, and Calories).

---

## Key Features and Technical Workflow

| Feature | Technical Implementation | Data Source |
|---------|-------------------------|-------------|
| **Data Acquisition** | Python with `requests` and `BeautifulSoup`. Parses a local `sitemap_1.xml` (from allrecipes.com) to extract 26 recipe links for scraping. | allrecipes.com |
| **Data Extracted** | Recipe Name, URL, Detailed Ingredients, Instructions, Prep Time, and Image URL. | Scraped data |
| **Image Handling** | Extracted image links are used to **manually download and cache** images into the local `/images` folder, referenced in `recipedata.csv`. This prevents broken links if the source site changes. | Local `images/` folder |
| **Nutritional Filtering** | Frontend JavaScript filters **39 food items** based on user-inputted min/max ranges for Cals, Carbs, Protein, and Fat. | fatsecret.co.in/.za/.sg/.uk/.nz/.com |
| **Frontend Data Use** | All CSV data (`recipedata.csv`, `nutritiondata.csv`) is converted to **JSON format** for fast, asynchronous loading in the HTML/JavaScript application. | JSON files |

---

## Data Files

The application relies on the following converted data files:

| File Name | Description | Used in HTML File |
|-----------|-------------|-------------------|
| `recipedata.json` | Contains the 26 scraped recipe details and **local image paths**. | `home.html` |
| `nutritiondata.json` | Contains 39 food items with Calorie, Carb, Protein, and Fat data per 100g. | `suggest.html` |

---

## Setup and Installation

### Prerequisites

You must have **Python 3.x** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/eatlyst.git
cd eatlyst
```

### 2. Install Required Libraries

Install the necessary Python packages for scraping and data handling:

```bash
pip install requests beautifulsoup4 pandas
```

### 3. Data Preparation (If Re-scraping)

1. Place your sitemap XML file (e.g., `sitemap_1.xml`) at the location specified in your Python script.

2. Run the scraping script (or the relevant code block) to generate `recipe_scraping.csv`.

3. **Note:** The final `recipedata.csv` and the local `/images` folder were curated **manually** after the initial scrape to download the images and link them correctly.

---

## Usage

### 1. The Web Application

The frontend is a static site and requires no server to run.

1. Open `index.html` in any modern web browser (e.g., Chrome, Firefox).

2. Use the main buttons to navigate to:
   - **Recipe of the Day** (`home.html`): Displays a randomly selected recipe on load.
   - **Suggest a Food** (`suggest.html`): Filter foods by nutritional ranges.

---

## Acknowledgements

This project was developed by **Pranav Kaul** as part of the **Computational Gastronomy (BIO544)** course, taught at **IIIT-Delhi** by **Prof. Ganesh Bagler**.

---

## References

The data used in this project was sourced from the following platforms:

Recipe Data: allrecipes.com

Nutritional Data: fatsecret.co.in/.za/.sg/.uk/.nz/.com

---

## License

This project is for educational purposes. Please respect the data sources and follow ethical scraping practices.
