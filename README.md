<img align="right" src="https://user-images.githubusercontent.com/14788425/119204060-d10abc80-ba94-11eb-91a0-72b0d0ab3649.png" height="300px">

# ♞ pupalink

A simple Python module to search and download books from SpringerLink.

---

> 🧪 **This project is still in an early stage of development. Expect breaking
> changes**.

---

## Features

- Search and download books from Springer Link

## Prerequisites

- An active SpringerLink account with premium access.

## Getting started

Sign in to your SpringerLink account and copy the `idp_session` cookie and paste it like below:

```python
from pupalink import Session

session = Session("YOUR_IDP_SESSION")
```

### Example 

```python
from pupalink import Session
from asyncio import get_event_loop

async def main():
    session = Session("YOUR_KEY")
    books = await session.search_book("Rust")

    for book in books:
        await session.download_book(book)

    await session.close()


loop = get_event_loop()
loop.run_until_complete(main())

```