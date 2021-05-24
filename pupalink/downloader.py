from typing import AsyncGenerator
import aiohttp
import urllib.parse as urlparse
import os
import re

from .metadata import Book, list_books


class Session:
    def __init__(
        self, idp_session: str, proxy: str = None, path: str = os.getcwd()
    ) -> None:
        """
        Creates an instance of a Springer Link session.

        Args:
            idp_session: This token is needed to download books from Springer Link.

            proxy: The proxy configuration to use, e.g `"http://user:pass@some.proxy.com"`
                !!! Info
                    The session uses the proxy configuration from the `HTTP_PROXY`
                    environment variables if present.
            path: Pass your download path, otherwise it will use the current working directory

        """

        self.__proxy = proxy
        self.__idp_session = idp_session
        self.__cookies = {"idp_session": self.__idp_session}
        self.__current_dir = path
        self._http = aiohttp.ClientSession(
            cookies=self.__cookies, trust_env=True)

    def get_file_name(self, url: str):
        return os.path.basename(urlparse.urlparse(f"{url}").path)

    async def request_site(self, url):
        async with self._http.get(url, proxy=self.__proxy) as response:
            html = await response.text()
            books = list_books(html)
            return books

    async def search_book(self, book_name: str) -> list[Book]:
        book = re.sub(" ", "+", book_name)
        url = f"https://link.springer.com/search?query={book}&facet-content-type=%22Book%22"
        async with self._http.get(url, proxy=self.__proxy) as response:
            html = await response.text()
            books = list_books(html)
            return books

    async def download_book(self, book: Book) -> bytes:
        async with self._http.get(book.download_link, proxy=self.__proxy) as response:
            return await response.read()

    async def stream_book(self, book: Book) -> AsyncGenerator[bytes, None]:
        async with self._http.get(book.download_link, proxy=self.__proxy) as response:
            async for chunk in response.content.iter_chunked(2048):
                yield chunk

    async def save_book(self, book: Book):
        with open(f"{self.__current_dir}/{book.name}.pdf", "wb") as f:
            async for chunk in self.stream_book(book):
                f.write(chunk)

    async def close(self):
        await self._http.close()
