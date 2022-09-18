'''

@author:a108222015 a108222026 a108222027
@date:2022 06 07
@project:final Draw Plot

'''

import os
inPath=os.path.join("..","input")
outPath=os.path.join("..","output")

import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
from sklearn.linear_model import LinearRegression
pio.renderers.default = 'browser'

#農業進出口
def plot1():

    ex1 = pd.read_csv(inPath + '/ex1.csv')
    ex1.info()

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['year'], empty='none')

    alt.data_transformers.enable('default', max_rows=None)
    # The basic line
    lineimports = alt.Chart(ex1,title='農業進口').mark_line(interpolate='basis').encode(
        x='year:O',
        y=alt.Y('mean(imports):Q'),
        color='region:N'
    )

    lineexports = alt.Chart(ex1,title="農業出口").mark_line(interpolate='basis').encode(
        x='year:O',
        y=alt.Y('mean(exports):Q'),
        color='region:N'
    )

    selectors = alt.Chart(ex1).mark_point().encode(
        x='year:O',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    pointsim = lineimports.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    pointsex = lineexports.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    textim = lineimports.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'mean(imports):Q', alt.value(' '))
    )
    textex = lineexports.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'mean(exports):Q', alt.value(' '))
    )

    rulesim = alt.Chart(ex1).mark_rule(color='gray').encode(
        x='year:O',
    ).transform_filter(
        nearest
    )
    rulesex = alt.Chart(ex1).mark_rule(color='gray').encode(
        x='year:O',
    ).transform_filter(
        nearest
    )

    chartim = alt.layer(
        lineimports, selectors, pointsim, rulesim, textim
    ).properties()
    chartex = alt.layer(
        lineexports, selectors, pointsex, rulesex, textex
    ).properties()

    chart = alt.vconcat(chartim, chartex, spacing=30, title='農業進出口趨勢圖'
                        ).configure_title(color='blue', fontSize=30, align='center', anchor='middle'
                        ).configure_axis(labelFontSize=14, labelColor='red',
                                         titleFontSize=20, titleColor='blue')

    chart.show()
    chart.save(outPath+'/chart1.html')

