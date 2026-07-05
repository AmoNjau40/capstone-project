import requests
from bs4 import BeautifulSoup
import csv

# User-Agent header
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Wikipedia pages for the crops
crop_urls = [
    "https://en.wikipedia.org/wiki/Maize",
    "https://en.wikipedia.org/wiki/Green_bean",
    "https://en.wikipedia.org/wiki/Broccoli",
    "https://en.wikipedia.org/wiki/Tomato",
    "https://en.wikipedia.org/wiki/Rice"
]

# Create CSV file
with open("crop_information.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    # Write column headings
    writer.writerow(["Crop", "Description"])

    # Loop through each crop page
    for url in crop_urls:

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            # Get crop name
            title = soup.find("h1").get_text()

            # Get all paragraphs
            paragraphs = soup.find_all("p")

            description = ""

            # Find the first non-empty paragraph
            for paragraph in paragraphs:

                text = paragraph.get_text(strip=True)

                if text:
                    description = text
                    break

            # Save to CSV
            writer.writerow([title, description])

            print(f"{title} saved successfully.")

        else:
            print(f"Failed to retrieve {url}")

print("Data successfully saved to crop_information.csv")
       

