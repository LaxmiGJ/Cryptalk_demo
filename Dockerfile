FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pydantic
EXPOSE 8000
CMD [&quot;uvicorn&quot;,&quot;backend:app&quot;,&quot;--host&quot;,&quot;0.0.0.0&quot;,&quot;--port&quot;,&quot;8000&quot;]
