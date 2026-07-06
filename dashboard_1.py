import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Panorama da Saúde da Mulher",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CARREGAMENTO E TRATAMENTO DOS DADOS
# ==========================================
@st.cache_data
def load_data():
    """
    Carrega e limpa os dados. O cache_data evita que o Streamlit 
    leia o arquivo toda vez que o usuário interagir com a tela.
    """
    try:
        # Carregando os dados
        df_exames = pd.read_excel('data/Exames.xlsx')
        df_obitos = pd.read_excel('data/Obitos.xlsx')
        
        # --- TRATAMENTO: EXAMES ---
        # Renomear colunas para termos mais fáceis
        df_exames = df_exames.rename(columns={'Faixa.etaria': 'Faixa Etária'})
        
        # Traduzir jargões técnicos dos exames para o público leigo
        mapa_exames = {
            'citocolo': 'Prevenção de Colo de Útero (Papanicolau)',
            'histomama': 'Rastreio de Mama (Mamografia/Biópsia)'
        }
        df_exames['exame'] = df_exames['exame'].map(mapa_exames)
        
        # --- TRATAMENTO: ÓBITOS ---
        df_obitos = df_obitos.rename(columns={'Idade_intervalo': 'Faixa Etária'})
        
        # Padronizar nomes das causas
        df_obitos['Causa'] = df_obitos['Causa'].str.strip().replace({
            'Câncer do colo do útero': 'Câncer de Colo de Útero',
            'Câncer de mama': 'Câncer de Mama'
        })
        
        return df_exames, df_obitos
    except Exception as e:
        st.error(f"Erro ao carregar os dados. Verifique a pasta 'data'. Detalhes: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_exames, df_obitos = load_data()

# ==========================================
# 3. BARRA LATERAL (MENU E FILTROS)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=100) # Ícone decorativo
st.sidebar.title("Navegação")

# Navegação entre páginas
pagina = st.sidebar.radio(
    "Escolha a página que deseja ver:",
    ["Visão Geral", "Análise: Câncer de Mama", "Análise: Câncer de Colo de Útero", "Comparações e Tendências", "Disponibilidade de Dados"]
)

st.sidebar.markdown("---")
st.sidebar.header("Filtros Globais")
# Filtro de Ano (pegando os anos disponíveis em ambos os datasets)
# Removendo possívies espaços nos nomes das colunas para evitar problemas
df_exames.columns = df_exames.columns.astype(str).str.strip()
df_obitos.columns = df_obitos.columns.astype(str).str.strip()
# Passando a coluna 'Ano' para inteiro para evitar problemas de comparação
df_exames['Ano'] = pd.to_numeric(df_exames['Ano'], errors='coerce')
df_obitos['Ano'] = pd.to_numeric(df_obitos['Ano'], errors='coerce')
anos_disponiveis = sorted(list(set(df_obitos['Ano'].unique()) | set(df_exames['Ano'].unique())))
ano_selecionado = st.sidebar.multiselect(
    "Selecione o(s) Ano(s):",
    options=anos_disponiveis,
    default=anos_disponiveis
)

# Aplicar o filtro de ano nos datasets
if ano_selecionado:
    df_exames_filtrado = df_exames[df_exames['Ano'].isin(ano_selecionado)]
    df_obitos_filtrado = df_obitos[df_obitos['Ano'].isin(ano_selecionado)]
else:
    df_exames_filtrado = df_exames.copy()
    df_obitos_filtrado = df_obitos.copy()

# ==========================================
# 4. CONSTRUÇÃO DAS PÁGINAS
# ==========================================

if pagina == "Visão Geral":
    st.title("🌸 Panorama da Saúde da Mulher")
    st.markdown("""
    Bem-vindo(a) ao painel de monitoramento da saúde feminina. 
    Aqui, traduzimos dados médicos sobre **Câncer de Mama** e **Câncer de Colo de Útero** em informações simples e visuais.
    Nosso objetivo é entender como estão os exames preventivos e, infelizmente, os casos de fatalidade, para conscientizar a sociedade.
    """)
    
    st.markdown("### 📊 Indicadores Principais (Período Selecionado)")
    
    # KPIs (Key Performance Indicators)
    col1, col2, col3 = st.columns(3)
    
    total_exames = df_exames_filtrado['Exames'].sum()
    total_obitos = len(df_obitos_filtrado)
    
    with col1:
        st.metric("Total de Exames Realizados", f"{total_exames:,.0f}".replace(',','.'))
        st.caption("Quanto mais exames, maior a chance de prevenção!")
        
    with col2:
        st.metric("Total de Vidas Perdidas", f"{total_obitos:,.0f}".replace(',','.'))
        st.caption("Óbitos registrados por esses dois tipos de câncer.")
        
    with col3:
        exame_mais_feito = df_exames_filtrado.groupby('exame')['Exames'].sum().idxmax()
        st.metric("Exame Mais Procurado", exame_mais_feito.split('(')[0].strip())
        st.caption("Tipo de prevenção com maior volume.")


    st.markdown("---")
    st.markdown("""
    ### 💡 Como usar este painel?
    - Utilize o **menu à esquerda** para navegar entre as diferentes páginas.
    - Você pode **filtrar por ano** na barra lateral para ver dados de um período específico.
    - Sempre que vir um gráfico, leia a caixa **"O que esse gráfico quer dizer?"** logo abaixo dele para uma explicação simples.
    """)

elif pagina == "Análise: Câncer de Mama":
    st.title("🎀 Câncer de Mama")
    st.markdown("O câncer de mama é um dos mais comuns entre as mulheres. A detecção precoce pela mamografia salva vidas.")
    
    # Filtrar apenas dados de Mama
    df_exames_mama = df_exames_filtrado[df_exames_filtrado['exame'].str.contains('Mama', case=False, na=False)]
    df_obitos_mama = df_obitos_filtrado[df_obitos_filtrado['Causa'] == 'Câncer de Mama']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exames Realizados por Faixa Etária")
        exames_por_idade = df_exames_mama.groupby('Faixa Etária')['Exames'].sum().reset_index()
        fig_exames = px.bar(exames_por_idade, x='Faixa Etária', y='Exames', 
                            color_discrete_sequence=['#ff99cc'], text_auto='.2s')
        fig_exames.update_layout(xaxis_title="Idade das Mulheres", yaxis_title="Quantidade de Exames")
        st.plotly_chart(fig_exames, use_container_width=True)
        
        st.info("**O que esse gráfico quer dizer?**\nEle mostra em qual idade as mulheres estão procurando mais os exames de mama. Picos altos indicam que as mulheres dessa idade estão se prevenindo mais.")

    with col2:
        st.subheader("Vidas Perdidas por Faixa Etária")
        obitos_por_idade = df_obitos_mama.groupby('Faixa Etária').size().reset_index(name='Óbitos')
        fig_obitos = px.line(obitos_por_idade, x='Faixa Etária', y='Óbitos', markers=True,
                             color_discrete_sequence=['#cc0066'])
        fig_obitos.update_layout(xaxis_title="Idade das Mulheres", yaxis_title="Quantidade de Óbitos")
        st.plotly_chart(fig_obitos, use_container_width=True)
        
        st.warning("**O que esse gráfico quer dizer?**\nEle mostra a linha de risco. Se a linha sobe em uma certa idade, significa que o câncer de mama tem sido mais fatal para mulheres dessa faixa etária.")

elif pagina == "Análise: Câncer de Colo de Útero":
    st.title("🎗️ Câncer de Colo de Útero")
    st.markdown("Esse tipo de câncer está muito ligado à infecção pelo HPV e pode ser facilmente prevenido com a vacina e o exame Papanicolau.")
    
    # Filtrar apenas dados de Colo de Útero
    df_exames_colo = df_exames_filtrado[df_exames_filtrado['exame'].str.contains('Colo', case=False, na=False)]
    df_obitos_colo = df_obitos_filtrado[df_obitos_filtrado['Causa'] == 'Câncer de Colo de Útero']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exames Papanicolau por Ano")
        exames_ano = df_exames_colo.groupby('Ano')['Exames'].sum().reset_index()
        fig_exames_ano = px.bar(exames_ano, x='Ano', y='Exames', 
                                color_discrete_sequence=['#66b3ff'], text_auto=True)
        fig_exames_ano.update_xaxes(type='category') # Garantir que o ano não apareça quebrado (ex: 2022.5)
        # Ajustando a formatação dos números para o padrão brasileiro
        fig_exames_ano.update_traces(
        text=exames_ano['Exames'].apply(lambda x: f"{x:,.0f}".replace(",", ".")),
        texttemplate='%{text}',
        textposition='inside')
        st.plotly_chart(fig_exames_ano, use_container_width=True)
        
        st.info("**O que esse gráfico quer dizer?**\nAjuda a entender se a procura pelo exame preventivo está aumentando ou caindo ao longo dos anos.")

    with col2:
        st.subheader("Cor/Raça e Impacto")
        obitos_raca = df_obitos_colo.groupby('RACACOR').size().reset_index(name='Quantidade')
        fig_raca = px.pie(obitos_raca, values='Quantidade', names='RACACOR', 
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_raca, use_container_width=True)
        
        st.warning("**O que esse gráfico quer dizer?**\nEle divide as fatalidades pela cor/raça registrada. Isso é fundamental para identificar se algum grupo específico está com dificuldades no acesso ao tratamento de saúde.")

elif pagina == "Comparações e Tendências":
    st.title("⚖️ Comparações: Mama vs Colo de Útero")
    st.markdown("Vamos colocar os dois cenários lado a lado para entender qual deles tem demandado mais atenção.")
    
    st.subheader("1. A evolução no tempo (Óbitos)")
    
    # Agrupar óbitos por Ano e Causa
    obitos_tendencia = df_obitos_filtrado.groupby(['Ano', 'Causa']).size().reset_index(name='Vidas Perdidas')
    
    fig_tendencia = px.bar(obitos_tendencia, x='Ano', y='Vidas Perdidas', color='Causa', barmode='group',
                           color_discrete_map={'Câncer de Mama': '#ff99cc', 'Câncer de Colo de Útero': '#66b3ff'})
    fig_tendencia.update_xaxes(type='category')
    st.plotly_chart(fig_tendencia, use_container_width=True)
    
    st.info("""
    **O que esse gráfico quer dizer?**
    Ele compara lado a lado as fatalidades de cada câncer em cada ano. 
    - Barras mais altas indicam uma necessidade de maior atenção das autoridades de saúde.
    - Se uma barra diminui com o passar dos anos, é sinal de que as políticas de prevenção podem estar funcionando.
    """)
    
    st.markdown("---")
    
    st.subheader("2. Proporção de Exames Preventivos")
    exames_totais = df_exames_filtrado.groupby('exame')['Exames'].sum().reset_index()
    fig_pizza_exames = px.pie(exames_totais, values='Exames', names='exame', hole=0.4,
                              color_discrete_sequence=['#ff99cc', '#66b3ff'])
    st.plotly_chart(fig_pizza_exames, use_container_width=True)
    
    st.success("""
    **O que esse gráfico quer dizer?**
    Esse formato de 'rosca' mostra para onde estão indo os esforços de exames da população. 
    Um pedaço maior indica que aquele tipo de exame foi realizado mais vezes do que o outro.
    """)

elif pagina == "Disponibilidade de Dados":
    st.title("📊 Disponibilidade de Dados")
    st.markdown("Dados referentes aos óbitos por câncer de mama e colo de útero")
    st.dataframe(df_exames)
    st.markdown("Dados referentes aos exames")
    st.dataframe(df_obitos)