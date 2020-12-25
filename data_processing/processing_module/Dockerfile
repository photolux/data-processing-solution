FROM python:3.9
COPY shared_functions /shared_functions
COPY data_processing/processing_module/app.py /app/app.py
ENV PYTHONPATH "${PYTHONPATH}:/shared_functions"
CMD python /app/app.py