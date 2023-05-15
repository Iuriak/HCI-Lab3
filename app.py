import dash
from dash import Dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

# 读取csv文件
df = pd.read_csv(
    'https://raw.githubusercontent.com/Iuriak/Iuriak-HCI-Lab/main/college-salaries/degrees-that-pay-back.csv')

majors = df['Undergraduate Major'].unique()

table = dash_table.DataTable(
    data=df.to_dict('records'),  # 将 DataFrame 转换成字典列表，每个字典代表表格的一行数据。
    sort_action='native',  # 使用本地的排序方式
    columns=[{'name': i, 'id': i} for i in df.columns],  # 通过一个列表推导式生成了一个包含字典元素的列表，每个字典包含列名和列 id。
    # 设置表头的背景颜色
    style_header={
        'backgroundColor': 'rgb(30,120,180)',
        'color': 'white',
        'fontWeight': 'bold'
    },
    # 设置表格中除了表头之外的所有行的背景颜色
    style_data_conditional=[{
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(235, 245, 255)'
    }],
    style_cell={  # 设置单元格的样式
        'width': 'auto',
        # 'maxWidth': '70px',
        # 'overflow': 'hidden', 内容超出单元格宽度的部分进行裁剪，不显示出来
        # 'textOverflow': 'ellipsis', 内容被裁剪后，以省略号 ... 的形式进行展示
        'whiteSpace': 'pre-wrap',
        'height': 'auto',
        'padding': '10px',
        'font-size': '14px',
        'text-align': 'center',
        'color': 'black',
        'border-right': '5px solid white'
    },
    page_size=15,  # 每页展示的行数
)

