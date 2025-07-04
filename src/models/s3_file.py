from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class S3File(BaseModel):
    bucket: Optional[str]
    key: Optional[str]
    uuid: Optional[str]
    last_modified: Optional[datetime]
    url: Optional[str]
    content: Optional[Any] = None
