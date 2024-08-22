import traceback
import asyncio
import csv
import xml.etree.ElementTree as ET
import requests


class Spider:
    def __init__(self, url):
        self.url = url
        self.loop = asyncio.get_event_loop()
        self.parse()

    def extract_and_store_data(self, entry, writer):
        title = entry.find("title").text
        link = entry.find("link").text
        price = entry.find("price").text if entry.find("price") is not None else ""
        description = entry.find("description").text
        year = entry.find("year").text if entry.find("year") is not None else ""
        transmission = (
            entry.find("transmission").text
            if entry.find("transmission") is not None
            else ""
        )
        condition = (
            entry.find("condition").text if entry.find("condition") is not None else ""
        )
        colors = [color.text for color in entry.findall("colors/color")]

        images = [img.text for img in entry.findall("images/img")]

        images_str = ''
        for i, m in enumerate(images):
            breaker = '\n'
            if (i == (len(images) - 1)):
                breaker = ''
            images_str = images_str + m + breaker

        colors_str = ''
        for i, m in enumerate(colors):
            breaker = '\n'
            if (i == (len(colors) - 1)):
                breaker = ''
            colors_str = colors_str + m + breaker

        writer.writerow(
            [
                title,
                link,
                price,
                description,
                images_str,
                colors_str,
                year,
                transmission,
                condition,
            ]
        )

    def parse(self):
        """
        This function parses the rss feed
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/xml",
            }
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                xml_data = response.content

                with open(
                    "scrapped_data.csv", mode="w", newline="", encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            "Title",
                            "Link",
                            "Price",
                            "Description",
                            "Images",
                            "Colors",
                            "Year",
                            "Transmission",
                            "Condition",
                        ]
                    )
                    # feed = feedparser.parse(self.url)
                    root = ET.fromstring(xml_data)
                    count = 0

                    # for entry in feed.entries:
                    for entry in root.findall("./channel/item"):
                        self.extract_and_store_data(entry, writer)
                        count = count + 1
                        # if count == 6:
                        #     print(entry)
                        #     break

                        print(f"Entry {count} is scrapped")
                    print(f"Total scrapped entries from this site are {count}")
            else:
                print(f"Failed to retrieve data: {response.status_code}")

        except Exception as _:
            traceback.print_exc()
