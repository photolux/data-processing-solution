from datetime import datetime
import faust


class Signal(faust.Record):
    date_time: datetime
    sensor_id: str
    value: float
