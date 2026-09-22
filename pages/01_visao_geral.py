import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown(
    """
    Visão geral da base de clientes e dos principais
    indicadores utilizados na análise.
    """
)


# ---------------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------------
df = pd.read_csv("data/clientes_segmentados_conquiste2.csv")

# ---------------------------------------------------------
# BASE ÚNICA DE CLIENTES
# ---------------------------------------------------------

# Evita contar o mesmo cliente mais de uma vez
# caso ele possua mais de um produto.

clientes = (
    df[
        [
            "cod_cliente_ficticio",
            "tipo_pessoa",
            "vl_renda_mensal"
        ]
    ]
    )


# ---------------------------------------------------------
# TÍTULO
# -------------------------------------------------------
# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

total_clientes = clientes["cod_cliente_ficticio"].nunique()

total_pf = clientes.loc[
    clientes["tipo_pessoa"] == "FISICA",
    "cod_cliente_ficticio"
].nunique()

total_pj = clientes.loc[
    clientes["tipo_pessoa"] == "JURÍDICA",
    "cod_cliente_ficticio"
].nunique()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Clientes",
    f"{total_clientes:,}".replace(",", ".")
)

col2.metric(
    "Pessoa Física",
    f"{total_pf:,}".replace(",", ".")
)

col3.metric(
    "Pessoa Jurídica",
    f"{total_pj:,}".replace(",", ".")
)


st.divider()


# =========================================================
# GRÁFICO 1 - VOLUME POR TIPO DE CLIENTE
# =========================================================

volume_tipo = (
    clientes
    .groupby("tipo_pessoa")
    .agg(
        clientes=("cod_cliente_ficticio", "nunique")
    )
    .reset_index()
)


fig_volume = px.bar(
    volume_tipo,
    x="tipo_pessoa",
    y="clientes",
    color="tipo_pessoa",
    text="clientes",
    title="Volume de Clientes por Tipo de Pessoa",
    labels={
        "tipo_pessoa": "Tipo de Cliente",
        "clientes": "Quantidade de Clientes"
    }
)

fig_volume.update_traces(
    textposition="outside"
)

fig_volume.update_layout(
    showlegend=False,
    xaxis_title="Tipo de Cliente",
    yaxis_title="Quantidade de Clientes"
)


# =========================================================
# GRÁFICO 2 - RENDA MÉDIA POR TIPO DE CLIENTE
# =========================================================

renda_tipo = (
    clientes
    .groupby("tipo_pessoa")
    .agg(
        renda_media=("vl_renda_mensal", "mean")
    )
    .reset_index()
)


fig_renda = px.bar(
    renda_tipo,
    x="tipo_pessoa",
    y="renda_media",
    color="tipo_pessoa",
    text="renda_media",
    title="Renda Média por Tipo de Cliente",
    labels={
        "tipo_pessoa": "Tipo de Cliente",
        "renda_media": "Renda Média"
    }
)

fig_renda.update_traces(
    texttemplate="R$ %{text:,.2f}",
    textposition="outside"
)

fig_renda.update_layout(
    showlegend=False,
    xaxis_title="Tipo de Cliente",
    yaxis_title="Renda Média (R$)"
)


# ---------------------------------------------------------
# EXIBIÇÃO DOS GRÁFICOS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_volume,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_renda,
        use_container_width=True
    )


# ---------------------------------------------------------
# PRÓXIMOS GRÁFICOS
# ---------------------------------------------------------

# =========================================================
# 3. DISTRIBUIÇÃO DOS PRODUTOS
# =========================================================

