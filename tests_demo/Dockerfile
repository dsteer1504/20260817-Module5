FROM python:3.12-slim
WORKDIR  /app
COPY Clean_Customers.py /app
RUN pip install pandas
ENTRYPOINT ["python3", "Clean_Customers.py"]
