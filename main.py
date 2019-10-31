import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64
import webbrowser as wb
import plotly.plotly as py
from PIL import Image
from base64 import decodestring
import numpy as np
import os
import urllib
import finaltryfit

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js",
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    },

    {
        'href': 'https://fonts.googleapis.com/css?family=Varela',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }

    
]


app = dash.Dash(__name__,meta_tags=[
    {
        'name': 'description',
        'content': 'My description'
    },
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    }
],
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets,
                static_folder='assets')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.title = 'RunTimeTerror'
app.config['suppress_callback_exceptions']=True



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

PLOTLY_LOGO = "/"



app.config['suppress_callback_exceptions']=True


page_1_layout = html.Div([

        dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/keras-logo-small-wb-1.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("RunTimeTerror", className="ml-4")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            
            dbc.NavbarToggler(id="navbar-toggler"),
           
        ],
        color="dark",      
        dark=True,
        sticky="top",
    ),


    
     html.Div([    
     html.Div([


        html.Div([ 
       dbc.Card(
            [
                dbc.CardHeader("AI-PUNE \u2b50"),
                dbc.CardBody(
                    [
                           
            html.Div([
            html.H5('Choose Image 	\ud83d\uddc3\ufe0f'),
            dcc.Upload(
                    id='upload-data',
                    children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
            ,' 	\ud83d\udcc1'
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin-bottom':'100%',
                        'margin': '1%'
                    },
                    # Allow multiple files to be uploaded
                   accept='image/*'
                )],className="ten columns offset-by-one")  ]), ]
        ),],style={ 'margin-top':'3%'}),   


         html.Div(id='output-image',style={"margin-top":"10px","margin-":"10px"}),


    ],className='ten columns offset-by-one'),
     ]),

])






@app.callback(Output('output-image', 'children'),
              [Input('upload-data','contents')],
              [State('upload-data', 'filename')])
def update_graph_interactive_image(content,new_filename):


  
    if (content is not None):
      
       
        string = content.split(';base64,')[-1]
        imgdata = base64.b64decode(string)
        new_filename=new_filename.split(".")[0]
        filename = 'image/'+new_filename+'.png'
        filename1 = 'image/'+new_filename+'.jpeg' # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        with open(filename1, 'wb') as f:
            f.write(imgdata)

        #image = Image.fromstring('RGB',(200,200),decodestring(string))

            


       # Do You processing here ----------------




        # Manipulate here

        finaltryfit.mains(new_filename)








       ##################################



        string=''
        with open("output/im_rec.png", "rb") as imageFile:
            string=base64.b64encode(imageFile.read()).decode("utf-8")

        img1=''
        with open("output/output11.png", "rb") as imageFile:
            img1=base64.b64encode(imageFile.read()).decode("utf-8")
       
        
        originalcard=html.Div([
        dbc.Card(
    [
        dbc.CardBody(
            [dbc.CardTitle(new_filename)]
        ),
        dbc.CardImg(
            src=(
                'data:image/png;base64,{}'.format(string)
            )
        ),
         dbc.CardBody(
            [
                dbc.CardText(
                   html.P("Image with geometrical coordinates")
                ),
            ]
        ),
    ],
    style={"max-width": "250px"},
),
],className="twelve columns")
        

        VariableOne=dbc.Card(
    [
        dbc.CardBody(
            [dbc.CardTitle("Processed Image")]
        ),
        dbc.CardImg(
            src=(
                'data:image/jpg;base64,{}'.format(img1)
            )
        ),
         dbc.CardBody(
            [
                dbc.CardText(
                   "Masked Image"
                ),
            ]
        ),
    ],
    style={"max-width": "250px"},
)


        return [


            html.Div([

                 dbc.Card(
            [
                dbc.CardHeader("Input Image \u2b50"),
                dbc.CardBody(
                    [   html.Div([



                        html.Div([
                        originalcard],className="five columns offset-by-four"),

                        ],className='row'




                                 ),
                    ]
                ),
            ]
        )

                ],className="twelve columns"),



             html.Div([

                 dbc.Card(
            [
                dbc.CardHeader("Output Image \u2b50"),
                dbc.CardBody(
                    [   html.Div([



                        html.Div([
                        VariableOne],className="five columns offset-by-four"),

                        ],className='row'




                                 ),
                    ]
                ),
            ]
        )

                ],className="twelve columns",style={ 'margin-bottom':'3%'})


            ]

           
    else:
        return []




# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_1_layout
    else:
        return []
    # You could also return a 404 "URL not found" page here

wb.open('http://127.0.0.1:8050/')
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True,host ='0.0.0.0',use_reloader=True)