perfil_produto = (
    df
    .groupby("produto")
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


fig_produtos = px.pie(
    perfil_produto,
    names="produto",
    values="clientes",
    hole=0.55,
    title="Distribuição de Clientes por Produto"
)

fig_produtos.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig_produtos.update_layout(
    legend_title="Produto"
)

st.plotly_chart(
    fig_produtos,
    use_container_width=True
)

# =========================================================
# SALDO DEVEDOR X TEMPO DE PERMANÊNCIA - PF E PJ
# =========================================================

st.subheader("Saldo Devedor x Tempo de Permanência")


# ---------------------------------------------------------
# BASE PF
# ---------------------------------------------------------

df_pf = df[
    df["tipo_pessoa"] == "FISICA"
].copy()


# ---------------------------------------------------------
# BASE PJ
# ---------------------------------------------------------

df_pj = df[
    df["tipo_pessoa"] == "JURÍDICA"
].copy()


# =========================================================
# GRÁFICO 1 - PESSOA FÍSICA
# =========================================================

fig_pf = px.scatter(
    df_pf,
    x="tempo_medio_permanencia_meses",
    y="vl_saldo_devedor_total",
    color="produto",
    size="qtd_cotas_total",
    hover_data=[
        "cod_cliente_ficticio",
        "produto",
        "vl_renda_mensal",
        "qtd_cotas_total"
    ],
    title="Pessoa Física | Saldo Devedor x Tempo de Permanência",
    labels={
        "tempo_medio_permanencia_meses": "Tempo Médio de Permanência (meses)",
        "vl_saldo_devedor_total": "Saldo Devedor Total (R$)",
        "produto": "Produto",
        "qtd_cotas_total": "Quantidade de Cotas"
    }
)

fig_pf.update_layout(
    xaxis_title="Tempo Médio de Permanência (meses)",
    yaxis_title="Saldo Devedor Total (R$)",
    legend_title="Produto"
)


# =========================================================
# GRÁFICO 2 - PESSOA JURÍDICA
# =========================================================

fig_pj = px.scatter(
    df_pj,
    x="tempo_medio_permanencia_meses",
    y="vl_saldo_devedor_total",
    color="produto",
    size="qtd_cotas_total",
    hover_data=[
        "cod_cliente_ficticio",
        "produto",
        "vl_renda_mensal",
        "qtd_cotas_total"
    ],
    title="Pessoa Jurídica | Saldo Devedor x Tempo de Permanência",
    labels={
        "tempo_medio_permanencia_meses": "Tempo Médio de Permanência (meses)",
        "vl_saldo_devedor_total": "Saldo Devedor Total (R$)",
        "produto": "Produto",
        "qtd_cotas_total": "Quantidade de Cotas"
    }
)

fig_pj.update_layout(
    xaxis_title="Tempo Médio de Permanência (meses)",
    yaxis_title="Saldo Devedor Total (R$)",
    legend_title="Produto"
)


# =========================================================
# EXIBIÇÃO DOS GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_pf,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_pj,
        use_container_width=True
    )

# =========================================================
# FAIXAS DE PERMANÊNCIA
# =========================================================

df["faixa_permanencia"] = pd.cut(
    df["tempo_medio_permanencia_meses"],
    bins=[0, 12, 24, 60, 120, float("inf")],
    labels=[
        "Até 1 ano",
        "1 a 2 anos",
        "2 a 5 anos",
        "5 a 10 anos",
        "Acima de 10 anos"
    ]
)


saldo_permanencia = (
    df
    .groupby(
        ["faixa_permanencia", "tipo_pessoa"],
        observed=True
    )
    .agg(
        saldo_medio=("vl_saldo_devedor_total", "mean")
    )
    .reset_index()
)


fig_saldo_permanencia = px.bar(
    saldo_permanencia,
    x="faixa_permanencia",
    y="saldo_medio",
    color="tipo_pessoa",
    barmode="group",
    title="Saldo Devedor Médio por Tempo de Permanência",
    labels={
        "faixa_permanencia": "Tempo de Permanência",
        "saldo_medio": "Saldo Devedor Médio",
        "tipo_pessoa": "Tipo de Cliente"
    }
)

fig_saldo_permanencia.update_layout(
    xaxis_title="Tempo de Permanência",
    yaxis_title="Saldo Devedor Médio (R$)",
    legend_title="Tipo de Cliente"
)

st.plotly_chart(
    fig_saldo_permanencia,
    use_container_width=True
)