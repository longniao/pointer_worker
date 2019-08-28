# -*- coding: utf-8 -*-

import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        for year in range(2013, 2015):
            begintime = '%s0101' % year
            endtime = '%s0101' % (year + 1)
            print(begintime, endtime)
            url = 'https://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=%s&endtime=%s&page=1&per_page=1000&webp=1' % (begintime, endtime)

            data = await fetch(session, url)
            print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())