from datetime import datetime
from faust import Record


class Signal(Record, isodates=True, serializer='json'):
    ts: datetime
    sensor_id: str
    value: float

