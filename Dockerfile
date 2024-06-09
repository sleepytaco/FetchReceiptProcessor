FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install poetry

# Install required dependencies through poetry
RUN poetry install

# Flask API serves on port 5000
EXPOSE 8888

# Run the application through poetry
CMD ["poetry", "run", "python", "api.py"]