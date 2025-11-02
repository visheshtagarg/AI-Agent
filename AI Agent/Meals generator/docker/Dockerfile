FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8501 8000
RUN chmod +x docker/start.sh
ENV STREAMLIT_PORT=8501 API_PORT=8000
CMD ["/bin/sh", "docker/start.sh"]

