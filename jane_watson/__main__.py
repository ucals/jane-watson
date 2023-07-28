from jane_watson import create_app

# flask --app jane_watson run --debug
app = create_app()
app.run(host='0.0.0.0', debug=True)
