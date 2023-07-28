FROM nikolaik/python-nodejs:python3.10-nodejs18

COPY ./requirements.txt /
WORKDIR /
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .
RUN npm install -D tailwindcss
#RUN npx tailwindcss -i ./app/jane_watson/tailwind.css -o ./app/jane_watson/static/style.css

#CMD waitress-serve --port 5000 --call jane_watson:create_app
CMD python -m jane_watson
