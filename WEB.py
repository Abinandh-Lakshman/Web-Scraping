import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lists to store data
Names = []
prices = []
reviews = []
Cameras = []
Display = []
Battery = []

# Define the range of pages to scrape
start_page = 2
end_page = 50

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for page_num in range(start_page, end_page + 1):
    # Update the link with the current page number
    link = f"https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_3_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_3_0_na_na_na&as-pos=3&as-type=HISTORY&suggestionId=mobiles&requestId=829e23bc-10c1-4844-97d5-59d452978ce3&page={page_num}"

    try:
        # Fetch the page content
        r = requests.get(link, headers=headers)
        r.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {page_num}: {e}")
        continue

    # Parse the page content
    soup = BeautifulSoup(r.text, "html.parser")

    # Find the container with the product details
    page = soup.find("div", class_="DOjaWF gdgoEp")
    if not page:
        print(f"No product container found on page {page_num}")
        continue

    # Extract mobile names
    try:
        tag = page.find_all('div', class_='KzDlHZ')
        mobile_names = [div.get_text(strip=True) for div in tag if div.get_text(strip=True)]
        Names.extend(mobile_names)
    except AttributeError:
        print(f"Failed to extract names on page {page_num}")

    # Extract prices
    try:
        price_div = page.find_all('div', class_='Nx9bqj')
        price = [div.get_text(strip=True) for div in price_div if div.get_text(strip=True)]
        prices.extend(price)
    except AttributeError:
        print(f"Failed to extract prices on page {page_num}")

    # Extract reviews
    try:
        review_div = page.find_all('div', class_='XQDdHH')
        review = [div.get_text(strip=True) for div in review_div if div.get_text(strip=True)]
        reviews.extend(review)
    except AttributeError:
        print(f"Failed to extract reviews on page {page_num}")

    # Extract camera details
    try:
        products = page.find_all("ul", class_="G4BRas")
        for box in products:
            camera = box.find_all('li', class_='J+igdf')[2]
            Cameras.append(camera.text.strip())
    except (AttributeError, IndexError):
        print(f"Failed to extract camera details on page {page_num}")

    # Extract display details
    try:
        bat1 = page.find_all("ul", class_="G4BRas")
        for battery in bat1:
            bat = battery.find_all('li', class_='J+igdf')[1]
            Display.append(bat.text.strip())
    except (AttributeError, IndexError):
        print(f"Failed to extract display details on page {page_num}")

    # Add a delay to avoid being blocked
    time.sleep(2)

# Ensure all lists have the same length
max_length = max(len(Names), len(prices), len(reviews), len(Cameras), len(Display))
Names += [None] * (max_length - len(Names))
prices += [None] * (max_length - len(prices))
reviews += [None] * (max_length - len(reviews))
Cameras += [None] * (max_length - len(Cameras))
Display += [None] * (max_length - len(Display))

# Create a DataFrame and save to Excel
df = pd.DataFrame({
    "Name": Names,
    "Price": prices,
    "Reviews": reviews,
    "Camera": Cameras,
    "Display": Display
})

print(df)
import datetime
try:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Flipkart_Mobiles_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"File saved successfully as {filename}")
except Exception as e:
    print(f"Failed to save file: {e}")