import os
from datetime import timedelta, datetime
import faust
from data_model import Signal
from shared_functions.resampling import mean

import random

INPUT_TOPIC_NAME = "input"
OUTPUT_TOPIC_NAME = "output"
WINDOW_SIZE = 5  # seconds

app = faust.App('processing', broker=f"kafka://{os.environ['KAFKA_BOOTSTRAP_NODES']}", topic_partitions=1)

input_topic = app.topic(INPUT_TOPIC_NAME, key_type=str, value_type=Signal)
output_topic = app.topic(OUTPUT_TOPIC_NAME, key_type=str, value_type=Signal)


def window_processor(key, signals):
    sensor_id = key[0]
    ts = key[1][0]  # beginning of window interval

    values = [signal.value for signal in signals]
    result = mean(values)

    print(f"DEBUG aggregation result: {sensor_id}:{result}, ts:{ts}")
    output_topic.send_soon(key=sensor_id, value=Signal(ts=ts, sensor_id=sensor_id, value=result))


signals_table = (app.Table("signals", default=list, on_window_close=window_processor, partitions=1)
                 .tumbling(WINDOW_SIZE, expires=timedelta(seconds=10))
                 #.relative_to_field(Signal.ts)
                 )


@app.agent(input_topic)
async def process(stream):
    async for signal in stream.group_by(Signal.sensor_id):
        print(f"DEBUG received signal: {signal}")


@app.agent(input_topic)
async def collect_signals(stream):
    async for s in stream.group_by(Signal.sensor_id):
        value_list = signals_table[s.sensor_id].value()
        value_list.append(s)
        signals_table[s.sensor_id] = value_list


@app.timer(1)
async def produce():
    sensor_id = "test_sensor"
    await input_topic.send(
        key=sensor_id,
        value=Signal(
            ts=datetime.now(),
            sensor_id=sensor_id,
            value=89)
    )


@app.timer(1)
async def produce():
    sensor_id = "another_sensor"
    await input_topic.send(
        key=sensor_id,
        value=Signal(
            ts=datetime.now(),
            sensor_id=sensor_id,
            value=1024 + random.random())
    )

if __name__ == '__main__':
    app.main()
