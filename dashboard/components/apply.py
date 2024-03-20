import plotly.express as px

def apply_updates(fig):
    # Atualizando as propriedades dos traços
    fig.update_traces(
        #textfont=dict(color="white"),
        #insidetextfont=dict(color="white"),
        hoverlabel=dict(font=dict(color="white")),
        marker_line_width=0
    )

    # Atualizando o layout
    fig.update_layout(
        title='',
        plot_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        paper_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''),
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font=dict(color="white")),
        font=dict(color="white")
    )

    # Atualizando os eixos x
    fig.update_xaxes(
        showgrid=True, 
        gridcolor='rgba(200,200,200,0.2)', 
        zeroline=False, 
        title_text='',
        nticks=5,
        tickangle=0,
    )

    return fig