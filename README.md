# pupalink
by [aykxt](https://github.com/aykxt) and [billaids](https://github.com/billaids/)

## Only for educational purposes!
---
## Features
- Search and download books from Springer Link

## How to start?
- You need an active Springer Link access
- Use from your cookie the value from parameter "idp_session"

<div class="termy">

```console
$ from pupalink import Session

$ session = Session("YOUR_IDP_SESSION)

```
</div>

## Example 

<div class="termy">

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
</div>