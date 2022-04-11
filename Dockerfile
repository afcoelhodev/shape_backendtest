FROM python:latest

# Setup all python related enviroment
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get install -y python python3-pip python-dev postgresql-client
RUN pip install psycopg2-binary


# Set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN apt-get -y update && apt-get -y autoremove

CMD ["./start.sh"]
