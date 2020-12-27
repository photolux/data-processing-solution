# Integrated Data Processing Solution
Simple stream processing application with micro-batch processing based on [Faust](https://github.com/robinhood/faust), [Kafka](https://kafka.apache.org/) and [Zookeeper](https://zookeeper.apache.org/). `Docker Compose` is used to assemble and run its parts.  

## Run
1. Go to the `data_processing` folder in the project's root
2. Run the command:
```bash
docker-compose up --build
```

## Test
Run tests from the command line
1. Go to the `tests` folder in the project's root
2. Run the command:
```bash
export PYTHONPATH="${PYTHONPATH}:../shared_functions" && python3 test_shared_functions.py
```
