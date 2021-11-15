import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from datetime import datetime             #to manipulate dates
import plotly.express as px               #to create interactive charts
from dash import dcc        #to get components for interactive user interfaces
from dash import html       #to compose the dash layout using Python structures
from dash.dependencies import Input, Output, State
import datetime
from dash import dash_table
import dash
import calendar
import random
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

location_database = pd.read_csv('data_file.csv')
species_df = pd.read_csv('species.csv')
database = pd.read_csv("db_test_final.csv")


database['occurrence_time'] = pd.to_datetime(database['occurrence_time'])
database['location'] = database['thanhpho_huyen'] + ', ' + database['tinh_thanhphotrunguong']
vn_name = []
for i in range(len(database)):
    vn_name.append(species_df[species_df['species_name'] == database.iloc[i, 5]]['VN_name'])
database['VN_name'] = vn_name

display_location = location_database[location_database['location'].isin(database['location'])]

# declare first date in the df
first_day_df = pd.to_datetime(database['occurrence_time']).min()
first_day_date = first_day_df.strftime("%d")
first_day_month = first_day_df.strftime("%m")
first_day_year = first_day_df.strftime("%Y")
first_day_df = first_day_df.strftime("%Y-%m-%d")

# declare today
today_date = datetime.datetime.now().strftime("%d").zfill(2)
today_month = datetime.datetime.now().strftime("%m").zfill(2)
today_month_EN = datetime.datetime.now().strftime("%B")
today_year = datetime.datetime.now().strftime("%Y")

district = database['tinh_thanhphotrunguong'].unique()
district_list = []
for i in district:
    if str(i) != 'nan':
        try:
            district_list.append(i.split('Tỉnh ')[1])
        except:
            district_list.append(i.split('Thành phố ')[1])

def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def display_map(location_database):
    px.set_mapbox_access_token('pk.eyJ1IjoibGFtbGVvMDMwOCIsImEiOiJja3Z5bmlxMm85YXJ6MzBxcG82cm5ndTZjIn0.dKy0r5isHevflHEBb5REyQ')

    fig = px.scatter_mapbox(
        location_database,
        lat=location_database.lat,
        lon=location_database.lon,
        hover_name = "location",
        zoom=4,
        mapbox_style = 'mapbox://styles/mapbox/streets-v11'
    )

    fig.update_layout(height=int(800))
    return fig

def create_plot_for_cases(df):
    case_df = df.copy()
    case_df['year_month'] = pd.to_datetime(df['occurrence_time']).dt.strftime('%Y-%m')  
    
    case_df.drop_duplicates(['occurrence_time', 'tinh_thanhphotrunguong', 'category_broad'], inplace=True)
    case_df = case_df.groupby(['year_month']).count().reset_index()
    
    case_df['Số vi phạm'] = case_df['sci_name']
    case_df['Tháng'] = case_df['year_month']
    fig = px.line(case_df, x='Tháng', y='Số vi phạm')
    
    return fig

# Generate some in-memory data.
geobuf = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=i, lon=j) for i,j in zip(display_location['lat'], display_location['lon'])]))
# district_area = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=29.015, lon=-118.271)]))