#農業土地占比 依照年分畫GEO 動態圖
def plot2():

    ex2 = pd.read_csv(inPath + '/ex2.csv')
    ex2.info()

    fig = px.choropleth(ex2, locations="Country Code",
                        color="agriculturalLand",
                        hover_name="Country Name",
                        animation_frame='year',
                        animation_group='agriculturalLand',
                        range_color=[0, 100],
                        hover_data=['agriculturalGDP'],
                        color_continuous_scale=px.colors.sequential.YlGn)

    fig.update_layout(
        title={
            'text': "農業土地占比(GDP)",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font_family="Courier New",
        font_color="blue",
        title_font_color="blue",
        legend_title_font_color="green",
        font=dict(
            family="Courier New, monospace",
            size=30,
            color="RebeccaPurple"
        )
    )

    fig.show()

    fig.write_html(outPath+"/chart2.html")

#(GDP vs machinery) 農業GDP與農業機械化程度是否有關
def plot3(_port=8055):

    ex3 = pd.read_csv(inPath + '/ex3.csv')
    ex3.info()

    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider', style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.Slider(
            ex3['year'].min(),
            ex3['year'].max(),
            step=None,
            value=ex3['year'].min(),
            marks={str(year): str(year) for year in ex3['year'].unique()},
            id='year-slider'
        )
    ])

    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('year-slider', 'value'))
    def update_figure(selected_year):

        filtered_df = ex3[ex3.year == selected_year]

        re=LinearRegression()
        ref=re.fit(np.array(filtered_df['agriculturalMachinery']).reshape(-1, 1), filtered_df['aGDP'])
        pre=ref.predict(np.array(filtered_df['agriculturalMachinery']).reshape(-1, 1))


        fig = make_subplots(
            rows=2, cols=3,
            column_widths=[0.25, 0.25, 0.45],
            row_heights=[0.6, 0.6],subplot_titles=['agriculturalGDP', 'agriculturalMachinery', '農業GDP與農業機械化是否有關'],
            specs=[[{"type": "scattergeo", "rowspan": 2}, {"type": "scattergeo", "rowspan": 2}, {"type": "bar", "rowspan": 2}],
                   [None, None, None]])

        fig.add_trace(
            go.Scattergeo(locations=filtered_df['Country Code'],
                          mode="markers",
                          hoverinfo="text",
                          showlegend=False,
                          text = filtered_df['Country Name']+filtered_df['aGDP'].astype(str),
                          marker=dict(color="crimson", size=filtered_df['agriculturalGDP'], opacity=0.8),),
            row=1, col=1
        )

        fig.add_trace(
            go.Scattergeo(locations=filtered_df['Country Code'],
                          mode="markers",
                          hoverinfo="text",
                          showlegend=False,
                          text = filtered_df['Country Name']+filtered_df['agriculturalMachinery'].astype(str),
                          marker=dict(color="crimson", size=(filtered_df['agriculturalMachinery']/filtered_df['agriculturalMachinery'].quantile(.4)), opacity=0.8)),
            row=1, col=2
        )

        # fig.add_trace(
        #     go.Scatter(
        #         x=filtered_df['Country Name'],
        #         y=filtered_df['agriculturalMachinery'],
        #         mode="lines",
        #         line=go.scatter.Line(color="blue"),
        #         name='agriculturalMachinery'
        #         ),
        #     row=1, col=3
        # )
        # print(filtered_df['agriculturalGDP'])
        # fig.add_trace(
        #     go.Scatter(
        #         x=filtered_df['Country Name'],
        #         y=filtered_df['agriculturalGDP'],
        #         mode="lines",
        #         line=go.scatter.Line(color="red"),
        #         name='agriculturalGDP'),
        #     row=1, col=3
        # )

        fig.add_trace(
            go.Scatter(
                x=filtered_df['agriculturalMachinery'],
                y=filtered_df['aGDP'],
                mode="markers",
                showlegend=False,
                name='agriculturalGDP',
                hovertemplate =
                "<b>agriculturalMachinery: %{x:}</b><br><br>" +
                "agriculturalGDP:$ %{y:}<br>"),
            row=1, col=3
        )
        fig.add_trace(
            go.Scatter(x=filtered_df['agriculturalMachinery'], y=pre, mode="lines", showlegend=False,
                       marker_color="lightgreen", name='trand line'),
            row=1, col=3
        )



        fig.update_geos(
            projection_type="orthographic",
            landcolor="white",
            oceancolor="MidnightBlue",
            showocean=True,
            lakecolor="LightBlue"
        )

        # fig.update_layout(
        #     xaxis=dict(title='Country'),
        #     yaxis=dict(
        #         title='agriculturalGDP & agriculturalMachinery', zeroline=True,
        #         showline=True,
        #         side='left'
        #     )
        # )

        fig.update_layout(
                xaxis=dict(title='agriculturalMachinery'),
                yaxis=dict(
                    title='agriculturalGDP', zeroline=True,
                    showline=True)
            )

        fig.update_layout(
            template="plotly_dark",
            margin=dict(r=10, t=25, b=40, l=10),
            height=800
        )

        fig.write_html(outPath + "/chart3.html")
        return fig

    app.run_server(debug=True,port=_port)

#
def plot4(_port=8041):

    ex4 = pd.read_csv(inPath + '/ex4_new.csv')
    ex4.info()
    
    year_date=ex4['year'].unique()#所有的日期    
    app = Dash()
    
    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider', style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.Slider(
                min=year_date.min(),max=year_date.max(),step=1,
                value=year_date.min(), id='my-range-slider', marks={str(year): str(year) for year in year_date})
      
    ])
    
     
    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('my-range-slider', 'value'))#year
    def update_figure(year): 
        filter0=ex4
        ff=np.where((filter0['year']==year ))
        filter1=ex4.loc[ff]
        fig = px.scatter(filter1, x='agriculturalLand', y='agriculturalMachinery', color='region',
                       title="AgriculturalLand vs AgriculturalMachinery", trendline="ols"
        ).update_layout(title_text='AgriculturalLand vs AgriculturalMachinery', title_x=0.5)
        fig.write_html(outPath + "/chart4.html")
        return fig
       
    app.run_server(port=_port,debug=True)

