FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
  gcc \
  python3-dev \
  cron

WORKDIR /code

COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# Copy cron file to the cron.d directory on container
COPY . .
COPY cron /etc/cron.d/cron

# Give execution access
RUN chmod 0755 /etc/cron.d/cron

# Create the log file
RUN touch /var/log/cron.log

# Run cron job on cron file
RUN crontab /etc/cron.d/cron

CMD ["cron", "-f"]