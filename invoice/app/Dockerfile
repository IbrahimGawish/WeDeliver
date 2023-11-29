FROM python:3.9
EXPOSE 5004
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY test_invoice_app.py /app
CMD python -m unittest -s test_invoice_app
COPY app.py /app
CMD python app.py