FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    wget \
    unzip \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create working directories
RUN mkdir -p /work /out /opt/tools
WORKDIR /work

COPY requirements.txt /work/
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts /work/scripts
COPY app /work/app
RUN chmod +x /work/scripts/download_tools.sh /work/scripts/run_jadx.sh /work/scripts/run_apktool.sh

# Download tools (apkid installed via pip)
RUN /work/scripts/download_tools.sh /opt/tools

ENTRYPOINT ["/work/app/entrypoint.sh"]
