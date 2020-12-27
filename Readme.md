#Integrated Data Processing Solution
Simple stream processing application based on `faust` library, [Kafka](https://kafka.apache.org/) and [Zookeeper](https://zookeeper.apache.org/). `Docker Compose` is used to assemble and run its parts.  

It contains shared functions which can be used either by the stream application itself or from `.ipynb` research notebooks.


## Run
1. Go to the `data_processing` folder in the project's root
2. Run the command:
```bash
docker-compose up --build
```


##Test
Run tests from the command line
1. Go to the `tests` folder in the project's root
2. Run the command:
```bash
export PYTHONPATH="${PYTHONPATH}:../shared_functions" && python3 test_shared_functions.py
```
