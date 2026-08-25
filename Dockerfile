FROM apache/airflow:3.0.0

USER airflow

RUN pip install --upgrade pip

# Cài đặt đầy đủ danh sách thư viện của đệ vào Image
RUN pip install --no-cache-dir \
    --use-deprecated=legacy-resolver \
    apache-airflow-providers-postgres \
    minio \
    pandas \
    pyarrow \
    requests \
    python-dotenv \
    psycopg2-binary \
    "dbt-postgres>=1.8.0,<1.9.0"