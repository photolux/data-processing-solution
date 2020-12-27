from datetime import datetime
from faust import Record


class Signal(Record):
    ts: datetime
    sensor_id: str
    value: float

