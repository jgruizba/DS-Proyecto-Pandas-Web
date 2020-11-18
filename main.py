from flask import Flask, render_template, url_for, redirect, request
import data
import pandas as pd

app = Flask(__name__)

df = data.get_data("www.datos.gov.co", "gt2j-8ykr", 300)
indf = data.normalize(df)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html',tables=[df.to_html(classes='data', header='true')], titles=df.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
