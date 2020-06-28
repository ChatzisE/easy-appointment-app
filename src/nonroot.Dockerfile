# Use an existing docker image as a base
FROM python:3.7-buster

#Change working directory
WORKDIR /app

# COPY requirements.txt
COPY ./requirements.txt ./

# Copy main.py file
COPY ./easy-appointment-app/src/app ./



# set user:group
RUN groupadd appuser && \
    useradd -g appuser -d /app -M appuser
# change permission on workdir
RUN chown -R appuser:appuser /app

USER appuser:appuser
ENV PATH=$PATH:/app/.local/bin
RUN pip install -r requirements.txt
EXPOSE 8000
# Tell what to do when it starts as a container
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
