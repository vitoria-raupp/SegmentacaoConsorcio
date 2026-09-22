import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Perfil de Cliente e Busca ",
    page_icon="📊",
    layout="wide"
) 

st.title("Perfil de Cliente e Busca ")
# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================

df = pd.read_csv(
    "data/clientes_segmentados_conquiste2.csv"
)


st.divider()


# =========================================================
# FILTROS
# =========================================================

st.subheader("🔎 Filtros")

df_filtrado = df.copy()


# =========================================================
# PRIMEIRA LINHA DE FILTROS
# =========================================================

col1, col2, col3 = st.columns(3)


# ---------------------------------------------------------
# TIPO DE CLIENTE
# ---------------------------------------------------------

with col1:

    tipos_pessoa = sorted(
        df["tipo_pessoa"]
        .dropna()
        .unique()
    )

    filtro_tipo = st.multiselect(
        "Tipo de Cliente",
        options=tipos_pessoa,
        default=tipos_pessoa
    )


# ---------------------------------------------------------
# UF
# ---------------------------------------------------------

with col2:

    ufs = sorted(
        df["nm_uf"]
        .dropna()
        .unique()
    )

    filtro_uf = st.multiselect(
        "UF",
        options=ufs,
        placeholder="Todas as UFs"
    )

# ---------------------------------------------------------
# PRODUTO ATUAL
# ---------------------------------------------------------

with col3:

    produtos = sorted(
        df["produto"]
        .dropna()
        .unique()
    )

    filtro_produto = st.multiselect(
        "Produto Atual",
        options=produtos,
        placeholder="Todos os produtos"
    )


# =========================================================
# SEGUNDA LINHA DE FILTROS
# =========================================================

col1, col2, col3 = st.columns(3)


# ---------------------------------------------------------
# PRODUTO RECOMENDADO
# ---------------------------------------------------------

with col1:

    produtos_recomendados = sorted(
        df["produto_recomendado"]
        .dropna()
        .unique()
    )

    filtro_recomendado = st.multiselect(
        "Produto Recomendado",
        options=produtos_recomendados,
        placeholder="Todos"
    )


# ---------------------------------------------------------
# SEGMENTO
# ---------------------------------------------------------

with col2:

    segmentos = sorted(
        df["segmento_conquiste"]
        .dropna()
        .unique()
    )

    filtro_segmento = st.multiselect(
        "Segmento Conquiste+",
        options=segmentos,
        placeholder="Todos os segmentos"
    )


# ---------------------------------------------------------
# FAIXA DE RENDA
# ---------------------------------------------------------

with col3:

    renda_min = float(
        df["vl_renda_mensal"]
        .dropna()
        .min()
    )

    renda_max = float(
        df["vl_renda_mensal"]
        .dropna()
        .max()
    )

    filtro_renda = st.slider(
        "Faixa de Renda Mensal",
        min_value=renda_min,
        max_value=renda_max,
        value=(
            renda_min,
            renda_max
        ),
        format="R$ %.0f"
    )


# =========================================================
# APLICAÇÃO DOS FILTROS
# =========================================================

if filtro_tipo:

    df_filtrado = df_filtrado[
        df_filtrado["tipo_pessoa"].isin(
            filtro_tipo
        )
    ]


if filtro_uf:

    df_filtrado = df_filtrado[
        df_filtrado["nm_uf"].isin(
            filtro_uf
        )
    ]


if filtro_produto:

    df_filtrado = df_filtrado[
        df_filtrado["produto"].isin(
            filtro_produto
        )
    ]


if filtro_recomendado:

    df_filtrado = df_filtrado[
        df_filtrado["produto_recomendado"].isin(
            filtro_recomendado
        )
    ]


if filtro_segmento:

    df_filtrado = df_filtrado[
        df_filtrado["segmento_conquiste"].isin(
            filtro_segmento
        )
    ]


df_filtrado = df_filtrado[
    df_filtrado["vl_renda_mensal"].between(
        filtro_renda[0],
        filtro_renda[1]
    )
]


# =========================================================
# VERIFICAÇÃO
# =========================================================

if df_filtrado.empty:

    st.warning(
        "Nenhum cliente encontrado para os filtros selecionados."
    )

    st.stop()


st.divider()


# =========================================================
# BASE DE CLIENTES ÚNICOS
# =========================================================

clientes_unicos = (
    df_filtrado[
        [
            "cod_cliente_ficticio",
            "tipo_pessoa",
            "nm_uf",
            "vl_renda_mensal"
        ]
    ]
    .drop_duplicates(
        subset=[
            "cod_cliente_ficticio",
            "tipo_pessoa"
        ]
    )
)


# =========================================================
# RESUMO DO PÚBLICO
# =========================================================

st.subheader("📊 Resumo do Público Selecionado")


