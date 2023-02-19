# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt .

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app/ ./app


# # 
CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

