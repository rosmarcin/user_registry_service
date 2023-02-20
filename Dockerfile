# Dockerfile

FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY user_profile_app/ /code/user_profile_app/
COPY user_registry/ /code/user_registry/
# COPY templates/ /code/templates/
# COPY admin.json /code/
COPY manage.py /code/
# COPY setup_prod.sh /code/
# #WORKDIR /code/sales-prediction-aws-lambda
# COPY sales-prediction-aws-lambda/ /code/sales-prediction-aws-lambda/
# ENV PYTHONPATH "${PYTHONPATH}/code/sales-prediction-aws-lambda/sales_prediction"
# RUN pip install -r /code/sales-prediction-aws-lambda/sales_prediction/requirements.txt