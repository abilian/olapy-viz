# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import sys
from os.path import isdir

import os

import numpy as np
from bokeh.core.properties import value
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import dodge
from flask import Blueprint, jsonify, current_app
from olapy.core.mdx.executor.execute import MdxEngine
from flask import request
from pathlib import Path
from werkzeug.utils import secure_filename
from bokeh.plotting import figure
from bokeh.embed import components

API = Blueprint('api', __name__, template_folder='templates')
api = API.route


def allowed_file(filename):
    file_extension = Path(filename).suffix
    return file_extension in ['.csv']


def clean_upload_dir(upload_path):
    if isdir(upload_path):
        for the_file in os.listdir(upload_path):
            file_path = os.path.join(upload_path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.makedirs(upload_path)


@api('/cubes/add', methods=['POST'])
def add_cube():
    # todo savegarder plusieurs cubes
    olapy_data_dir = os.path.join(current_app.instance_path, 'olapy-data', 'cubes', 'user_cube')
    clean_upload_dir(olapy_data_dir)

    for uploaded_file in request.files.getlist('files'):
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(olapy_data_dir, filename))
    # if import one file, consider it as facts table
    if len(request.files.getlist('files')) == 1:
        fact_table_name = os.path.splitext(request.files.getlist('files')[0].filename)[0]
    else:
        fact_table_name = 'Facts'
    executor = MdxEngine(olapy_data_location=os.path.join(current_app.instance_path, 'olapy-data', 'cubes'),
                         source_type='csv', cubes_folder='')

    try:
        executor.load_cube('user_cube', fact_table_name=fact_table_name)
        return jsonify([{str(column): str(type)} for column, type in executor.star_schema_dataframe.dtypes.items()])
        # return jsonify(executor.star_schema_dataframe.dtypes.to_dict())
    except:
        return jsonify({})


def datetime(x):
    return np.array(x, dtype=np.datetime64)


def _line_plot(df, x_axis, plot_size, y_axis, plot_legend, line_style, fill_color, x_axis_label,
               y_axis_label, y_axis_location, **kwargs):
    plot = figure(title=plot_legend, y_axis_location=y_axis_location,
                  x_axis_type="datetime", plot_height=350, plot_width=1200)
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.axis_label = x_axis_label if x_axis_label else x_axis[0]
    plot.yaxis.axis_label = y_axis_label if y_axis_label else y_axis[0]
    # plot.yaxis.axis_label = y_axis[0]
    # grouped_df = executor.star_schema_dataframe.groupby(x_axis)[y_axis].sum()
    groupped_df = df.groupby(x_axis)[y_axis].sum()
    for measure in y_axis:
        plot.line(list(groupped_df.index.values), df[measure].tolist(), color=fill_color[measure], line_width=plot_size,
                  legend=measure, line_dash=line_style)
    # plot.multi_line([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]], line_width=plot_size, legend=plot_legend,
    #                 line_dash=line_style)
    # plot.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='GOOG')
    # plot.legend.location = "top_left"

    return components(plot, wrap_script=False)


def _vbar_plot(df, x_axis, y_axis, plot_size, fill_color, line_style, x_axis_label,
               y_axis_label, y_axis_location, **kwargs):
    # grouped_df = executor.star_schema_dataframe.groupby(x_axis)[y_axis].sum()

    if y_axis:
        measures = y_axis
        groupped_df = df.groupby(x_axis)[measures].sum()
    else:
        measures = [df.columns[0]]
        groupped_df = df.groupby(x_axis)[measures].count()

    source = ColumnDataSource(groupped_df)
    columns = source.data[x_axis[0]].tolist()
    plot = figure(x_range=columns, y_axis_location=y_axis_location, plot_height=350, plot_width=1200)
    # fill_alpha, fill_color, js_event_callbacks, js_property_callbacks, line_alpha, line_cap, line_color,
    # line_dash, line_dash_offset, line_join, line_width, name, subscribed_events, tags, top, width or x
    data_offset = -0.2
    # if y_axis:
    for measure in measures:
        plot.vbar(x=dodge(x_axis[0], data_offset, range=plot.x_range), top=measure, width=plot_size / 100,
                  source=source, color=fill_color.get(measure, '#5ab2dd'), legend=value(measure),
                  line_dash=line_style.lower())
        data_offset += 0.2
    # else:
    #     # color=fill_color[x_axis[0]]
    #     plot.vbar(x=dodge(x_axis[0], data_offset, range=plot.x_range), width=plot_size / 100,
    #               source=source, legend=value(x_axis[0]), line_dash=line_style,top=x_axis[0])
    plot.x_range.range_padding = 0.1
    plot.xgrid.grid_line_color = None
    plot.legend.location = "top_right"
    plot.legend.orientation = "horizontal"
    try:
        plot.xaxis.axis_label = x_axis_label if x_axis_label else x_axis[0]
    except:
        plot.xaxis.axis_label = ''

    try:
        plot.yaxis.axis_label = y_axis_label if y_axis_label else y_axis[0]
    except:
        plot.yaxis.axis_label = ''

    return components(plot, wrap_script=False)