total_clientes = clientes_unicos[
    "cod_cliente_ficticio"
].nunique()


renda_media = clientes_unicos[
    "vl_renda_mensal"
].mean()


saldo_medio = df_filtrado[
    "vl_saldo_devedor_total"
].mean()


tempo_medio = df_filtrado[
    "tempo_medio_permanencia_meses"
].mean()


total_pf = clientes_unicos.loc[
    clientes_unicos["tipo_pessoa"] == "FISICA",
    "cod_cliente_ficticio"
].nunique()


total_pj = clientes_unicos.loc[
    clientes_unicos["tipo_pessoa"] == "JURÍDICA",
    "cod_cliente_ficticio"
].nunique()


col1, col2, col3, col4, col5, col6 = st.columns(6)


col1.metric(
    "Clientes",
    f"{total_clientes:,}".replace(",", ".")
)

col2.metric(
    "PF",
    f"{total_pf:,}".replace(",", ".")
)

col3.metric(
    "PJ",
    f"{total_pj:,}".replace(",", ".")
)

col4.metric(
    "Renda Média",
    f"R$ {renda_media:,.0f}"
)

col5.metric(
    "Saldo Médio",
    f"R$ {saldo_medio:,.0f}"
)

col6.metric(
    "Permanência Média",
    f"{tempo_medio:.0f} meses"
)


st.divider()


# =========================================================
# VISÃO DO PÚBLICO FILTRADO
# =========================================================

st.subheader("Perfil do Público Filtrado")


# ---------------------------------------------------------
# GRÁFICO 1 - TIPO DE CLIENTE
# ---------------------------------------------------------

volume_tipo = (
    clientes_unicos
    .groupby("tipo_pessoa")
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


fig_tipo = px.pie(
    volume_tipo,
    names="tipo_pessoa",
    values="clientes",
    hole=0.55,
    title="Composição PF x PJ"
)

fig_tipo.update_traces(
    textinfo="percent+label"
)


# ---------------------------------------------------------
# GRÁFICO 2 - RENDA POR UF
# ---------------------------------------------------------

renda_uf = (
    clientes_unicos
    .groupby(
        [
            "nm_uf",
            "tipo_pessoa"
        ]
    )
    .agg(
        renda_media=("vl_renda_mensal", "mean")
    )
    .reset_index()
)


fig_renda_uf = px.bar(
    renda_uf,
    x="nm_uf",
    y="renda_media",
    color="tipo_pessoa",
    barmode="group",
    title="Renda Média por UF",
    labels={
        "nm_uf": "UF",
        "renda_media": "Renda Média",
        "tipo_pessoa": "Tipo de Cliente"
    }
)

fig_renda_uf.update_layout(
    yaxis_tickprefix="R$ ",
    yaxis_tickformat=",.0f"
)


# ---------------------------------------------------------
# EXIBIÇÃO
# ---------------------------------------------------------

col1, col2 = st.columns(
    [1, 2]
)


with col1:

    st.plotly_chart(
        fig_tipo,
        use_container_width=True
    )


with col2:

    st.plotly_chart(
        fig_renda_uf,
        use_container_width=True
    )


st.divider()


# =========================================================
# ANÁLISE INDIVIDUAL
# =========================================================

st.subheader("🔍 Perfil Individual do Cliente")


lista_clientes = sorted(
    df_filtrado[
        "cod_cliente_ficticio"
    ]
    .dropna()
    .unique()
)


cliente_selecionado = st.selectbox(
    "Selecione o cliente",
    options=lista_clientes
)


# =========================================================
# DADOS DO CLIENTE
# =========================================================

dados_cliente = (
    df_filtrado[
        df_filtrado[
            "cod_cliente_ficticio"
        ] == cliente_selecionado
    ]
    .copy()
)


cliente = dados_cliente.iloc[0]


# =========================================================
# IDENTIFICAÇÃO
# =========================================================

st.markdown("### 👤 Identificação")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Código do Cliente",
    str(cliente_selecionado)
)


col2.metric(
    "Tipo",
    str(cliente["tipo_pessoa"])
)


col3.metric(
    "UF",
    str(cliente["nm_uf"])
)


col4.metric(
    "Renda Mensal",
    f'R$ {cliente["vl_renda_mensal"]:,.2f}'
)


# =========================================================
# RELACIONAMENTO
# =========================================================

st.markdown("### 🤝 Relacionamento")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Tempo de Relacionamento",
    f'{cliente["tempo_relacionamento_anos"]:.1f} anos'
)


col2.metric(
    "Permanência Média",
    f'{cliente["tempo_medio_permanencia_meses"]:.0f} meses'
)


col3.metric(
    "Quantidade de Cotas",
    f'{cliente["qtd_cotas_total"]:.0f}'
)


