import json
import aiohttp
import asyncio

def async_mass_request(json, urls, headers):
    async def request(session, url):
        async with session.get(url, headers=headers) as response:
            perms = await response.json()
            return perms

    async def get():
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[asyncio.ensure_future(request(session, url)) for url in urls])
            return results

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(get())