import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_book_info(session, book_info):
    new_book_info = []
    for book_link in book_info:
        download_url = 'https://books.toscrape.com/catalogue/'
        work_url = book_link[2].strip('../')
        link = download_url + work_url
        work_link = await fetch(session, link)
        soup = BeautifulSoup(work_link, 'html.parser')
        book_table = soup.find('table', class_='table table-striped')
        book_data = []

        for table_row in book_table.find_all('tr'):
            data = [item.get_text(strip=True) for item in table_row.find_all('td')]
            book_data.extend(data)

        new_book_info.append(book_link + book_data)
    return new_book_info


async def parse_books_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    book_info = []

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color')
        book_link = book.h3.a['href']

        book_info.append([title, price, book_link])

    return book_info

async def save_to_csv(new_book_info):
    with open('book_info.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Link',
                         'UPC', 'Product Type', 'Price (excl. tax)',
                         'Price (incl. tax)', 'Tax', 'Availability',
                         'Number of reviews'])
        writer.writerows(new_book_info)

async def main():
    # TODO: Insert the link here.
    url = input("Enter link here: ")

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        book_info = await parse_books_info(html)
        other_book_info = await parse_book_info(session, book_info)

        await save_to_csv(other_book_info)

        print("CSV file saved successfully.")


if __name__ == "__main__":
    asyncio.run(main())