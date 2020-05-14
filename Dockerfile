FROM python:3.6.6-alpine3.6
WORKDIR /cam-core-api-automation
COPY . /cam-core-api-automation/
RUN chmod -Rf 777 .

# Install required packages
RUN apk add --no-cache gcc g++ linux-headers tini bash
#COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt
RUN ls -al
RUN pwd
# Container entry point
CMD ["/bin/bash", "api_run_tests.sh"]