col4.metric(
    "Saldo Devedor",
    f'R$ {cliente["vl_saldo_devedor_total"]:,.2f}'
)


# =========================================================
# HISTÓRICO DO CONSÓRCIO
# =========================================================

st.markdown("### 💰 Histórico de Consórcio")


col1, col2, col3 = st.columns(3)


col1.metric(
    "Cotas Totais",
    f'{cliente["qtd_cotas_total"]:.0f}'
)


col2.metric(
    "Cotas Contempladas",
    f'{cliente["qtd_cotas_contempladas"]:.0f}'
)


col3.metric(
    "Cotas Não Contempladas",
    f'{cliente["qtd_cotas_nao_contempladas"]:.0f}'
)


# =========================================================
# PRODUTOS
# =========================================================

st.markdown("### 🚗🏠 Produtos e Segmentação")


produtos_cliente = (
    dados_cliente[
        "produto"
    ]
    .dropna()
    .unique()
)


produtos_texto = ", ".join(
    map(
        str,
        produtos_cliente
    )
)


col1, col2, col3 = st.columns(3)


col1.metric(
    "Produtos Atuais",
    produtos_texto
)


col2.metric(
    "Produto Recomendado",
    str(
        cliente["produto_recomendado"]
    )
)


col3.metric(
    "Segmento Conquiste+",
    str(
        cliente["segmento_conquiste"]
    )
)


st.divider()


# =========================================================
# SCORE DE PROPENSÃO
# =========================================================

st.subheader("🎯 Propensão do Cliente")


scores_cliente = pd.DataFrame(
    {
        "Produto": [
            "Veículos",
            "Imóveis"
        ],

        "Score": [
            cliente["score_veiculos"],
            cliente["score_imoveis"]
        ]
    }
)


fig_score = px.bar(
    scores_cliente,
    x="Produto",
    y="Score",
    text="Score",
    title="Score de Propensão por Produto",
    labels={
        "Score": "Score de Propensão"
    }
)


fig_score.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)


fig_score.update_layout(
    height=450,
    showlegend=False,
    yaxis_title="Score",
    xaxis_title=""
)


st.plotly_chart(
    fig_score,
    use_container_width=True
)


st.divider()


# =========================================================
# CLIENTE X PERFIL MÉDIO
# =========================================================

st.subheader("📊 Cliente x Perfil Médio")


# Comparar apenas com clientes do mesmo tipo
perfil_comparacao = df_filtrado[
    df_filtrado[
        "tipo_pessoa"
    ] == cliente["tipo_pessoa"]
]


# =========================================================
# MÉDIAS DO PERFIL
# =========================================================

renda_media_perfil = (
    perfil_comparacao[
        "vl_renda_mensal"
    ]
    .mean()
)


saldo_medio_perfil = (
    perfil_comparacao[
        "vl_saldo_devedor_total"
    ]
    .mean()
)


tempo_medio_perfil = (
    perfil_comparacao[
        "tempo_medio_permanencia_meses"
    ]
    .mean()
)


cotas_media_perfil = (
    perfil_comparacao[
        "qtd_cotas_total"
    ]
    .mean()
)


# =========================================================
# CARDS COMPARATIVOS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


# ---------------------------------------------------------
# RENDA
# ---------------------------------------------------------

variacao_renda = (
    (
        cliente["vl_renda_mensal"]
        / renda_media_perfil
    ) - 1
) * 100


col1.metric(
    "Renda",
    f'R$ {cliente["vl_renda_mensal"]:,.0f}',
    delta=f"{variacao_renda:.1f}% vs média"
)


# ---------------------------------------------------------
# SALDO
# ---------------------------------------------------------

variacao_saldo = (
    (
        cliente["vl_saldo_devedor_total"]
        / saldo_medio_perfil
    ) - 1
) * 100


col2.metric(
    "Saldo Devedor",
    f'R$ {cliente["vl_saldo_devedor_total"]:,.0f}',
    delta=f"{variacao_saldo:.1f}% vs média"
)


# ---------------------------------------------------------
# PERMANÊNCIA
# ---------------------------------------------------------

variacao_tempo = (
    (
        cliente["tempo_medio_permanencia_meses"]
        / tempo_medio_perfil
    ) - 1
) * 100


col3.metric(
    "Permanência",
    f'{cliente["tempo_medio_permanencia_meses"]:.0f} meses',
    delta=f"{variacao_tempo:.1f}% vs média"
)


# ---------------------------------------------------------
# COTAS
# ---------------------------------------------------------

variacao_cotas = (
    (
        cliente["qtd_cotas_total"]
        / cotas_media_perfil
    ) - 1
) * 100


col4.metric(
    "Quantidade de Cotas",
    f'{cliente["qtd_cotas_total"]:.0f}',
    delta=f"{variacao_cotas:.1f}% vs média"
)


