import os
import sys
import logging

from datetime import timedelta, datetime
import faust

from data_model import Signal
from shared_functions.resampling import mean

import random

INPUT_TOPIC_NAME = os.environ["INPUT_TOPIC_NAME"]
OUTPUT_TOPIC_NAME = os.environ["OUTPUT_TOPIC_NAME"]
WINDOW_SIZE = int(os.environ["WINDOW_SIZE"])  # seconds
WINDOW_TTL = 1  # seconds

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.environ["LOG_LEVEL"].upper(), logging.INFO))

app = faust.App('processing', broker=f"kafka://{os.environ['KAFKA_BOOTSTRAP_NODES']}", topic_partitions=1)

input_topic = app.topic(INPUT_TOPIC_NAME, key_type=str, value_type=Signal)
output_topic = app.topic(OUTPUT_TOPIC_NAME, key_type=str, value_type=Signal)


def window_processor(key, signals):
    sensor_id = key[0]
    ts = key[1][0]  # beginning of window interval

    values = [signal.value for signal in signals]
    result = mean(values)

    logging.debug(f"Aggregation result: {sensor_id}:{result}, ts:{ts}")
    output_topic.send_soon(key=sensor_id, value=Signal(ts=ts, sensor_id=sensor_id, value=result))


signals_table = (app.Table("signals", default=list, on_window_close=window_processor, partitions=1)
                 .tumbling(timedelta(seconds=WINDOW_SIZE), expires=timedelta(seconds=WINDOW_TTL))
                 .relative_to_field(Signal.ts)
                 )


@app.agent(input_topic)
async def process(stream):
    async for signal in stream.group_by(Signal.sensor_id):
        logging.debug(f"Received signal: {signal}")


@app.agent(input_topic)
async def collect_signals(stream):
    async for s in stream.group_by(Signal.sensor_id):
        value_list = signals_table[s.sensor_id].value()
        value_list.append(s)
        signals_table[s.sensor_id] = value_list


# @app.timer(1)
# async def produce():
#     sensor_id = "test_sensor"
#     await input_topic.send(
#         key=sensor_id,
#         value=Signal(
#             ts=datetime.now(),
#             sensor_id=sensor_id,
#             value=89)
#     )


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
