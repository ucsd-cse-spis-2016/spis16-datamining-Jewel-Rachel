import plotly.plotly as py
import plotly.graph_objs as go

def pie_chart(labels, values, title):
    fig = {
        'data': [{'labels': labels,
                  'values': values,
                  'type': 'pie'}],
        'layout': {'title': title}
         }
    py.plot(fig)
    print 'pie complete'

def line(xlist,ylist,title,xaxis,yaxis)
    '''xlist, ylist, title, xaxis, yaxis'''
    plot = go.Scatter(
        x = xlist,
        y = ylist,
        mode = 'lines+markers',
        name = title
    )
    layout = dict(title = title,
              xaxis = dict(title = xaxis),
              yaxis = dict(title = yaxis),
              )
    fit = dict(data=plot, layout=layout)
    py.plot(fig)
    print 'line complete'
