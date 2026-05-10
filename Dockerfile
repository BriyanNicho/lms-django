# Gunakan image Python versi stabil dan ringan
FROM python:3.11-slim

# Mencegah Python menulis file .pyc ke disk (opsional tapi disarankan)
ENV PYTHONDONTWRITEBYTECODE 1
# Memastikan output log Python langsung dikirim ke terminal
ENV PYTHONUNBUFFERED 1

# Set direktori kerja di dalam container
WORKDIR /code

# Salin requirements dan install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Salin seluruh kode proyek ke dalam container
COPY . /code/