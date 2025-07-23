import asyncio
import os

import aiohttp
import requests


class CrewAiClient:
    CREWAI_ENTERPRISE_URL = os.getenv("CREWAI_ENTERPRISE_URL")
    CREWAI_ENTERPRISE_API_KEY = os.getenv("CREWAI_ENTERPRISE_API_KEY")
    CREWAI_ENTERPRISE_POLLING_RATE = int(
        os.getenv("CREWAI_ENTERPRISE_POLLING_RATE", 10)
    )

    def kickoff(self, id: str, input_file_base64: str):
        response = requests.post(
            f"{self.CREWAI_ENTERPRISE_URL}/kickoff",
            json={
                "inputs": {
                    "id": id,
                    "input_file": input_file_base64,
                }
            },
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    async def status(self, kickoff_id: str):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(
                        f"{self.CREWAI_ENTERPRISE_URL}/status/{kickoff_id}",
                        headers=self._headers,
                    ) as response:
                        response.raise_for_status()
                        response_json = await response.json()

                        if response_json.get("state") in ["SUCCESS", "FAILED"]:
                            return response_json

                        print(
                            f"Status check performed for [kickoff_id='{kickoff_id}']. No final state reached yet."
                        )
                        await asyncio.sleep(self.CREWAI_ENTERPRISE_POLLING_RATE)

                except Exception as e:
                    print(f"Error checking status: {e}")
                    await asyncio.sleep(60)

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self.CREWAI_ENTERPRISE_API_KEY}"}
