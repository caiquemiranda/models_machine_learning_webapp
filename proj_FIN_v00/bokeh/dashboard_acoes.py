import yfinance as yf
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from datetime import datetime

# Lista de ações para análise
acoes = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Obtendo os dados históricos das ações
dados_acoes = yf.download(acoes, start='2022-01-01', end='2023-01-01')

# Criando a fonte de dados para o gráfico
source = ColumnDataSource(dados_acoes['Close'])

# Criando o gráfico de linha para cada ação
p = figure(x_axis_type='datetime', title='Preço de Fechamento das Ações', width=800, height=400)
for acao in acoes:
    p.line(x='Date', y=acao, source=source, line_width=2, legend_label=acao)

# Adicionando as ferramentas de interação
hover = HoverTool()
hover.tooltips = [("Data", "@Date{%F}"), ("Preço de Fechamento", "$y")]
hover.formatters = {'@Date': 'datetime'}
p.add_tools(hover)

p.legend.location = 'top_left'
p.legend.click_policy = 'hide'

# Criando o menu dropdown para selecionar a ação
menu = Select(options=acoes, value='AAPL', title='Selecione uma Ação')

# Função para atualizar o gráfico ao selecionar uma ação no menu dropdown
def update_plot(attr, old, new):
    selected_acao = menu.value
    p.title.text = f"Preço de Fechamento da Ação {selected_acao}"
    source.data = ColumnDataSource(dados_acoes[selected_acao]).data

menu.on_change('value', update_plot)

# Organizando o layout do dashboard
layout = column(menu, p)

# Configurando o documento do Bokeh
curdoc().add_root(layout)
