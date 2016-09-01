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

def line(xlist,ylist,title,xaxis,yaxis,filename):
    '''xlist, ylist, title, xaxis, yaxis'''
    trace = go.Scatter(
        x = xlist,
        y = ylist,
        mode = 'lines+markers',
        name = title
    )
    layout = dict(title = title,
              xaxis = dict(title = xaxis),
              yaxis = dict(title = yaxis),
              )
    data = [trace]
    fig = dict(data=data, layout = layout)
    py.plot(fig)
    print 'line plot complete'

def color_scatter(xlist, ylist, clist, title, xaxis, yaxis, caxis, filename):
    trace = go.Scatter(
        x = xlist,
        y = ylist,
        name = title,
        mode='markers',
        marker=dict(
            size='8',
            color = clist, #set color equal to a variable
            colorscale='Viridis',
            showscale=True,
            colorbar= dict(title = caxis)
        )
    )
    layout = dict(title = title,
              xaxis = dict(title = xaxis),
              yaxis = dict(title = yaxis),
              )
    data = [trace]
    fig = dict(data = data, layout = layout)
    py.plot(fig)
    print 'color scatter plot complete'