#淡水 vs 耕地 vs 食物生產指數 vs 農業GDP
def plot5(_port=8055):
 
    ex5 = pd.read_csv(inPath + '/ex5.csv')
    ex5.info()         
    c_data=ex5['region'].unique()
    #print(ex5['year'].unique())
    year_date=ex5['year'].unique()#所有的日期    
        
    app = Dash()
    
    app.layout = html.Div([
      html.Div([
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label':rr, 'value':rr} for rr in list(c_data)],
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),  
        html.Iframe(
        id='plot',
        height='600',
        width='2000',
        sandbox='allow-scripts',

        # This is where we will pass the html
        # srcDoc=

        # Get rid of the border box
        style={'border-width': '0px'}
    ),
        dcc.RangeSlider(min=year_date.min(),max=year_date.max(),step=1,
                value=[year_date.min(), year_date.max()], id='my-range-slider', marks={str(year): str(year) for year in year_date})
      
    ])
    @app.callback(
        Output('plot', 'srcDoc'),
        Input('my-range-slider', 'value'),#year
        Input('name-dropdown', 'value'))#year
    def update_figure(year,country): 
        filter0=ex5
        ff=np.where((filter0['year']>=year[0])&(filter0['year']<year[1]))
        filter1=ex5.loc[ff]        
        ff1=filter1.where(country==filter1['region'],inplace=False)
        filter2=ff1
        selector = alt.selection_single(empty='all', fields=['Country Name'])
        alt.data_transformers.enable('default', max_rows=None)
        
        
        
        base = alt.Chart(filter2).properties(
            width=450,
            height=450
        ).add_selection(selector)    
        
        points = base.mark_point(filled=True, size=200 ).encode(
            x='foodProductionIndex:Q',
            y='aGDP:Q',           
            tooltip=['Country Name', 'region', 'foodProductionIndex', 'aGDP','year'],
            color=alt.condition(selector, 'Country Name:N', alt.value('lightgray'), legend=None),
        )
        
        water = base.mark_point(filled=True, size=200).encode(
            x='aGDP:Q',
            y='annualFreshwater:Q',
            tooltip=['Country Name', 'region', 'annualFreshwater', 'aGDP','year'],
            color=alt.Color('Country Name:N', legend=None)
        ).transform_filter(selector)
        
        land = base.mark_point(filled=True, size=200).encode(
             x='aGDP:Q',
            y='AgriculturalLand:Q',
            tooltip=['Country Name', 'region', 'AgriculturalLand', 'aGDP','year'],
           color=alt.Color('Country Name:N', legend=None)
        ).transform_filter(selector)
            
        chart = alt.hconcat(points.properties(title='所選年份中糧食生產和農業產量(GDP)的關係'),
                            water.properties(title="所選年份中淡水面積(billion cubic meters)和農業產量(GDP)的關係"),
                            land.properties(title="所選年份中耕種面積和農業產量(GDP)的關係"), spacing=50, title="農業種植面積和淡水是否會影響不同地區的農業產量(GDP)"). configure_title(color='green', fontSize=24, align="center",anchor="middle"
                                          ).configure_axis(labelFontSize=14,
                                                           labelColor="red",
                                                           titleFontSize=20,
                                                           titleColor="blue") 
        chart.save(outPath+'/chart5.html')
        return chart.to_html()
    app.run_server(port=_port,debug=True)

def plot6():
    # GDP (current US$)
    # Agriculture value added (% of GDP)
    # Population, total
    ex6 = pd.read_csv(inPath + '/ex6.csv')
    ex6.info()

    alt.data_transformers.disable_max_rows()
    chart1 = alt.Chart().mark_point(filled=True, size=15, opacity=0.5).encode(
        alt.X(alt.repeat('column'), type='quantitative'),
        alt.Y(alt.repeat('row'), type='quantitative'),      
        color="Country Name:N"
    ).properties(
        width=150,
        height=150,
    ).repeat(
        data=ex6,
        row=['population', 'GDP', 'agriculturalGDP'],
        column=['agriculturalGDP', 'GDP', 'population'],
    )
    chart=alt.hconcat(chart1,title='GDP vs Agriculture value vs Population'
                      ).configure_axis(
                                labelColor='purple',
                                titleColor='green',
                                gridColor="cyan"
                                )
    
    chart.show()
    chart.save(outPath+'/chart6.html')
    # 中下:GDP高的國家多半不依靠農業
    # 中右:人口總數確實和GDP呈現正相關
    # 右下:以農業為主要進口的國家 人口還是會有一定的數量
    
def plot7(_port=8050):

    ex7 = pd.read_csv(inPath + '/ex7.csv')

    year_date=ex7['year'].unique()#所有的日期    
        
    app = Dash()
    
    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider', style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.Slider(
                min=year_date.min(),max=year_date.max(),step=1,
                value=year_date.min(), id='my-range-slider', marks={str(year): str(year) for year in year_date})
      
    ])
    
     
    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('my-range-slider', 'value'))#year
    def update_figure(year): 
        filter0=ex7
        ff=np.where((filter0['year']==year ))
        filter1=ex7.loc[ff]
        fig = px.scatter_geo(
            filter1,
            locations='Country Code',       
            color=  'landUnderCerealProduction', # which column to use to set the color of markers
            #title="Land under cereal production (hectares) vs Arable land (hectares per person)",
            hover_name="Country Name", 
            size= 'arableLand', 
            projection="natural earth"
        ).update_layout(title_text='Land under cereal production (hectares) vs Arable land (hectares per person)', title_x=0.5)
        fig.write_html(outPath + "/chart7.html")
        return fig
       
    app.run_server(port=_port,debug=True)