# =========================================================
# GRÁFICO COMPARATIVO
# =========================================================

comparacao = pd.DataFrame(
    {
        "Indicador": [
            "Renda",
            "Saldo Devedor",
            "Permanência",
            "Cotas"
        ],

        "Cliente": [
            cliente[
                "vl_renda_mensal"
            ],

            cliente[
                "vl_saldo_devedor_total"
            ],

            cliente[
                "tempo_medio_permanencia_meses"
            ],

            cliente[
                "qtd_cotas_total"
            ]
        ],

        "Média do Perfil": [
            renda_media_perfil,
            saldo_medio_perfil,
            tempo_medio_perfil,
            cotas_media_perfil
        ]
    }
)


# =========================================================
# NORMALIZAÇÃO PARA COMPARAR ESCALAS DIFERENTES
# =========================================================

comparacao_normalizada = comparacao.copy()


for indice, linha in comparacao.iterrows():

    maior_valor = max(
        linha["Cliente"],
        linha["Média do Perfil"]
    )

    if maior_valor > 0:

        comparacao_normalizada.loc[
            indice,
            "Cliente"
        ] = (
            linha["Cliente"]
            / maior_valor
        ) * 100


        comparacao_normalizada.loc[
            indice,
            "Média do Perfil"
        ] = (
            linha["Média do Perfil"]
            / maior_valor
        ) * 100


# =========================================================
# TRANSFORMAÇÃO PARA FORMATO LONGO
# =========================================================

comparacao_plot = (
    comparacao_normalizada
    .melt(
        id_vars="Indicador",
        value_vars=[
            "Cliente",
            "Média do Perfil"
        ],
        var_name="Perfil",
        value_name="Índice"
    )
)


# =========================================================
# GRÁFICO
# =========================================================

fig_comparacao = px.bar(
    comparacao_plot,
    x="Indicador",
    y="Índice",
    color="Perfil",
    barmode="group",
    text_auto=".0f",
    title=(
        f"Cliente x Média do Perfil "
        f"{cliente['tipo_pessoa']}"
    )
)


fig_comparacao.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Índice Comparativo",
    legend_title=""
)


st.plotly_chart(
    fig_comparacao,
    use_container_width=True
)


st.divider()


# =========================================================
# POSICIONAMENTO DO CLIENTE
# =========================================================

st.subheader("📌 Posicionamento do Cliente")


col1, col2 = st.columns(2)


# =========================================================
# RENDA X PERMANÊNCIA
# =========================================================

with col1:

    fig_renda_tempo = px.scatter(
        perfil_comparacao,
        x="tempo_medio_permanencia_meses",
        y="vl_renda_mensal",
        opacity=0.4,
        title="Renda x Tempo de Permanência",
        labels={
            "tempo_medio_permanencia_meses":
                "Permanência (meses)",

            "vl_renda_mensal":
                "Renda Mensal"
        }
    )


    fig_renda_tempo.add_trace(
        go.Scatter(
            x=[
                cliente[
                    "tempo_medio_permanencia_meses"
                ]
            ],

            y=[
                cliente[
                    "vl_renda_mensal"
                ]
            ],

            mode="markers",

            marker=dict(
                size=18,
                symbol="star"
            ),

            name="Cliente Selecionado"
        )
    )


    fig_renda_tempo.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.0f"
    )


    st.plotly_chart(
        fig_renda_tempo,
        use_container_width=True
    )


# =========================================================
# SALDO X PERMANÊNCIA
# =========================================================

with col2:

    fig_saldo_tempo = px.scatter(
        perfil_comparacao,
        x="tempo_medio_permanencia_meses",
        y="vl_saldo_devedor_total",
        opacity=0.4,
        title="Saldo Devedor x Tempo de Permanência",
        labels={
            "tempo_medio_permanencia_meses":
                "Permanência (meses)",

            "vl_saldo_devedor_total":
                "Saldo Devedor"
        }
    )


    fig_saldo_tempo.add_trace(
        go.Scatter(
            x=[
                cliente[
                    "tempo_medio_permanencia_meses"
                ]
            ],

            y=[
                cliente[
                    "vl_saldo_devedor_total"
                ]
            ],

            mode="markers",

            marker=dict(
                size=18,
                symbol="star"
            ),

            name="Cliente Selecionado"
        )
    )


    fig_saldo_tempo.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.0f"
    )


    st.plotly_chart(
        fig_saldo_tempo,
        use_container_width=True
    )


# =========================================================
# DADOS DETALHADOS
# =========================================================

st.divider()


with st.expander(
    "📋 Ver todos os dados do cliente"
):

    st.dataframe(
        dados_cliente,
        use_container_width=True,
        hide_index=True
    )