app.layout = html.Div([
    # 顶部文字设置
    html.Div([
        html.Div([
            html.H1([
                'Where it Pays to Attend College'
            ], style={'color': 'white',
                      'padding': '20px',
                      'margin': '0',  # 移除 margin 属性
                      'box-sizing': 'border-box'}),
            html.H4([
                'Salaries by college, region, and academic major',
            ], style={'color': 'rgb(195, 195, 195)',
                      'padding': '20px',
                      'margin': '0',  # 移除 margin 属性
                      'box-sizing': 'border-box'}),
        ], style={'backgroundColor': 'rgb(30,120,180)', 'margin': '0', 'box-sizing': 'border-box'}),

        html.Div([
            html.Div([
                html.Div([
                    html.H4([
                        # 'Salary Increase By Major',
                        html.A('Salary Increase By Major',
                               href='https://www.wsj.com/public/resources/documents/info-Degrees_that_Pay_you_Back-sort.html',
                               target='_blank',  # 链接所指向的页面将会在新的窗口或标签页中打开
                               style={'color': 'rgb(63, 146, 246)',
                                      'font-size': '22px',
                                      })  # 'text-decoration': 'none' 不添加下划线
                    ]),
                    html.P(
                        "Your parents might have worried when you chose Philosophy or International Relations as a major. "
                        "But a year-long survey of 1.2 million people with only a bachelor's degree by PayScale Inc. "
                        "shows that graduates in these subjects earned 103.5% and 97.8% more, respectively, "
                        "about 10 years post-commencement. Majors that didn't show as much salary growth "
                        "include Nursing and Information Technology.")
                ], style={'width': '70%', 'display': 'inline-block', 'padding': '20px'}),
            ], style={'flex': '1'}),
            html.Div([
                html.Img(
                    src='https://th.bing.com/th/id/R.bf05a104e02bdd2033872c0c5d00d219?rik=W6Pylb85OhmYeA&pid=ImgRaw&r=0',
                    style={'width': '80%', 'height': '80%', 'float': 'center', 'padding': '20px'})
            ], style={'flex': '1', 'max-width': '40%'}),
        ], style={'display': 'flex'}),  # 'margin-left': '10px', 'margin-top': '10px', 'margin-bottom': '20px',
    ], style={}),
    # 下拉多选框
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='major-dropdown',
                options=[{'label': major, 'value': major} for major in majors],
                value=[majors[0], majors[1]],
                multi=True,
                style={'margin-top': '5px', 'margin-bottom': '5px'}
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),
    ], style={
        # 'borderTop': 'thin lightgrey solid',
        'backgroundColor': 'rgb(235, 245, 255)',
        'padding': '10px 5px'
    }),
    # 三张图表设置
    html.Div([
        dcc.Graph(
            id='crossfilter-salary-scatter',
            hoverData={'points': [{'x': 'Accounting'}]}  # majors[0]
        ),
        html.Div([
            dcc.Slider(
                id='crossfilter-year--slider',
                min=1,
                max=4,
                marks={
                    1: {'label': '10th', 'style': {'font-weight': 'bold'}},
                    2: {'label': '25th', 'style': {'font-weight': 'bold'}},
                    3: {'label': '75th', 'style': {'font-weight': 'bold'}},
                    4: {'label': '90th', 'style': {'font-weight': 'bold'}}
                },
                value=1
            ),
        ], style={'padding': '0px 20px 20px 20px'}),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '10 20'}),
    html.Div([
        dcc.Graph(id='major-line-plot'),
        html.Div([
            dcc.Graph(id='crossfilter-change-scatter'),
            dcc.RadioItems(id='graph-mode-radio',
                           options=[{'label': mode, 'value': mode} for mode in {'stack', 'group'}],
                           value='stack',
                           style={
                               # 'borderBottom': 'thin lightgrey solid',
                               'backgroundColor': 'rgb(235, 245, 255)',
                               'padding': '5px 5px',
                               'max-width': '20%',
                               'margin-left': '50px'
                           }, )  # 设置一个graph mode切换按键，inline水平排列
        ]),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '10 20'}),

    html.Div([
        html.H4(['Salary Increase By Major',
                 ], style={'color': 'rgb(63, 146, 246)',
                           'font-size': '22px', }),
        table
    ], style={'width': '99%',
              'display': 'inline-block',
              # 'padding': '40 40',
              'margin-top': '20px', 'margin-bottom': '20px',
              'margin-left': '10px', 'margin-right': '40px',
              }),

    html.H4([
        'Created by 2152354 Karry',
    ], style={'borderTop': 'thin lightgrey solid',
              'color': 'rgb(0, 108, 180)',
              'font-size': '22px',
              'text-align': 'center',  # 居中对齐
              'padding': '20px 0px 0px 0px'}),

    html.Div([
        html.Div([
            html.Img(
                src='https://pngimg.com/uploads/github/github_PNG40.png',
                style={'height': 30}),
            html.Div([
                html.A('Contact me with Github!',
                       href='https://github.com/Iuriak',
                       target='_blank',
                       style={'color': 'black',
                              'font-size': '20px',
                              'text-align': 'center'})
            ], style={'display': 'flex',
                      'align-items': 'center',
                      'padding-left': '20px'})
        ], style={'display': 'flex',
                  'justify-content': 'center',
                  'align-items': 'center',
                  'max-width': '500px',
                  'margin': 'auto',
                  })
    ], style={'margin-bottom': '40px',})
])


