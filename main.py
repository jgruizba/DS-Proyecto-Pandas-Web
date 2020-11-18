from flask import Flask, render_template, url_for, redirect, request
import data
import pandas as pd

app = Flask(__name__)

df = data.get_data("www.datos.gov.co", "gt2j-8ykr", 300)
indf = data.normalize(df)
strings = []
numbers = []
dates = []


@app.route("/", methods=["POST", "GET"])
def index():

    global vwdf, strings, numbers, date
    strings = []
    numbers = []
    dates = []

    if request.method == "POST":
       
        for key, value in request.form.items():
            if value != '':
                if key in data.STRINGS:
                    strings.append((key, [x.strip().title() for x in value.split(',')]))
                if key in data.NUMBERS:
                    nums = [int(x.strip()) for x in value.split(',')]
                    numbers.append((key, nums, ['=='] * len(nums)))
                if key in data.DATES:
                    dates.append((key, [x.strip() for x in value.split(',')]))
        
        q = []
        for s in strings:
            q.append(data.by_string(s[0], s[1]))
        for n in numbers:
            q.append(data.by_number(n[0], n[1], n[2]))
        for d in dates:
            q.append(data.by_string(d[0], d[1]))

        op = 'or' if request.form["dc"] == 'dis' else 'and'
        print(data.join_queries(q, op))

        if len(q) > 0:
            vwdf = indf.pipe(data.execute, data.join_queries(q, op)).rename(columns=dict(zip(data.COLS,data.COLS2))).fillna('')
        else:
            vwdf = indf.rename(columns=dict(zip(data.COLS,data.COLS2))).fillna('')
        
        return redirect(url_for('success', name='consulta'))
    else:
        vwdf = df

    return render_template(
        "index.html",
        tables=[vwdf.to_html(classes="data", header="true")]
    )


@app.route("/<name>", methods=["POST", "GET"])
def success(name):

    global vwdf, strings, numbers, date
    strings = []
    numbers = []
    dates = []
    if request.method == "POST":
        for key, value in request.form.items():
            if value != '':
                if key in data.STRINGS:
                    strings.append((key, [x.strip().title() for x in value.split(',')]))
                if key in data.NUMBERS:
                    nums = [int(x.strip()) for x in value.split(',')]
                    numbers.append((key, nums, ['=='] * len(nums)))
                if key in data.DATES:
                    dates.append((key, [x.strip() for x in value.split(',')]))
        
        q = []
        for s in strings:
            q.append(data.by_string(s[0], s[1]))
        for n in numbers:
            q.append(data.by_number(n[0], n[1], n[2]))
        for d in dates:
            q.append(data.by_string(d[0], d[1]))

        op = 'or' if request.form["dc"] == 'dis' else 'and'
        print(data.join_queries(q, op))

        if len(q) > 0:
            vwdf = indf.pipe(data.execute, data.join_queries(q, op)).rename(columns=dict(zip(data.COLS,data.COLS2))).fillna('')
        else:
            vwdf = indf.rename(columns=dict(zip(data.COLS,data.COLS2))).fillna('')
        
        return redirect(url_for('success', name='consulta'))

    return render_template(
        "index.html",
        tables=[vwdf.to_html(classes="data", header="true")]
    )


if __name__ == "__main__":
    app.run(debug=True)