# Create example app.
app.layout = html.Div([

    html.Div([
        html.Div([
            html.H1([
                "Wildlife Tracfficking Vietnam"
            ], style={'display': 'inline-block'}),

            html.P(f"Hotline miễn phí bảo vệ ĐVHD: 1800-1522", style={'display': 'inline-block', 'float':'right'}),

        ]),
        

        html.Div([
            html.Div("Từ ngày", 
                        style={'width': '100%', 
                            'height':'50%',
                            'display': 'block',
                        }),

            html.Div([
                dcc.Dropdown(
                    id="start-date-search",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=first_day_date,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-month-search",
                    options=[{"label": 'January'  , "value": '01'},
                                {"label": 'February' , "value": '02'},
                                {"label": 'March'    , "value": '03'},
                                {"label": 'April'    , "value": '04'},
                                {"label": 'May'      , "value": '05'},
                                {"label": 'June'     , "value": '06'},
                                {"label": 'July'     , "value": '07'},
                                {"label": 'August'   , "value": '08'},
                                {"label": 'September', "value": '09'},
                                {"label": 'October'  , "value": '10'},
                                {"label": 'November' , "value": '11'},
                                {"label": 'December' , "value": '12'}],
                    value=first_day_month,
                    clearable=False
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-year-search",
                    options=[{"label": i  , "value": i} for i in range(int(first_day_year), datetime.datetime.now().year+1)],
                    value=first_day_year,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'}),
        ], style={'width': '20%', 'display': 'inline-block', 'float':'left'}),
        # ----------
        
        html.Div([
            html.Div("Đến ngày", 
                            style={'width': '100%', 
                                'height':'50%',
                                'display': 'block',
                            }),
            html.Div([
                dcc.Dropdown(
                    id="end-date-search",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=today_date,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="end-month-search",
                    options=[{"label": 'January'  , "value": '01'},
                                {"label": 'February' , "value": '02'},
                                {"label": 'March'    , "value": '03'},
                                {"label": 'April'    , "value": '04'},
                                {"label": 'May'      , "value": '05'},
                                {"label": 'June'     , "value": '06'},
                                {"label": 'July'     , "value": '07'},
                                {"label": 'August'   , "value": '08'},
                                {"label": 'September', "value": '09'},
                                {"label": 'October'  , "value": '10'},
                                {"label": 'November' , "value": '11'},
                                {"label": 'December' , "value": '12'}],
                    value=today_month,
                    clearable=False
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Dropdown(
                    id="end-year-search",
                    options=[{"label": i  , "value": i} for i in range(int(first_day_year), datetime.datetime.now().year+1)],
                    value=today_year,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'})
        ], style={'width': '20%', 'display': 'inline-block', 'float':'left'}),
        # ---------             

        # html.Div([
            html.Div([
                html.Div("Tỉnh / Thành phố", 
                        style={
                            'width': '100%', 
                            'height':'50%',
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="search-district-filter",
                    value='All',
                    options=[{"label": i, "value": i} for i in district_list] + [{"label": "Tất cả", "value": "All"}],
                    
                    clearable=False
                ),
            ], style={'width': '15%', 'display': 'inline-block', 'float':'left'}),

            html.Div([
                html.Div("Nhóm loài động vật", 
                        style={
                            'width': '100%', 
                            'height':'50%',
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="search-big-group-filter",
                    value='All',
                    options=[
                        {"label": 'Hổ', "value": "Tigers"}, 
                        {"label": 'Linh trưởng', "value": "Primates"}, 
                        {"label": 'Tê tê', "value": "Pangolins"}, 
                        {"label": 'Gấu', "value": "Bears"}, 
                        {"label": 'Sừng tê giác', "value": "Rhinos"}, 
                        {"label": 'Ngà voi', "value": "Elephants"}, 
                        {"label": 'Thú rừng', "value": "Others"}, 
                        {"label": 'Chim', "value": "Birds"}, 
                        {"label": 'Rùa', "value": "Turtles"}, 
                        {"label": 'Họ Mèo', "value": "Feliformia"}, 
                    ] + [{"label": "Tất cả", "value": "All"}],
                    clearable=False
                ),
            ], style={'width': '10%', 'display': 'inline-block', 'float':'left'}),

            html.Div([
                
                html.Div("Loại hành vi phạm tội", 
                        style={
                            'width': '100%', 
                            'height':'50%',
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="search-category-filter",
                    value='All',
                    options=[
                        {"label": 'Tàng trữ', "value": "Storing"}, 
                        {"label": 'Buôn bán', "value": "Trading"}, 
                        {"label": 'Quảng cáo', "value": "Advertising"}, 
                        {"label": 'Tiêu thụ', "value": "Consumpsion"}, 
                    ] + [{"label": "Tất cả", "value": "All"}],

                    clearable=False
                ),
            ], style={'width': '15%', 'display': 'inline-block', 'float':'left'}),  

            html.Div([
                dcc.RadioItems(
                    id='online-offline',
                    options=[
                        {'label': 'Offline', 'value': 'offline'},
                        {'label': 'Online', 'value': 'online'},
                        {'label': 'Cả hai', 'value': 'both'}
                    ],
                    value='both',
                    # labelStyle={'display': 'inline-block', "float":"right"}
                ),
            ], style={'width': '10%', 'display': 'inline-block'})

        # ]),
    ]),


    
    dl.Map(center=[21.0304271810001, 105.801469498], zoom=5, children=[
        dl.TileLayer(),
        # dl.GeoJSON(url='/data/gis/01.json', id="states",
        #            hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),),
        dl.GeoJSON(data=geobuf, format="geobuf", id="locations"), 
        
    ], style={'width': '50%', 'height': '80vh', 'margin': "auto", "display": "inline-block"}, id="map"),

    
    html.Div([
        html.Div(id='total', style={'display':'block', 'height':'50vh'}),
        
        html.Div(id="detail")

    ], style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block", 'float':'right'}), 

    dash_table.DataTable(
                            id='cases',
                            data=database.to_dict('records'),
                            # columns=[{"name": i, "id": i} for i in database.columns[1:-1]],
                            columns=[
                                {
                                    "name": "Ngày", 
                                    "id": "occurrence_time"
                                },
                                
                                {
                                    "name": "Tỉnh",
                                    "id": "tinh_thanhphotrunguong",
                                    
                                },
                                {
                                    "name": "Thành phố",
                                    "id": "thanhpho_huyen",
                                    
                                },
                                {
                                    "name": "Danh pháp khoa học", 
                                    "id": "sci_name"
                                },
                                {
                                    "name": "Tên loài", 
                                    "id": "VN_name"
                                },
                                
                                {
                                    "name": "Số lượng",
                                    "id": "num_animal",
                                    
                                },
                                {
                                    "name": "Tang vật",
                                    "id": "object",
                                    
                                },
                                {
                                    "name": "Số lượng",
                                    "id": "volumn",
                                    
                                },
                                {
                                    "name": "Online/Offline",
                                    "id": "online_offline",
                                    
                                },
                                {
                                    "name": "Hành vi phạm tội",
                                    "id": "category_broad",
                                    
                                }
                            ],
                            export_format='xlsx',
                            export_headers='display',
                            merge_duplicate_headers=True,
                            fixed_rows={'headers': True},
                            style_table={'height': 400},
                            style_cell={
                                'minWidth': 80, 'maxWidth': 250, 'width': 95
                            }
                       ),

        html.P("@Axolotl 2021")

    
])


@app.callback(Output("detail", "children"), [Input("locations", "click_feature")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked"

# update map
@app.callback(
    Output("locations", "data"), 
    [Input("start-date-search", "value"), 
     Input("start-month-search", "value"),
     Input("start-year-search", "value"), 
     Input("end-date-search", "value"),
     Input("end-month-search", "value"), 
     Input("end-year-search", "value"),
     Input("search-district-filter", "value"),
     Input("search-big-group-filter", "value"),
     Input("search-category-filter", "value"),
     Input("online-offline", "value")]
)
def display_daily_expenses(start_date, start_month, start_year,
                           end_date, end_month, end_year,
                           district,
                           big_group,
                           category,
                           on_off):
    
    filter_df = database.copy()
    filter_df['occurrence_time'] = pd.to_datetime(filter_df['occurrence_time'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    filter_df = filter_df[(filter_df['occurrence_time'] >= start_day) & (filter_df['occurrence_time'] <= end_day)]
    
    filter_df['occurrence_time'] = filter_df['occurrence_time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    if district != "All":
        if district in ['Hà Nội', 'Hồ Chí Minh']:
            district = 'Thành phố ' + district
        else:
            district = 'Tỉnh ' + district

        filter_df = filter_df[filter_df['tinh_thanhphotrunguong'] == district]
        
    if big_group != "All":
        filter_df = filter_df[filter_df['sci_name'].isin(species_df[species_df['big_category']==big_group]['species_name'])]
        
    if category != "All":
        filter_df = filter_df[filter_df['category_broad'] == category]

    if on_off != 'both':
        filter_df = filter_df[filter_df['online_offline'] == on_off]

    display_location = location_database[location_database['location'].isin(filter_df['location'])]
    return dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=i+random.random(), lon=j+random.random()) for i,j in zip(display_location['lat'], display_location['lon'])]))



# update cases table
@app.callback(
    Output("cases", "data"), 
    [Input("start-date-search", "value"), 
     Input("start-month-search", "value"),
     Input("start-year-search", "value"), 
     Input("end-date-search", "value"),
     Input("end-month-search", "value"), 
     Input("end-year-search", "value"),
     Input("search-district-filter", "value"),
     Input("search-big-group-filter", "value"),
     Input("search-category-filter", "value"),
     Input("online-offline", "value")]
)
def table(start_date, start_month, start_year,
        end_date, end_month, end_year,
        district,
        big_group,
        category,
        on_off):
    
    filter_df = database.copy()
    filter_df['occurrence_time'] = pd.to_datetime(filter_df['occurrence_time'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    filter_df = filter_df[(filter_df['occurrence_time'] >= start_day) & (filter_df['occurrence_time'] <= end_day)]
    
    filter_df['occurrence_time'] = filter_df['occurrence_time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    if district != "All":
        if district in ['Hà Nội', 'Hồ Chí Minh']:
            district = 'Thành phố ' + district
        else:
            district = 'Tỉnh ' + district

        filter_df = filter_df[filter_df['tinh_thanhphotrunguong'] == district]
        
    if big_group != "All":
        filter_df = filter_df[filter_df['sci_name'].isin(species_df[species_df['big_category']==big_group]['species_name'])]
       
        
    if category != "All":
        filter_df = filter_df[filter_df['category_broad'] == category]

    if on_off != 'both':
        filter_df = filter_df[filter_df['online_offline'] == on_off]

    return filter_df.to_dict('records')

@app.callback(
    Output("total", "children"), 
    [Input("start-date-search", "value"), 
     Input("start-month-search", "value"),
     Input("start-year-search", "value"), 
     Input("end-date-search", "value"),
     Input("end-month-search", "value"), 
     Input("end-year-search", "value"),
     Input("search-district-filter", "value"),
     Input("search-big-group-filter", "value"),
     Input("search-category-filter", "value"),
     Input("online-offline", "value")]
)
def table(start_date, start_month, start_year,
        end_date, end_month, end_year,
        district,
        big_group,
        category,
        on_off):
    
    filter_df = database.copy()
    filter_df['occurrence_time'] = pd.to_datetime(filter_df['occurrence_time'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    filter_df = filter_df[(filter_df['occurrence_time'] >= start_day) & (filter_df['occurrence_time'] <= end_day)]
    
    filter_df['occurrence_time'] = filter_df['occurrence_time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    if district != "All":
        if district in ['Hà Nội', 'Hồ Chí Minh']:
            district = 'Thành phố ' + district
        else:
            district = 'Tỉnh ' + district

        filter_df = filter_df[filter_df['tinh_thanhphotrunguong'] == district]
        
    if big_group != "All":
        filter_df = filter_df[filter_df['sci_name'].isin(species_df[species_df['big_category']==big_group]['species_name'])]
       
        
    if category != "All":
        filter_df = filter_df[filter_df['category_broad'] == category]

    if on_off != 'both':
        filter_df = filter_df[filter_df['online_offline'] == on_off]

    drop_dup = filter_df.drop_duplicates(['occurrence_time', 'tinh_thanhphotrunguong', 'category_broad'])
    first_date = pd.to_datetime(filter_df['occurrence_time'].min()).strftime('%d/%m/%Y') 
    last_date = pd.to_datetime(filter_df['occurrence_time'].max()).strftime('%d/%m/%Y') 
    return [
        html.H4(f"Tổng số vi phạm trong giai đoạn {first_date} - {last_date}: {len(drop_dup)}"),
        dcc.Graph(figure=create_plot_for_cases(filter_df))
    ]


app.run_server()