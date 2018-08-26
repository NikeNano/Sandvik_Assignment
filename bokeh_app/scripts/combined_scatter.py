import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg_clean as df


from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
                          ColumnDataSource, Panel, 
                          FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
                                  Tabs, CheckboxButtonGroup, 
                                  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def combined_scatter(df_selected=None):
    df = df_selected.copy()
    df=df.drop(["language","file"],axis=1)

    SIZES = list(range(6, 22, 3))
    COLORS = Spectral5
    N_SIZES = len(SIZES)
    N_COLORS = len(COLORS)

    # data cleanup

    df.label = df.label.astype(str)
    df.age_range = df.age_range.astype(str)
    df.dialect = df.dialect.astype(str)
    

    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]

    def create_figure():
        xs = df[x.value].values
        ys = df[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()

        kw = dict()
        if x.value in discrete:
            kw['x_range'] = sorted(set(xs))
        if y.value in discrete:
            kw['y_range'] = sorted(set(ys))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,hover,reset', **kw)
        p.xaxis.axis_label = x_title
        p.yaxis.axis_label = y_title

        if x.value in discrete:
            p.xaxis.major_label_orientation = pd.np.pi / 4

        sz = 9
        if size.value != 'None':
            if len(set(df[size.value])) > N_SIZES:
                groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
            else:
                groups = pd.Categorical(df[size.value])
            sz = [SIZES[xx] for xx in groups.codes]

        c = "#31AADE"
        if color.value != 'None':
            if len(set(df[color.value])) > N_SIZES:
                groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
            else:
                groups = pd.Categorical(df[color.value])
            c = [COLORS[xx] for xx in groups.codes]

        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

        return p


    def update(attr, old, new):
        layout.children[1] = create_figure()


    x = Select(title='X-Axis', value='meanfun', options=columns)
    x.on_change('value', update)

    y = Select(title='Y-Axis', value='Q25', options=columns)
    y.on_change('value', update)

    size = Select(title='Size', value='None', options=['None'] + continuous)
    size.on_change('value', update)

    color = Select(title='Color', value='None', options=['None'] + ['label'])
    color.on_change('value', update)

    controls = widgetbox([x, y, color, size], width=200)
    layout = row(controls, create_figure())


    tab = Panel(child=layout, title = 'Scatter plot/Complete data explorere')
    return tab