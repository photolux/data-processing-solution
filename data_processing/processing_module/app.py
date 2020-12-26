import os
import faust
from data_model import Signal
from shared_functions.resampling import resample

print("DEBUG Starting processing module...")


app = faust.App('processing', broker=f"kafka://{os.environ['KAFKA_BOOTSTRAP_URL']}")
input_topic = app.topic('input', key_type=str, value_type=Signal)


@app.agent(input_topic)
async def process(signals):
    async for signal in signals:
        print(f"DEBUG received signal: {signal}")


if __name__ == '__main__':
    app.main()