def _hex_plot(df, x_axis, y_axis, plot_size, fill_color, plot_legend, line_style, x_axis_label,
              y_axis_label, y_axis_location, size_elements=None, color_elements=None):
    if color_elements:
        colors = [fill_color[x] for x in df[color_elements[0]].tolist()]
    else:
        colors = list(fill_color.values())[0]

    if size_elements:
        sizes = [(size / len(df[size_elements[0]].tolist())) * 10 * plot_size for size in df[size_elements[0]].tolist()]
    else:
        sizes = plot_size - 2

    plot = figure(title=plot_legend, y_axis_location=y_axis_location, match_aspect=True,
                  tools="wheel_zoom,reset", background_fill_color='#440154', plot_height=350, plot_width=1200)

    plot.grid.visible = False
    plot.xaxis.axis_label = x_axis_label if x_axis_label else x_axis[0]
    plot.yaxis.axis_label = y_axis_label if y_axis_label else y_axis[0]

    r, bins = plot.hexbin(df[x_axis[0]], df[y_axis[0]], size=0.5, hover_color="pink", hover_alpha=0.8)

    plot.circle(df[x_axis[0]], df[y_axis[0]], fill_color=colors, color=colors, fill_alpha=0.2, size=sizes,
                line_width=1, line_dash=line_style)

    plot.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))

    return components(plot, wrap_script=False)


def _circle_plot(df, x_axis, y_axis, plot_size, fill_color, plot_legend, line_style, x_axis_label,
                 y_axis_label, y_axis_location, color_elements=None, size_elements=None):
    plot = figure(title=plot_legend, y_axis_location=y_axis_location, plot_height=350, plot_width=1200)
    # angle, angle_units, fill_alpha, fill_color, js_event_callbacks, js_property_callbacks, line_alpha,
    # line_cap, line_color, line_dash, line_dash_offset, line_join, line_width, name, radius, radius_dimension,
    # radius_units, size, subscribed_events, tags, x or y
    plot.xaxis.axis_label = x_axis_label if x_axis_label else x_axis[0]
    plot.yaxis.axis_label = y_axis_label if y_axis_label else y_axis[0]

    if color_elements:
        colors = [fill_color[x] for x in df[color_elements[0]].tolist()]
    else:
        colors = list(fill_color.values())[0]

    if size_elements:
        sizes = [(size / len(df[size_elements[0]].tolist())) * 10 * plot_size for size in df[size_elements[0]].tolist()]
    else:
        sizes = plot_size

    plot.circle(df[x_axis[0]], df[y_axis[0]], fill_color=colors, color=colors, fill_alpha=0.2, size=sizes,
                line_width=1, line_dash=line_style, )

    return components(plot, wrap_script=False)


@api("/get_unique_rows", methods=['POST'])
def unique_rows():
    columns = request.get_json().get('column')
    executor = MdxEngine(olapy_data_location=os.path.join(current_app.instance_path, 'olapy-data'))
    fact_table_name = get_fact_name(os.path.join(current_app.instance_path, 'olapy-data'))
    executor.load_cube('user_cube', fact_table_name=fact_table_name)
    selected_colors_column = list(columns[0].keys())
    return jsonify(list(set(executor.star_schema_dataframe[selected_colors_column[0]])))


def auto_plot_type(df, x_axis, y_axis, plot_size, plot_legend, line_style, fill_color, color_elements,
                   size_elements, x_axis_label, y_axis_label, y_axis_location, **kwargs):
    """
    If no plot_type is passed, auto guess type and generate chart.
    :param df:
    :param x_axis:
    :param y_axis:
    :param plot_size:
    :param plot_legend:
    :param line_style:
    :param fill_color:
    :param color_elements:
    :param x_axis_label:
    :param y_axis_label:
    :param y_axis_location:
    :return:
    """
    current_module = sys.modules[__name__]
    plot = {'div': None, 'script': None}
    for chart_type_test in ['vbar', 'circle', 'line', 'hex']:
        try:
            script, div = getattr(current_module, '_' + chart_type_test + '_plot')(df=df,
                                                                                   x_axis=x_axis,
                                                                                   y_axis=y_axis,
                                                                                   plot_size=plot_size,
                                                                                   plot_legend=plot_legend,
                                                                                   line_style=line_style,
                                                                                   fill_color=fill_color,
                                                                                   color_elements=color_elements,
                                                                                   size_elements=size_elements,
                                                                                   x_axis_label=x_axis_label,
                                                                                   y_axis_label=y_axis_label,
                                                                                   y_axis_location=y_axis_location)
            plot['div'] = div
            plot['script'] = script
            return plot
        except:
            pass
    return plot


