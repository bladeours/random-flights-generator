FROM python

ENV ROWS=5
ENV IP_DISTANCE=http://localhost:8081
ENV IP_FLIGHT=http://localhost:8082
COPY requirements.txt .
COPY generator.py .
COPY airports_codes.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "-u", "generator.py", "-e" ]