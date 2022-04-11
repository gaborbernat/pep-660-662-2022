from datetime import datetime
from typing import List

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "broken",
    "friends": [1, 2, "not a number"],
}
try:
    user = User(**external_data)
except ValidationError as e:
    print(e.json())
