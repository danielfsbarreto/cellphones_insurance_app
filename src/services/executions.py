import json
from base64 import b64decode, b64encode
from collections import defaultdict

from clients import CrewAiClient, S3Client
from models import Execution


class ExecutionsService:
    def __init__(self):
        self.s3 = S3Client()
        self.crewai = CrewAiClient()

    def list_executions(self):
        files = self.s3.list_files()
        grouped_files = defaultdict(list)
        for file in files:
            if file.uuid:
                grouped_files[file.uuid].append(file)
        executions = []
        for uuid, files in grouped_files.items():
            input_file = next(
                (f for f in files if f.key and f.key.endswith("input.xlsx")), None
            )
            output_file = next(
                (f for f in files if f.key and f.key.endswith("output.xlsx")), None
            )

            output_file = output_file or self._check_execution(uuid)

            executions.append(
                Execution(
                    uuid=uuid,
                    input_file=input_file,
                    output_file=output_file,
                    started_at=input_file.last_modified if input_file else None,
                    completed_at=output_file.last_modified if output_file else None,
                    status="pending" if input_file and not output_file else "completed",
                )
            )
        executions.sort(key=lambda e: e.started_at or 0, reverse=True)
        return executions

    def start_execution(self, file: bytes):
        uuid = self.crewai.kickoff(b64encode(file).decode("utf-8"))["kickoff_id"]
        self.s3.upload_file(file, uuid, "input.xlsx")

    def _check_execution(self, uuid: str):
        response = self.crewai.status(uuid)
        if response:
            print(f"Execution completed for [uuid='{uuid}']")
            result_dict = json.loads(response["result"])
            file = b64decode(result_dict["output_file"])
            return self.s3.upload_file(file, uuid, "output.xlsx")
