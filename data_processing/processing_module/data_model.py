from faust import Record


class Signal(Record, serializer='json'):
    timestamp: int
    sensor_id: str
    value: float

