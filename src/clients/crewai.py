import os

import requests


class CrewAiClient:
    _URL = os.getenv("CREWAI_ENTERPRISE_URL")
    _API_KEY = os.getenv("CREWAI_ENTERPRISE_API_KEY")
    _POLLING_RATE = int(os.getenv("CREWAI_ENTERPRISE_POLLING_RATE", 30))

    def kickoff(self, input_file_base64: str):
        response = requests.post(
            f"{self._URL}/kickoff",
            json={
                "inputs": {
                    "input_file": input_file_base64,
                }
            },
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()

    def status(self, uuid: str):
        response = requests.get(
            f"{self._URL}/status/{uuid}",
            headers=self._headers,
        )
        response.raise_for_status()
        response_json = response.json()
        if response_json.get("state") in ["SUCCESS"]:
            return response_json
        return None

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self._API_KEY}"}
