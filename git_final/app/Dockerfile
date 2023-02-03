FROM python:3.9

WORKDIR /home/app/web

COPY req.txt .

RUN pip install -U pip && pip install -r req.txt

COPY . .

RUN chmod +x /home/app/web/entrypoint.sh

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