@app.callback(
    dash.dependencies.Output('crossfilter-salary-scatter', 'figure'),
    [dash.dependencies.Input('major-dropdown', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(selected_majors, selected_year):
    dff = df[df['Undergraduate Major'].isin(selected_majors)]
    if selected_year == 1:
        dff = dff[['Undergraduate Major', 'Mid-Career 10th Percentile Salary']]
        y_label = 'Mid-Career 10th Percentile Salary'
    elif selected_year == 2:
        dff = dff[['Undergraduate Major', 'Mid-Career 25th Percentile Salary']]
        y_label = 'Mid-Career 25th Percentile Salary'
    elif selected_year == 3:
        dff = dff[['Undergraduate Major', 'Mid-Career 75th Percentile Salary']]
        y_label = 'Mid-Career 75th Percentile Salary'
    else:
        dff = dff[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']]
        y_label = 'Mid-Career 90th Percentile Salary'
    data = {
        'x': dff['Undergraduate Major'],
        'y': dff[y_label],
        'type': 'bar'
    }
    layout = {
        'height': 600,
        'title': f'{y_label} by Undergraduate Major'
    }
    return {'data': [data], 'layout': layout}


@app.callback(
    dash.dependencies.Output('crossfilter-change-scatter', 'figure'),
    dash.dependencies.Input('major-dropdown', 'value'),
    dash.dependencies.Input('graph-mode-radio', 'value')
)
def update_change_graph(selected_majors, barmode):
    dff = df[df['Undergraduate Major'].isin(selected_majors)]
    change = pd.DataFrame({
        "Major": dff['Undergraduate Major'],
        "Starting": dff['Starting Median Salary'],
        "Mid-Career": dff['Mid-Career Median Salary'],
        "Change": dff['Percent change from Starting to Mid-Career Salary']
    })

    data = [
        {
            'x': change['Major'],
            'y': change['Starting'],
            'name': 'Starting',
            'type': 'bar',
            'marker': {'color': 'rgb(158,202,225)'},
            'showlegend': True,
        },
        {
            'x': change['Major'],
            'y': change['Mid-Career'],
            'name': 'Mid-Career',
            'type': 'bar',
            'marker': {'color': 'rgb(58,200,225)'},
            'showlegend': True,
        },
        {
            'x': change['Major'],
            'y': change['Change'],
            'name': 'Percent Change(%)',
            'mode': 'lines+markers',
            'line': {'color': 'rgb(0,128,184)', 'dash': 'dash'},
            'hoverinfo': 'none',
            'showlegend': False,
            'xaxis': 'x',
            'yaxis': 'y2',
        },
        {
            'x': change['Major'],
            'y': change['Change'],
            'mode': 'text',
            'text': change['Change'],
            'textposition': 'bottom',
            'hoverinfo': 'text',
            'textfont': {'color': 'rgb(0,128,184)'},
            'showlegend': False,
            'xaxis': 'x',
            'yaxis': 'y2',
        }
    ]

    layout = {
        'height': 350,
        'title': 'Salary changes from Starting to Mid-Career',
        'barmode': barmode,
        'xaxis': {'title': 'Major'},
        'yaxis': {'title': 'Salary', 'side': 'right'},
        'yaxis2': {'title': 'Percent Change (%)', 'overlaying': 'y', 'side': 'left', 'range': [0, 100]},
        'uniformtext_minsize': 8,  # 将所有文本的最小字号设置为8
        'uniformtext_mode': 'hide',  # 将长度超出柱子宽度的文本隐藏起来，以避免重叠。
        'legend': {'x': 1.05, 'y': 1.2, 'bgcolor': 'rgba(0,0,0,0)'}  # 将图例放置在合适位置，并使其背景透明
    }

    return {'data': data, 'layout': layout}


@app.callback(
    dash.dependencies.Output('major-line-plot', 'figure'),
    dash.dependencies.Input('crossfilter-salary-scatter', 'hoverData'))
def update_year_graph(hoverData):  # selected_majors, selected_year,
    print(hoverData)
    major = hoverData['points'][0]['x']
    print(major)
    print('\n')
    dff_major = df[df['Undergraduate Major'] == major]
    y = []
    for i in range(7):
        if i != 1 and i != 2:
            y.append(dff_major[dff_major.columns[1 + i]].values[0])

    title = f'Salary changes over the Career with undergraduate major in {major}'

    return {
        'data': [go.Scatter(
            x=['Starting', 'Mid-Career 10th', 'Mid-Career 25th', 'Mid-Career 75th', 'Mid-Career 90th'],
            y=y,  # [dff_major[dff_major.columns[1 + i]].values[0] for i in range(7) and i != 2 and i != 3],
            mode='lines+markers'
        )],
        'layout': {
            'title': title,
            'height': 350,
            'xaxis': {'title': 'Career'},
            'yaxis': {'title': 'Salary'}
        }
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)
