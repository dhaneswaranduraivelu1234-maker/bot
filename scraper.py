import requests
from bs4 import BeautifulSoup
import os
import time

# ----------------------------
# MANUAL CURATED URL LIST
# ----------------------------

URLS = [
    # Core pages
    "https://www.nitt.edu/",
    "https://www.nitt.edu/home/academics/",
    "https://www.nitt.edu/home/academics/programmes/",
    "https://www.nitt.edu/home/academics/nirf/",
    "https://www.nitt.edu/home/academics/admission_procedure/",
    "https://www.nitt.edu/home/academics/anti_ragging/",
    "https://www.nitt.edu/home/academics/contact_details/",
    "https://www.nitt.edu/home/admissions/",
    "https://www.nitt.edu/home/departments/",
    "https://www.nitt.edu/home/facilities/",
    "https://www.nitt.edu/home/facilities/hostels/",
    "https://www.nitt.edu/home/students/",
    "https://www.nitt.edu/home/placements/",
    "https://www.nitt.edu/home/placements/statistics/",
    "https://www.nitt.edu/home/research/",
    "https://www.nitt.edu/home/administration/director/",

    # Mechanical faculty
    "https://www.nitt.edu/home/academics/departments/mech/faculty/",

    # Additional department faculty pages
    "https://www.nitt.edu/home/academics/departments/cse/faculty/",
    "https://www.nitt.edu/home/academics/departments/chem/chemfaculty/",
    "https://www.nitt.edu/home/academics/departments/civil/faculty/",
    "https://www.nitt.edu/home/academics/departments/eee/people/faculty/",
    "https://www.nitt.edu/home/academics/departments/ice/faculty/",
    "https://www.nitt.edu/home/academics/departments/meta/faculty/",
    "https://www.nitt.edu/home/academics/departments/prod/faculty/",
]

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def clean_text(soup):
    # Remove script/style/nav/footer
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Clean extra blank lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def scrape():
    print("🚀 Starting curated scraping...\n")

    for idx, url in enumerate(URLS):
        try:
            print(f"Scraping: {url}")

            response = requests.get(url, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            clean_page = clean_text(soup)

            filename = os.path.join(DATA_DIR, f"page_{idx}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(clean_page)

            time.sleep(1)  # be polite to server

        except Exception as e:
            print(f"❌ Failed: {url}")
            print(e)

    print("\n✅ Scraping completed.")


if __name__ == "__main__":
    scrape()