def generate_plot(chart_type, df, x_axis, y_axis, plot_size, plot_legend, line_style, fill_color, color_elements,
                  size_elements, x_axis_label, y_axis_label, y_axis_location, **kwargs):
    current_module = sys.modules[__name__]
    if chart_type:
        script, div = getattr(current_module, '_' + chart_type + '_plot')(df=df,
                                                                          x_axis=x_axis,
                                                                          y_axis=y_axis,
                                                                          plot_size=plot_size,
                                                                          plot_legend=plot_legend,
                                                                          line_style=line_style,
                                                                          fill_color=fill_color,
                                                                          color_elements=color_elements,
                                                                          size_elements=size_elements,
                                                                          x_axis_label=x_axis_label,
                                                                          y_axis_label=y_axis_label,
                                                                          y_axis_location=y_axis_location)
        plot = {'div': div, 'script': script}

    else:
        # if no plot_type is passed, auto guess type and generate chart
        plot = auto_plot_type(df=df,
                              x_axis=x_axis,
                              y_axis=y_axis,
                              plot_size=plot_size,
                              plot_legend=plot_legend,
                              line_style=line_style,
                              fill_color=fill_color,
                              color_elements=color_elements,
                              size_elements=size_elements,
                              x_axis_label=x_axis_label,
                              y_axis_label=y_axis_label,
                              y_axis_location=y_axis_location)
    return plot


def get_fact_name(olapy_data_path):
    """
    # todo temporary until we use db with cubes
    # todo remove this
    :param olapy_data_path:
    :return:
    """
    user_cube_files = os.listdir(os.path.join(olapy_data_path, 'cubes', 'user_cube'))

    if len(user_cube_files) == 1:
        facts_table_name = os.path.splitext(user_cube_files[0])[0]
    else:
        facts_table_name = 'Facts'
    return facts_table_name


@api("/get-plot", methods=['GET', 'POST'])
def get_plot():
    # todo in percent
    if request.method == 'POST':
        request_data = request.get_json()
        x_axis = [list(x.keys())[0] for x in request_data.get('X_axis')]
        y_axis = [list(y.keys())[0] for y in request_data.get('Y_axis')]
        color_elements = [list(colors.keys())[0] for colors in request_data.get('ColorByColumn')]
        size_elements = [list(size.keys())[0] for size in request_data.get('SizeByColumn')]
        plot_size = request_data.get('circleSize')
        fill_color = request_data.get('pickedColor', {})
        plot_legend = request_data.get('plotLegend', '')
        chart_type = request_data.get('chartType', None)
        line_style = request_data.get('lineStyle', 'solid')
        x_axis_label = request_data.get('x_axis_label', '')
        y_axis_label = request_data.get('y_axis_label', '')
        y_axis_location = request_data.get('YAxisLocation', 'left')
        executor = MdxEngine(olapy_data_location=os.path.join(current_app.instance_path, 'olapy-data'))

        # todo temporary until we use db with cubes
        # todo remove this
        fact_table_name = get_fact_name(os.path.join(current_app.instance_path, 'olapy-data'))
        executor.load_cube('user_cube', fact_table_name=fact_table_name)
        df = executor.star_schema_dataframe

        plot = generate_plot(chart_type=chart_type, df=df,
                             x_axis=x_axis,
                             y_axis=y_axis,
                             plot_size=plot_size,
                             plot_legend=plot_legend,
                             line_style=line_style,
                             fill_color=fill_color,
                             color_elements=color_elements,
                             size_elements=size_elements,
                             x_axis_label=x_axis_label,
                             y_axis_label=y_axis_label,
                             y_axis_location=y_axis_location)

        return jsonify(plot)

    return jsonify({'div': None, 'script': None})
    # # todo clean all this
    # plot = figure(plot_height=350, plot_width=1200,
    #               title='title',
    #               y_axis_location='left',
    #               y_axis_label='lalble',
    #               )
    # plot.circle([1, 2], [3, 4], color="#1d8b24")
    # script, div = components(plot, wrap_script=False)
    # return jsonify({'div': div, 'script': script})
