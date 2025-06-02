FROM python:3.10-slim

#Add source files
WORKDIR /app
COPY . .
COPY static/ ./static/
COPY requirements.txt .

#Install requirements
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python", "app.py"]
