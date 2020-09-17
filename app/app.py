# Boilerplate from https://github.com/dradecic

import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from flask import Flask, render_template, request


indicators_table = pd.read_csv('../data/indicators.csv')

def one_variable_timeline(var_name, keyvariables):
    p = figure(plot_width=400, plot_height=250, x_axis_type="datetime")
    keyvariables['day'] = pd.to_datetime(keyvariables['day'])
    p.line(keyvariables['day'], keyvariables[var_name], color='navy', alpha=0.5)
    p.circle(keyvariables['day'], keyvariables[var_name], size=5, color='red', legend=var_name)
    return p

def redraw(indicator_name):
    key_chart = one_variable_timeline(indicator_name,indicators_table)
    return (
        key_chart
    )

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chart():
    indicators_list = indicators_table.columns
    selected_indicator = request.form.get('dropdown-select')

    if selected_indicator == 0 or selected_indicator == None:
        selected_indicator = indicators_list[0]
    key_chart = redraw(selected_indicator)


    script_key_chart, div_key_chart = components(key_chart)

    return render_template(
        'index.html',
        indicators_list=indicators_list,
        div_key_chart=div_key_chart,
        script_key_chart=script_key_chart,
        selected_indicator=selected_indicator
    )

if __name__ == '__main__':
    app.run(debug=True)
