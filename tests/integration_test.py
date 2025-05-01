import asyncio

from starlette import status

from tests.common.base_integration import BaseIntegrationTestCase


class IntegrationTest(BaseIntegrationTestCase):
    async def test_get_data_concurrently(self):
        concurrency = 5
        tasks = [self.aclient.get("/v2/data") for _ in range(concurrency)]

        responses = await asyncio.gather(*tasks)

        self.assertEqual(len(responses), concurrency)
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    async def test_post_data_concurrently(self):
        concurrency = 5
        tasks = [self.aclient.post("/v2/data") for _ in range(concurrency)]

        responses = await asyncio.gather(*tasks)

        child_id_list = []
        parent_id_list = []
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            child, parent = response.json()
            child_id_list.append(child.get('id'))
            parent_id_list.append(parent.get('id'))

        self.assertEqual(len(child_id_list), concurrency)
        self.assertEqual(len(parent_id_list), concurrency)

    async def test_get_data(self):
        response = await self.aclient.get("/v2/data")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    async def test_post_data(self):
        response = await self.aclient.post("/v2/data")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()), 2)
