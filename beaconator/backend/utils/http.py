import asyncio
import typing
from socket import AF_INET

import aiohttp

SIZE_POOL_AIOHTTP = 100


# https://github.com/tiangolo/fastapi/issues/236#issuecomment-616509245


class SingletonAiohttp:
    sem: asyncio.Semaphore = None
    aiohttp_client: aiohttp.ClientSession = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector
            )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str) -> typing.Dict:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url) as response:
                response.raise_for_status()
                json_result = await response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result

    @classmethod
    async def post_payload(cls, url: str, payload: typing.Dict) -> typing.Dict:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url, data=payload) as response:
                response.raise_for_status()
                json_result = await response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result
