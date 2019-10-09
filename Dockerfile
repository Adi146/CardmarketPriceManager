FROM python:3.7-alpine

ADD ./config.yaml /config/config.yaml
ADD . /CardmarketPriceManager
WORKDIR /CardmarketPriceManager

RUN pip install -r requirements.txt

RUN echo "0 0 * * * /CardmarketPriceManager/main.py --config /config/config.yaml" | crontab -

CMD /usr/sbin/crond -f -l 8
