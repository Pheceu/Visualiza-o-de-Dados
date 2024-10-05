import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



#python -m streamlit run dashboard.py

#Escolha do tema
backgroundColor="#f9f9f9"
secondaryBackgroundColor="#bac9e6"
textColor="#0f0f10"

# Carregar o dataset
data = pd.read_csv("houses_to_rent_v2.csv")

#Renomeia as colunas e substitui todos resultados das colunas "Mobilia" e "Animal" pelas expressões relacionadas.
data_trad=data.rename(columns={'city':'Cidade', 'area':'Área','rooms':'Quartos','bathroom':'Banheiros','parking spaces':'Vagas de estacionamento','floor':'Andar','animal':'Animal','furniture':'Mobília','hoa':'Condomínio (R$)','rent amount (R$)':'Valor do Aluguel (R$)','property tax (R$)':'IPTU','fire insurance (R$)':'Seguro Contra Incêndio','total (R$)':'Total (R$)'})
data_trad['Mobília'] = data_trad['Mobília'].replace({'furnished': 'Mobiliado','not furnished': 'Sem mobília'})
data_trad['Animal'] = data_trad['Animal'].replace({'acept': 'Aceita','not acept': 'Não Aceita'})

#Cria menu lateral configurar layout do app Streamlit para ocupação total da página
with st.sidebar:
    st.set_page_config(layout="wide")
    st.title("Imóveis para Aluguel")

# Combobox para selecionar a quantidade de quartos
    rooms_selected = st.selectbox("Selecione a quantidade de quartos", sorted(data_trad['Quartos'].unique()))

# Filtrar os dados pela quantidade de quartos selecionada
    filtered_data = data_trad[data_trad['Quartos'] == rooms_selected]

st.header("Universidade Federal do Maranhão - UFMA")

mult= '''Disciplina: Visualizão de Dados  

Prof: Drº Paulo Rogério de Almeida Ribeiro  

Tutor: Clemilton Duarley P. da Silva

Aluno: Valdessandro Costa Moreira'''
st.markdown(mult)
st.divider()

# Criar uma estrutura de 3 colunas para exibir a quantidade de imóveis, preço mínimo e preço máximo
col1, col2, col3 = st.columns(3)

# Exibir os dados nas respectivas colunas
with col1:
    total_properties = len(filtered_data)
    st.metric(label="Quantidade de imóveis", value=total_properties)

with col2:
    min_rent = filtered_data['Valor do Aluguel (R$)'].min()
    st.metric(label="Preço mínimo do aluguel*", value=f"R$ {min_rent}")

with col3:
    max_rent = filtered_data['Valor do Aluguel (R$)'].max()
    st.metric(label="Preço máximo do aluguel*", value=f"R$ {max_rent}")
st.caption("***Não incluso demais custos**")
st.divider()

#Insere duas quebras de linhas
('\n') 
('\n')
st.markdown("Podemos constatar que a cidade de **São Paulo** possui o **maior número de imóveis** bem como **o maior preço médio**")
col4, col5 =st.columns(2)
col6, col7=st.columns(2)

# Preço médio por cidade, ordenado em ordem decrescente
avg_price_by_city = filtered_data.groupby('Cidade')['Valor do Aluguel (R$)'].mean().sort_values(ascending=True)

# Preço médio com e sem mobília
avg_price_furnished = filtered_data[filtered_data['Mobília'] == 'Mobiliado']['Valor do Aluguel (R$)'].mean()
avg_price_not_furnished = filtered_data[filtered_data['Mobília'] == 'Sem mobília']['Valor do Aluguel (R$)'].mean()


# Gráfico de barras para preço médio por cidade sem eixo x e em ordem decrescente
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), gridspec_kw={'width_ratios': [20, 15]})

# Gráfico de barras horizontal para o preço médio por cidade sem eixo x
ax1.barh(avg_price_by_city.index, avg_price_by_city.values, color='#d0dbf1', edgecolor='none')
ax1.set_title("Preço Médio por Cidade (Ordem Decrescente)")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.tick_params(left=False, bottom=False)  # Remover ticks do eixo x
ax1.set_xticks([])  # Remover valores do eixo x
for i, v in enumerate(avg_price_by_city.values):
    ax1.text(v + 100, i, f'{v:.2f}', va='center', color='black')

# Gráfico de barras para preços médios com e sem mobília sem eixo y e com largura reduzida

ax2.bar(['Mobíliado', 'Sem Mobília'], [avg_price_furnished, avg_price_not_furnished], color=['#d0dbf1', '#d0dbf1'], edgecolor='none')
ax2.set_title("Preço Médio com e sem Mobília")
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.tick_params(left=False, bottom=False)  # Remover ticks do eixo y
ax2.set_yticks([])  # Remover valores do eixo y
for i, v in enumerate([avg_price_furnished, avg_price_not_furnished]):
    ax2.text(i, v + 100, f'{v:.2f}', ha='center', color='black')

# Exibir os gráficos usando a largura total da página
st.pyplot(fig)

# Adicionar um ComboBox para selecionar a cidade, já selecionando a cidade com o maior valor
city_selected = st.selectbox("Selecione a cidade", sorted(filtered_data['Cidade'].unique()), index=0)

# Filtrar os imóveis pela cidade selecionada e ordenar por preço decrescente
city_filtered_data = filtered_data[filtered_data['Cidade'] == city_selected].sort_values(by='Valor do Aluguel (R$)', ascending=False)

# Exibir a lista dos primeiros imóveis da cidade selecionada, sem o índice
st.write(f"Imóveis na cidade de {city_selected} (ordenados por preço de forma decrescente):")
st.dataframe(city_filtered_data[['Cidade', 'Valor do Aluguel (R$)', 'Quartos', 'Mobília', 'Total (R$)']].head(10), width=1400, height=300,hide_index=True)