#
def plot8():
    #https://dash.plotly.com/basic-callbacks
    # ex8 = pd.read_csv(inPath + '/ex8.csv')
    app = Dash(__name__)
    
    df = pd.read_csv(inPath + "/ex8_melt.csv")
    df.info()
    
    
    app.layout = html.Div([
        html.Div([
    
            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Agricultural raw materials imports (% of merchandise imports)',
                    id='xaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='xaxis-type',
                    inline=True
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
    
            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Agricultural raw materials exports (% of merchandise exports)',
                    id='yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='yaxis-type',
                    inline=True
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
    
        dcc.Graph(id='indicator-graphic'),
    
        dcc.Slider(
            df['Year'].min(),
            df['Year'].max(),
            step=None,
            id='year--slider',
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
    
        )
    ])
    
    
    @app.callback(
        Output('indicator-graphic', 'figure'),
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('year--slider', 'value'))
    def update_graph(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type,
                     year_value):
        dff = df[df['Year'] == year_value]
    
        fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                         y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                         hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                         title="import vs explore vs grosssaving vs nature resource")
    
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    
        fig.update_xaxes(title=xaxis_column_name,
                         type='linear' if xaxis_type == 'Linear' else 'log')
    
        fig.update_yaxes(title=yaxis_column_name,
                         type='linear' if yaxis_type == 'Linear' else 'log')
        
        fig.update_layout(
            template="plotly_dark",
            title={'text': "import vs explore vs grosssaving vs nature resource",
                   'y':0.95,
                   'x':0.5},
            height=800
        )
        fig.write_html(outPath + "/chart8.html")
        return fig
    
    app.run_server(debug=True,port=8051)
#化肥消耗量 vs 糧食生產指數
def plot9(_port=8050):
    ex9 = pd.read_csv(inPath + '/ex9.csv')
    ex9.info()
    datemmin=0
    datemax=0
    
    region_data = ex9['region'].unique()
    country_data=ex9['Country Name'].unique()
    year_date=ex9['year'].unique()#所有的日期    
        
    app = Dash()
    
    app.layout = html.Div(
        [     
            html.Div([
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label':rr, 'value':rr} for rr in list(region_data)],
                #value = region_data[0], 
                multi=True,#list(fnameDict.keys())[0]
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),
            
            ###############################################################################
            html.Div([
                dcc.Dropdown(
                id='opt-dropdown', multi=True
                ), 
               ]
             ,style={'width': '20%', 'display': 'inline-block'}),
            
            
             html.Div(id='output-container-range-slider'),
            ###############################################################################
         
            
       
          html.Div([
        dcc.Graph(id='graph-with-slider', style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.RangeSlider(
                min=year_date.min(),max=year_date.max(),step=1,
                value=[year_date.min(), year_date.max()], id='my-range-slider', marks={str(year): str(year) for year in year_date})
      
    ])]        
    )
    
    
    #收地區資料
    @app.callback(
        Output('opt-dropdown', 'options'),
        Input('name-dropdown', 'value')   #dropdown value -->option
    )
    def update_date_dropdown(name):
        #the region u had been selected
        rr=ex9[ex9['region'].isin(name)]
        rr=rr['Country Name'].unique()#選擇的國家   
        return [{'label': i, 'value': i} for i in list(rr)]
    
    
    @app.callback(
        Output('output-container-range-slider', 'children'),
        Input('my-range-slider', 'value')
    )
    def update_output(value):
        return '選擇的年代： .format{}'.format(value)
        #date changed
    #收國家資料
    @app.callback(
        Output('opt-dropdown', 'value'),
        Output('name-dropdown', 'value'), 
        Input('opt-dropdown', 'options'),
        Input('name-dropdown', 'value')
        )
    def callback(value,cc):
        return None,cc

    @app.callback(
        #dash.dependencies.Output('output-container-range-slider', 'children'),
        Output('graph-with-slider', 'figure'),
        Input('name-dropdown', 'value'),#region
        Input('opt-dropdown', 'value'),#country
        Input('my-range-slider', 'value'))#year
    
    def update_figure(region,country,year): 
       filter0=ex9    
       ff=np.where((filter0['year']>=year[0])&(filter0['year']<year[1]))
       filter1=ex9.loc[ff]
       #filter2=filter1
       if  country!=None:#!=None:
           filter2=filter1[filter1['Country Name'].isin(country)]
           fig = px.scatter(filter2, x="fertilizerConsumption", y="cropProduction",color='Country Name',trendline="ols").update_layout(title_text='國家：每100公頃的施肥量(%)vs穀物收成量', title_x=0.5)
       else:
           #filter1=filter1[filter1['region'].isin(region)]
           filter2=filter1[filter1['region'].isin(region)]
           fig = px.scatter(filter2, x="fertilizerConsumption", y="cropProduction",color='region',trendline="ols").update_layout(title_text='區域：每100公頃的施肥量(%)vs穀物收成量', title_x=0.5)
       fig.write_html(outPath + "/chart9.html")
       return fig
   
    app.run_server(port=_port )

#農業男女 vs 農業GDP
def plot10():
    ex10 = pd.read_csv(inPath + '/ex10.csv')
    ex10.info()

    re = LinearRegression()
    ref = re.fit(np.array(ex10['totalpop']).reshape(-1, 1), ex10['agriculturalGDP'])
    pre = ref.predict(np.array(ex10['totalpop']).reshape(-1, 1))
    ex10['pre'] = pre

    alt.data_transformers.enable('default', max_rows=None)

    dropdown_options = ex10['region'].drop_duplicates().tolist()

    dropdown = alt.binding_select(options=[None] + dropdown_options, labels=['ALL'], name='region ')

    selection = alt.selection_single(fields=['region'], bind=dropdown, name='Select')

    slider = alt.binding_range(min=ex10['year'].min(), max=ex10['year'].max(), step=1)
    select_year = alt.selection_single(name='year', bind=slider, init={'year': ex10['year'].max()})

    base = alt.Chart(ex10).add_selection(select_year).properties(width=250)

    left = base.encode(
        y=alt.Y('agriculturalGDP:Q', axis=None, stack=None, bin=True),
        x=alt.X('sum(female):Q',
                sort=alt.SortOrder('descending'), scale=alt.Scale(domainMax=1500)),
        color=alt.condition(selection, alt.Color('region:N'), alt.value('lightgray')),
    ).mark_bar(opacity=0.8).properties(title='Female', width=300, height=600)

    middle = base.encode(
        y=alt.Y('agriculturalGDP:Q', axis=None, stack=None, bin=True),
        text=alt.Text('mean(agriculturalGDP):Q'),
    ).mark_text().properties(width=20, title='agriculturalGDP', height=600)

    right = base.encode(
        y=alt.Y('agriculturalGDP:Q', axis=None, stack=None, bin=True),
        x=alt.X('sum(male):Q', scale=alt.Scale(domainMax=1500)),
        color=alt.condition(selection, alt.Color('region:N'), alt.value('lightgray')),
    ).mark_bar(opacity=0.8).properties(title='Male', width=300, height=600)

    fig = alt.concat(left, middle, right)

    point = alt.Chart(ex10, title='農業人口與GDP關聯').mark_point().encode(
        alt.X('totalpop:Q', scale=alt.Scale(domain=(0, 200))),
        alt.Y('mean(agriculturalGDP):Q', scale=alt.Scale(domain=(0, 100))),
        color=alt.condition(selection, alt.Color('region:N'), alt.value('lightgray')),
        tooltip=['Country Name', 'agriculturalGDP', "totalpop", 'year']
    ).properties(width=650, height=600)

    line = alt.Chart(ex10).mark_line().encode(
        alt.X('totalpop:Q', scale=alt.Scale(domain=(0, 200))),
        alt.Y('pre:Q', scale=alt.Scale(domain=(0, 100))),
        color=alt.condition(selection, alt.Color('region:N'), alt.value('lightgray'))
    ).properties(width=650, height=600).interactive()

    plot = alt.layer(point, line)

    chart = alt.hconcat(fig, plot, spacing=30, title='農業男女 vs 農業GDP 關係'
                        ).configure_title(color='blue', fontSize=30, align='center', anchor='middle'
                                          ).configure_axis(labelFontSize=14, labelColor='red',
                                                           titleFontSize=20, titleColor='blue'
                                                           ).add_selection(selection).transform_filter(selection
                                                                                                       ).transform_filter(
        select_year)
    chart.show()
    chart.save(outPath + '/chart10.html')

if __name__ == '__main__':
    #1.2.3.10/4.6.8/5.7.9
    # plot1() #altair
    # plot2() #plotly
    # plot3(8002)  #dash
    # plot4()      #dash
    # plot5(8003)  #dash
    # plot6() #altair
    # plot7(8004)  #dash
    # plot8()  #dash
    # plot9(8082)  #dash
    plot10() #altair