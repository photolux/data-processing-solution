FROM python:3.9

COPY data_processing/processing_module/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY shared_functions /shared_functions
COPY data_processing/processing_module/data_model.py /app/
COPY data_processing/processing_module/app.py /app/
COPY data_processing/processing_module/wait-for-it.sh /

ENV PYTHONPATH "${PYTHONPATH}:/shared_functions:/app"

#CMD "bash" "-c" "/wait-for-it.sh $KAFKA_BOOTSTRAP_URL -- python /app/app.py worker -l debug"
CMD "bash" "-c" "/wait-for-it.sh $KAFKA_BOOTSTRAP_URL -- python /app/app.py worker"