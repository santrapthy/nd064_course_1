FROM python:3.8
COPY . /app
WORKDIR /app
EXPOSE 3111
RUN pip install -r techtrends/requirements.txt
RUN python techtrends/init_db.py
CMD [ "python", "techtrends/app.py" ]
