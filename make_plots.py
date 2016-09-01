import plotly.plotly as py
import plotly.graph_objs as go

fig = {
    'data': [{'labels': ['Residential', 'Non-Residential', 'Utility'],
              'values': [19, 26, 55],
              'type': 'pie'}],
    'layout': {'title': 'Forcasted 2014 U.S. PV Installations by Market Segment'}
     }

py.plot(fig)
print 'done'

def scatter()

fig2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'lines+markers',
    name = 'markers'
)

py.plot(fig2)
