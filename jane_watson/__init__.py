import os
import pandas as pd

from flask import Flask, render_template, request
from jane_watson.db import kbai
from markdown import markdown


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='L3q)ewK+7"al0G`Oz(2.RF.XcGBVl^P0Q|#^U?BR[1hkx2[m3jjpl{At@',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    data = list(kbai.find({}))
    df = pd.DataFrame(data)
    modules = df['module'].unique()

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html', modules=modules)

    @app.route('/<int:module_number>')
    def module(module_number):
        module_name = modules[module_number - 1]
        x = df[df['module'] == module_name]
        content = ""
        for idx, row in x.iterrows():
            content = f"{content}## {row['class'].replace('_', ':')}\n\n{row['summary']}\n\n\n"

        return render_template(
            'module.html',
            modules=modules,
            module_name=module_name,
            content=markdown(content)
        )

    @app.route('/search')
    def search():
        q = request.args.get('q')
        a = db.answer(q)
        for item in a['top_results']:
            item['summary'] = markdown(item['summary'])

        return render_template(
            'search.html',
            modules=modules,
            question=q,
            answer=a['answer'],
            top_results=a['top_results'],
            module_url=a['module_url']
        )

    return app
