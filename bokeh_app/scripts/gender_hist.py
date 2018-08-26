import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
                          ColumnDataSource, Panel, 
                          FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
                                  Tabs, CheckboxButtonGroup, 
                                  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def gender_hist(df_selected):
    
    def make_dataset(gender_list, range_start = 0.076070, range_end = 0.271264, bin_width = 0.00001):

        by_gender_group = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                           'f_proportion', 'f_interval',
                                           'name', 'color'])
        range_extent = range_end - range_start
 
        # Iterate through all the carriers
        for i, gender_group in enumerate(gender_list):
            # Subset to the carrier
            subset = df_selected[df_selected['label'] == gender_group]
            # Create a histogram with 5 minute bins
            arr_hist, edges = np.histogram(subset['meanfun'], 
                               bins = int(range_extent/bin_width),
                               range = [range_start, range_end])

            # Divide the counts by the total to get a proportion
            arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:] })

            # Format the proportion 
            arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%0.5f to %0.5f KHz' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
            # Assign the carrier for labels
            arr_df['name'] = gender_group

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            by_gender_group = by_gender_group.append(arr_df)

        # Overall dataframe
        by_gender_group = by_gender_group.sort_values(['name', 'left'])

        return ColumnDataSource(by_gender_group)
    
    def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p
    
    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700, 
                  title = 'Gender and Mean Fundamental Frequency',
                  x_axis_label = 'Mean fundamental frequency (KHz)', y_axis_label = 'Proportion')

        # Quad glyphs to create a histogram
        p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
               color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'black')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Gender', '@name'), 
                                    ('Meanfund frequency', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                          mode='vline')

        p.add_tools(hover)

        # Styling
        p = style(p)

        return p
    
    def update(attr, old, new):
        gender_group_to_plot = [gender_group_selection.labels[i] for i in gender_group_selection.active]
        
        new_src = make_dataset(gender_group_to_plot,
                               range_start = range_select.value[0],
                               range_end = range_select.value[1],
                               bin_width = binwidth_select.value)

        src.data.update(new_src.data)

    # This is the option on the side

    available_gender_groups = list(df_selected['label'].unique())
    gender_group_selection = CheckboxGroup(labels=available_gender_groups, active = [0, 1])
    # What happens when you select it 
    gender_group_selection.on_change('active', update)
    
    # The slider on the side
    binwidth_select = Slider(start = 0.001, end = 0.01, 
                         step = 0.001, value = 0.001,
                         title = 'Frequency Width (KHz)')
    #Something is updated
    binwidth_select.on_change('value', update)
    
    #The slider and the ranges for that one
    range_select = RangeSlider(start = 0.076070 ,end = 0.271264, value = (0.076070, 0.271264),
                               step = 0.01, title = 'Meanfun Frequency (KHz)')
    # Same here 
    range_select.on_change('value', update)
    
    
    
    initial_age_grop = [gender_group_selection.labels[i] for i in gender_group_selection.active]
    
    src = make_dataset(initial_age_grop,
                      range_start = range_select.value[0],
                      range_end = range_select.value[1],
                      bin_width = binwidth_select.value)
    
    p = make_plot(src)
    
    # Put controls in a single element
    controls = WidgetBox(gender_group_selection, binwidth_select, range_select)
    
    # Create a row layout
    layout = row(controls, p)
    
    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'Gender Fundamental Frequency')
    return tab
