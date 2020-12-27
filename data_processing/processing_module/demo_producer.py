import os
import random
from datetime import datetime
import faust

from data_model import Signal


INPUT_TOPIC_NAME = os.environ["INPUT_TOPIC_NAME"]


app = faust.App('processing', broker=f"kafka://{os.environ['KAFKA_BOOTSTRAP_NODES']}", topic_partitions=1)

input_topic = app.topic(INPUT_TOPIC_NAME, key_type=str, value_type=Signal)


@app.timer(1)
async def produce():
    sensor_id = "some_sensor"
    signal = Signal(ts=datetime.now(), sensor_id=sensor_id, value=1024 + random.random())
    print(f"DEBUG Sending signal: {signal}")
    await input_topic.send(key=sensor_id, value=signal)


if __name__ == '__main__':
    app.main()
