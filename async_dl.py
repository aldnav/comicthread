"""
asyncio version of `script.py`
previously it uses threads managed by the OS
now asyncio manages it using cooperative multitasking

@author Aldrin Navarro <aldrinnavarro16@gmail.com>
@date 2019-01-24
"""

import asyncio
import aiohttp
from lxml import html
from lxml.cssselect import CSSSelector


async def download_page(context, queue):
    """Downloads a page and saves the body into queue"""
    url, selector = context
    await asyncio.sleep(0)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            queue.put_nowait((body, selector))
            return body


async def get_image(queue):
    """When there is an item in queue, parse to get comics url"""
    while True:
        payload = await queue.get()
        await asyncio.sleep(0)
        body, selector = payload
        tree = html.fromstring(body)
        select = CSSSelector(selector)
        elements = [e.get('src') for e in select(tree)]
        if len(elements) > 0:
            url = elements[0]
            if not (url.startswith('http:') or url.startswith('https:')):
                url = 'https:' + url
            print('  ', url)
        # ack queue that the item has been processed
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    sources = [
        'https://c.xkcd.com/random/comic',
        'http://www.commitstrip.com/?random=1'
    ]
    selectors = [
        '#comic img',
        '.entry-content p img'
    ]
    tasks = []
    for url, selector in zip(sources, selectors):
        task = asyncio.create_task(download_page((url, selector), queue))
        tasks.append(task)

    asyncio.ensure_future(get_image(queue))
    await queue.join()
    print('Here are your comics')
    await asyncio.gather(*tasks, return_exceptions=True)
    print('Go fun your self!')


asyncio.run(main())
