import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# AJUSTE DA LARGURA
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1.5rem;
        }

        .criterio-box {
            padding: 18px;
            border-radius: 10px;
            border: 1px solid #d9d9d9;
            min-height: 150px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DADOS
# =========================================================

df = pd.read_csv(
    "data/clientes_segmentados_conquiste2.csv"
)


# =========================================================
# TÍTULO
# =========================================================

st.title("🎯 Construção da Segmentação Conquiste+")

st.markdown(
    """
    Esta página apresenta como a base original foi transformada em uma
    base analítica para definição do público da nova campanha
    **Conquiste+**, passando pela criação de variáveis, score,
    elegibilidade, segmentação e recomendação de produto.
    """
)

st.divider()


# =========================================================
# 1. VARIÁVEIS CRIADAS
# =========================================================

st.header("1. Variáveis criadas para a análise")

st.markdown(
    """
    A partir das informações disponíveis na base original foram criadas
    variáveis adicionais para representar **capacidade financeira,
    relacionamento, recência, histórico de cotas e propensão de compra**.
    """
)


# ---------------------------------------------------------
# TABELA DE EXPLICAÇÃO DAS NOVAS COLUNAS
# ---------------------------------------------------------

novas_colunas = pd.DataFrame(
    {
        "Coluna": [
            "qtd_cotas_total",
            "qtd_cotas_contempladas",
            "qtd_cotas_nao_contempladas",
            "vl_saldo_devedor_total",
            "tempo_relacionamento_anos",
            "tempo_medio_permanencia_meses",
            "faixa_renda",
            "recencia_dias",
            "faixa_recencia",
            "score_veiculos",
            "score_imoveis",
            "score_conquiste",
            "produto_recomendado",
            "elegivel",
            "segmento_conquiste"
        ],

        "Objetivo": [
            "Quantidade total de cotas associadas ao cliente",
            "Quantidade de cotas já contempladas",
            "Quantidade de cotas ainda não contempladas",
            "Saldo devedor consolidado do cliente",
            "Tempo total de relacionamento com a empresa",
            "Tempo médio de permanência nos consórcios",
            "Classificação da renda em faixas",
            "Dias desde a última compra",
            "Classificação da recência da última compra",
            "Score de propensão para Conquiste+ Veículos",
            "Score de propensão para Conquiste+ Imóveis",
            "Score principal utilizado na segmentação",
            "Produto indicado de acordo com os scores",
            "Indica se o cliente atende aos critérios mínimos",
            "Segmento final utilizado para priorização da campanha"
        ],

        "Dimensão": [
            "Engajamento",
            "Histórico",
            "Histórico",
            "Financeiro",
            "Relacionamento",
            "Relacionamento",
            "Financeiro",
            "Recência",
            "Recência",
            "Propensão",
            "Propensão",
            "Propensão",
            "Oferta",
            "Elegibilidade",
            "Campanha"
        ]
    }
)


with st.expander(
    "📋 Ver explicação das variáveis criadas",
    expanded=True
):

    st.dataframe(
        novas_colunas,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================================
# 2. ESTRUTURA DO SCORE
# =========================================================

st.header("2. Como foi construído o score")

st.markdown(
    """
    O score foi estruturado para representar diferentes dimensões do
    relacionamento do cliente com a empresa. O objetivo não é prever
    conversão com um modelo supervisionado, mas criar uma
    **priorização analítica inicial** para a campanha.
    """
)


# ---------------------------------------------------------
# PESOS
# ---------------------------------------------------------

pesos = pd.DataFrame(
    {
        "Critério": [
            "Capacidade Financeira",
            "Recência",
            "Engajamento / Cotas",
            "Relacionamento",
            "Afinidade com Produto"
        ],

        "Peso": [
            30,
            20,
            20,
            15,
            15
        ]
    }
)


fig_pesos = px.bar(
    pesos,
    x="Critério",
    y="Peso",
    text="Peso",
    title="Composição do Score Conquiste+",
    labels={
        "Peso": "Peso no Score (%)"
    }
)

fig_pesos.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

fig_pesos.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Participação no Score (%)",
    showlegend=False
)


# ---------------------------------------------------------
# DESCRIÇÃO DOS CRITÉRIOS
# ---------------------------------------------------------

col1, col2 = st.columns(
    [1.4, 1]
)


with col1:

    st.plotly_chart(
        fig_pesos,
        use_container_width=True
    )


with col2:

    st.markdown("### Critérios considerados")

    st.markdown(
        """
        **30% — Capacidade financeira**

        Renda mensal utilizada como proxy para capacidade de aquisição.

        **20% — Recência**

        Clientes com compras mais recentes recebem maior peso.

        **20% — Engajamento**

        Considera o histórico e quantidade de cotas.

        **15% — Relacionamento**

        Valoriza clientes com relacionamento mais consolidado.

        **15% — Afinidade**

        Considera o histórico do cliente com Veículos e Imóveis.
        """
    )


st.divider()


# =========================================================
# 3. SCORES SEPARADOS POR PRODUTO
# =========================================================

st.header("3. Propensão por produto")

st.markdown(
    """
    Foram mantidos **dois scores independentes** para que a mesma pessoa
    possa apresentar propensão diferente para Veículos e Imóveis.
    """
)


# ---------------------------------------------------------
# TRANSFORMAR SCORES PARA FORMATO LONGO
# ---------------------------------------------------------

scores_long = df[
    [
        "cod_cliente_ficticio",
        "tipo_pessoa",
        "score_veiculos",
        "score_imoveis"
    ]
].copy()


scores_long = scores_long.melt(
    id_vars=[
        "cod_cliente_ficticio",
        "tipo_pessoa"
    ],
    value_vars=[
        "score_veiculos",
        "score_imoveis"
    ],
    var_name="Produto",
    value_name="Score"
)


scores_long["Produto"] = (
    scores_long["Produto"]
    .replace(
        {
            "score_veiculos": "Veículos",
            "score_imoveis": "Imóveis"
        }
    )
)


# ---------------------------------------------------------
# BOXPLOT
# ---------------------------------------------------------

fig_scores = px.box(
    scores_long,
    x="Produto",
    y="Score",
    color="tipo_pessoa",
    title="Distribuição dos Scores por Produto e Tipo de Cliente",
    labels={
        "tipo_pessoa": "Tipo de Cliente"
    }
)

fig_scores.update_layout(
    height=520,
    xaxis_title="Produto",
    yaxis_title="Score",
    legend_title="Tipo de Cliente"
)


st.plotly_chart(
    fig_scores,
    use_container_width=True
)


st.info(
    """
    O score de Veículos e o score de Imóveis permanecem separados.
    Dessa forma, um cliente pode possuir maior aderência a um produto
    mesmo apresentando menor aderência ao outro.
    """
)


st.divider()


# =========================================================
# 4. ELEGIBILIDADE
# =========================================================

st.header("4. Critérios de elegibilidade")

st.markdown(
    """
    Antes da priorização pelo score, foram aplicados critérios básicos
    para evitar direcionar a campanha para perfis considerados
    inadequados para a ação inicial.
    """
)


# ---------------------------------------------------------
# CARDS DOS CRITÉRIOS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        <div class="criterio-box">
            <h4>✓ Adimplência</h4>
            <p>Priorizar clientes em situação regular.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="criterio-box">
            <h4>✓ Sem cancelamentos</h4>
            <p>Histórico sem cotas canceladas como critério de segurança.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="criterio-box">
            <h4>✓ Renda válida</h4>
            <p>Existência de informação financeira utilizável.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        """
        <div class="criterio-box">
            <h4>✓ Relacionamento</h4>
            <p>Recência e histórico considerados na priorização.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# ELEGÍVEIS X NÃO ELEGÍVEIS
# ---------------------------------------------------------

elegibilidade = (
    df
    .groupby("elegivel")
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


elegibilidade["Status"] = elegibilidade[
    "elegivel"
].replace(
    {
        True: "Elegível",
        False: "Não Elegível"
    }
)


fig_elegibilidade = px.pie(
    elegibilidade,
    names="Status",
    values="clientes",
    hole=0.55,
    title="Clientes Elegíveis para a Campanha"
)

fig_elegibilidade.update_traces(
    textinfo="percent+label+value"
)


st.plotly_chart(
    fig_elegibilidade,
    use_container_width=True
)


st.divider()


# =========================================================
# 5. SEGMENTAÇÃO FINAL
# =========================================================

st.header("5. Segmentação dos clientes")

st.markdown(
    """
    Após a elegibilidade, os clientes foram distribuídos em quatro
    segmentos. O score determina o nível de prioridade comercial.
    """
)


# ---------------------------------------------------------
# CRITÉRIOS DA SEGMENTAÇÃO
# ---------------------------------------------------------

criterios_segmentacao = pd.DataFrame(
    {
        "Segmento": [
            "Alta prioridade",
            "Potencial",
            "Nutrição",
            "Não prioritário"
        ],

        "Regra": [
            "Elegível e Score ≥ 80",
            "Elegível e Score ≥ 65",
            "Elegível e Score < 65",
            "Não elegível"
        ],

        "Estratégia": [
            "Abordagem comercial prioritária",
            "CRM, WhatsApp e e-mail",
            "Nutrição e remarketing",
            "Fora da primeira onda da campanha"
        ]
    }
)


st.dataframe(
    criterios_segmentacao,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# DISTRIBUIÇÃO DOS SEGMENTOS
# ---------------------------------------------------------

segmentos = (
    df
    .groupby("segmento_conquiste")
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


ordem_segmentos = [
    "Alta prioridade",
    "Potencial",
    "Nutrição",
    "Não prioritário"
]


segmentos["segmento_conquiste"] = pd.Categorical(
    segmentos["segmento_conquiste"],
    categories=ordem_segmentos,
    ordered=True
)


segmentos = segmentos.sort_values(
    "segmento_conquiste"
)


fig_segmentos = px.bar(
    segmentos,
    x="segmento_conquiste",
    y="clientes",
    text="clientes",
    title="Distribuição dos Clientes por Segmento",
    labels={
        "segmento_conquiste": "Segmento",
        "clientes": "Quantidade de Clientes"
    }
)

fig_segmentos.update_traces(
    textposition="outside"
)

fig_segmentos.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Clientes",
    showlegend=False
)


st.plotly_chart(
    fig_segmentos,
    use_container_width=True
)


st.divider()


# =========================================================
# 6. SCORE POR SEGMENTO
# =========================================================

st.header("6. Separação dos segmentos pelo score")


fig_score_segmento = px.box(
    df,
    x="segmento_conquiste",
    y="score_conquiste",
    color="segmento_conquiste",
    category_orders={
        "segmento_conquiste": ordem_segmentos
    },
    title="Distribuição do Score Conquiste+ por Segmento",
    labels={
        "segmento_conquiste": "Segmento",
        "score_conquiste": "Score Conquiste+"
    }
)


fig_score_segmento.update_layout(
    height=550,
    xaxis_title="",
    yaxis_title="Score Conquiste+",
    showlegend=False
)


st.plotly_chart(
    fig_score_segmento,
    use_container_width=True
)


st.divider()


# =========================================================
# 7. PRODUTO RECOMENDADO
# =========================================================

st.header("7. Qual produto oferecer?")

st.markdown(
    """
    Depois da classificação do cliente, os scores específicos de
    Veículos e Imóveis são utilizados para definir a oferta mais
    aderente ao perfil.
    """
)


produto_recomendado = (
    df
    .groupby("produto_recomendado")
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


fig_produto = px.pie(
    produto_recomendado,
    names="produto_recomendado",
    values="clientes",
    hole=0.50,
    title="Produto Recomendado para a Campanha"
)

fig_produto.update_traces(
    textinfo="percent+label"
)


st.plotly_chart(
    fig_produto,
    use_container_width=True
)


# ---------------------------------------------------------
# CRÉDITOS DA NOVA CAMPANHA
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.success(
        """
        🚗 **Conquiste+ Veículos**

        Faixa de crédito considerada:

        **R$ 100 mil a R$ 200 mil**
        """
    )


with col2:

    st.success(
        """
        🏠 **Conquiste+ Imóveis**

        Faixa de crédito considerada:

        **R$ 200 mil a R$ 400 mil**
        """
    )


st.divider()


# =========================================================
# 8. PÚBLICO ESCOLHIDO
# =========================================================

st.header("8. Público escolhido para a primeira onda")

st.markdown(
    """
    Para a primeira campanha, o foco principal é o segmento
    **Alta prioridade**, formado por clientes elegíveis e com
    maior score de propensão.

    Esse público representa o grupo com maior aderência aos critérios
    definidos e pode ser utilizado como primeira audiência para testar
    a campanha antes de ampliar a comunicação para os segmentos
    Potencial e Nutrição.
    """
)


# ---------------------------------------------------------
# BASE ALTA PRIORIDADE
# ---------------------------------------------------------

publico_alta = df[
    df["segmento_conquiste"]
    == "Alta prioridade"
].copy()


# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

total_alta = publico_alta[
    "cod_cliente_ficticio"
].nunique()


renda_alta = publico_alta[
    "vl_renda_mensal"
].mean()


score_alta = publico_alta[
    "score_conquiste"
].mean()


tempo_alta = publico_alta[
    "tempo_relacionamento_anos"
].mean()


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Clientes Alta Prioridade",
    f"{total_alta:,}".replace(",", ".")
)


col2.metric(
    "Renda Média",
    f"R$ {renda_alta:,.0f}"
)


col3.metric(
    "Score Médio",
    f"{score_alta:.1f}"
)


col4.metric(
    "Relacionamento Médio",
    f"{tempo_alta:.1f} anos"
)


# =========================================================
# PF X PJ NO PÚBLICO ESCOLHIDO
# =========================================================

perfil_alta = (
    publico_alta
    .groupby(
        [
            "tipo_pessoa",
            "produto_recomendado"
        ]
    )
    ["cod_cliente_ficticio"]
    .nunique()
    .reset_index(name="clientes")
)


fig_perfil_alta = px.bar(
    perfil_alta,
    x="tipo_pessoa",
    y="clientes",
    color="produto_recomendado",
    barmode="stack",
    text_auto=True,
    title="Composição do Público de Alta Prioridade",
    labels={
        "tipo_pessoa": "Tipo de Cliente",
        "clientes": "Quantidade de Clientes",
        "produto_recomendado": "Produto Recomendado"
    }
)


fig_perfil_alta.update_layout(
    height=520,
    xaxis_title="Tipo de Cliente",
    yaxis_title="Clientes",
    legend_title="Oferta"
)


st.plotly_chart(
    fig_perfil_alta,
    use_container_width=True
)


st.divider()


# =========================================================
# 9. TABELA FINAL - VISÃO DE ALTO NÍVEL
# =========================================================

st.header("9. Visão de alto nível do público prioritário")

st.markdown(
    """
    Resumo do público selecionado para facilitar o direcionamento
    da primeira onda da campanha.
    """
)


# ---------------------------------------------------------
# AGREGAÇÃO
# ---------------------------------------------------------

tabela_publico = (
    publico_alta
    .groupby(
        [
            "tipo_pessoa",
            "produto_recomendado"
        ]
    )
    .agg(
        clientes=(
            "cod_cliente_ficticio",
            "nunique"
        ),

        renda_media=(
            "vl_renda_mensal",
            "mean"
        ),

        score_medio=(
            "score_conquiste",
            "mean"
        ),

        score_veiculos_medio=(
            "score_veiculos",
            "mean"
        ),

        score_imoveis_medio=(
            "score_imoveis",
            "mean"
        ),

        relacionamento_medio_anos=(
            "tempo_relacionamento_anos",
            "mean"
        ),

        permanencia_media_meses=(
            "tempo_medio_permanencia_meses",
            "mean"
        ),

        saldo_devedor_medio=(
            "vl_saldo_devedor_total",
            "mean"
        )
    )
    .reset_index()
)


# ---------------------------------------------------------
# RENOMEAR
# ---------------------------------------------------------

tabela_publico = tabela_publico.rename(
    columns={
        "tipo_pessoa":
            "Tipo",

        "produto_recomendado":
            "Produto Recomendado",

        "clientes":
            "Clientes",

        "renda_media":
            "Renda Média",

        "score_medio":
            "Score Médio",

        "score_veiculos_medio":
            "Score Veículos",

        "score_imoveis_medio":
            "Score Imóveis",

        "relacionamento_medio_anos":
            "Relacionamento Médio (anos)",

        "permanencia_media_meses":
            "Permanência Média (meses)",

        "saldo_devedor_medio":
            "Saldo Devedor Médio"
    }
)


# ---------------------------------------------------------
# FORMATAR PARA EXIBIÇÃO
# ---------------------------------------------------------

tabela_exibicao = tabela_publico.copy()


tabela_exibicao["Renda Média"] = (
    tabela_exibicao["Renda Média"]
    .map(
        lambda x: f"R$ {x:,.2f}"
    )
)


tabela_exibicao["Saldo Devedor Médio"] = (
    tabela_exibicao[
        "Saldo Devedor Médio"
    ]
    .map(
        lambda x: f"R$ {x:,.2f}"
    )
)


for coluna in [
    "Score Médio",
    "Score Veículos",
    "Score Imóveis",
    "Relacionamento Médio (anos)",
    "Permanência Média (meses)"
]:

    tabela_exibicao[coluna] = (
        tabela_exibicao[coluna]
        .round(1)
    )


st.dataframe(
    tabela_exibicao,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CONCLUSÃO
# =========================================================

st.divider()

st.subheader("📌 Estratégia sugerida")

st.markdown(
    """
    **1. Alta prioridade**

    Primeira onda da campanha, com abordagem comercial mais direta.

    **2. Potencial**

    Segunda onda após avaliação dos resultados iniciais.

    **3. Nutrição**

    Trabalhar relacionamento, conteúdo e remarketing antes de uma
    oferta mais direta.

    **4. Não prioritário**

    Não incluir na primeira ação comercial.
    """
)