from __future__ import annotations
from dataclasses import dataclass
from bs4 import BeautifulSoup


def list_books(cached_site: str) -> list[Book]:
    soup = BeautifulSoup(cached_site, "lxml")
    books = []

    results = soup.find(id="results-list")

    for result in results.find_all("li"):
        meta = result.find("div", "text")
        book_header = meta.h2.a
        book_name = book_header.string
        isbn = book_header.attrs["href"].split("/").pop()
        authors = result.find("span", "authors")
        authors_list = [a.string for a in authors.find_all("a")]
        books.append(Book(book_name, authors_list, isbn))

    return books


@dataclass
class Book:
    name: str
    authors: list[str]
    isbn: str

    def get_cover(self, width: int = None) -> str:
        if width:
            return f"https://media.springernature.com/w{width}/springer-static/cover-hires/book/{self.isbn}"
        return f"https://media.springernature.com/original/springer-static/cover-hires/book/{self.isbn}"

    def gen_dl_link(self) -> str:
        return f"https://link.springer.com/content/pdf/10.1007%2F{self.isbn}.pdf"
