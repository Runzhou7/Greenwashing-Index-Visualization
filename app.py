import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================
# 网页设置
# =========================
st.set_page_config(
    page_title="Global Distribution of Climate Commitments and Greenwashing",
    layout="wide"
)



st.title("🌍 Global Distribution of Climate Commitments and Greenwashing")
# =========================
# Introduction
# =========================

st.markdown("---")

st.markdown(
    """
    **Introduction**  
    
    Greenwashing refers to the practice where firms exaggerate or misrepresent their environmental 
    performance or climate commitments to appear more sustainable than they actually are.
    This can mislead investors, regulators, and the public, potentially undermining 
    genuine sustainability efforts and causing financial and reputational risks.
    """
)
# =========================
# Map Description
# =========================
st.markdown(
    """
    These interactive maps show the cross-country distribution of the following indices:

    •  **Climate Commitment Intensity Index (CCII)**  
    Measures the intensity of corporate climate commitments based on CDP disclosures.

    •  **GWE (Greenwashing based on E-score)**  
    Measures greenwashing behavior using environmental scores.

    •  **GWGHG (Greenwashing based on carbon emissions)**  
    Measures greenwashing behavior using firms' Scope 1 2 and 3 greenhouse gas emissions.

    In addition to the global map, users can also explore:

    •  **Top 10 Countries by Climate Commitment and Greenwashing Indices**  
    This section highlights the leading countries each year in terms of climate commitment (CCII) and potential greenwashing behavior (GWE and GWGHG), allowing users to track which countries are setting ambitious climate commitments and which may exhibit symbolic or formalistic disclosures.

    •  **Industry-level Climate Commitment vs Greenwashing**  
    This animated scatter plot visualizes industries' climate commitment (CCII) against greenwashing intensity (GWE or GWGHG) over time. The four-quadrant layout helps identify industries with substantive commitments versus symbolic or potentially greenwashing behavior, enabling a clear comparison of commitment and actual performance across sectors.


    These indices were developed using the state-of-the-art **[ClimateBERT Large Language Model](https://www.chatclimate.ai/climatebert)**
    combined with **[CDP Questionnaires](https://www.cdp.net/en)** from the world's largest greenhouse gas disclosure organization.
     
    For detailed methodology on index construction, please refer to our forthcoming paper:  
    *Climate Commitments, Greenwashing, and Regulation: Global Evidence from Natural Language Processing Based Indices*. 

    We believe this information can be useful for regulatory authorities as well as investors interested in greenwashing.
    """
)

st.markdown("---")
st.markdown("""
    **Authors:** [Runzhou Zheng](https://profiles.cardiff.ac.uk/staff/zhengr16), Qian Li, and Asma Mobarek  
    **Email:** zhengr16@cardiff.ac.uk  
    **LinkedIn:** [Runzhou Zheng](https://www.linkedin.com/in/runzhou-zheng-660a11293/)
    """)


# =========================
# 三个指数的全球图
# =========================
st.markdown("---")
st.subheader("🌍 Global Climate Commitment and Greenwashing Indices")

# =========================
# 读取数据
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("countrylevel.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# =========================
# 指标选择模块
# =========================
indicator = st.radio(
    "Select Indicator:",
    ("CCII", "GWE", "GWGHG"),
    horizontal=True
)

# =========================
# 指标配置（核心）
# =========================
indicator_config = {
    "CCII": {
        "column": "ccii",
        "title": "Climate Commitment Intensity Index (CCII)",
        "colorscale": ["#cce6ff", "#3399ff", "#003366"]  # 蓝
    },
    "GWE": {
        "column": "gwe",
        "title": "Greenwashing based on Environmental Score (GWE)",
        "colorscale": ["#d9f2d9", "#4caf50", "#1b5e20"]  # 绿
    },
    "GWGHG": {
        "column": "gwghg",
        "title": "Greenwashing based on Carbon Emissions (GWGHG)",
        "colorscale": ["#f5cccc", "#e53935", "#7f0000"]  # 红
    }
}

col = indicator_config[indicator]["column"]
title_name = indicator_config[indicator]["title"]
scale = indicator_config[indicator]["colorscale"]

# =========================
# 用户选择模式
# =========================
mode = st.radio(
    "Display Mode:",
    ("Single Year", "Animate Over Years")
)

# =========================
# 单年份地图
# =========================
if mode == "Single Year":
    year = st.selectbox(
        "Select Year",
        sorted(df["year"].unique())
    )
    df_plot = df[df["year"] == year]

    fig = px.choropleth(
        df_plot,
        locations="country",
        locationmode="country names",
        color=col,
        color_continuous_scale=scale,
        hover_name="country",
        hover_data={
            "year": True,
            col: True
        },
        title=f"Global Distribution of {title_name} ({year})"
    )

# =========================
# 动画地图
# =========================
else:
    fig = px.choropleth(
        df,
        locations="country",
        locationmode="country names",
        color=col,
        color_continuous_scale=scale,
        hover_name="country",
        hover_data={
            "year": True,
            col: True
        },
        animation_frame="year",
        title=f"Global Distribution of {title_name} (Animated)"
    )

# =========================
# 统一暗色风格
# =========================
fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
    coloraxis_colorbar=dict(
        title=indicator
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
Hover over the colored block to view the specific parameters.
""")


# =========================
# Top 10 CCII, GWE, GWGHG排名
# =========================
st.markdown("---")
st.subheader("📈 Top 10 Countries by Climate Commitment and Greenwashing Indices")

metric_map = {
    "Climate Commitment Intensity Index (CCII)": "ccii",
    "Greenwashing Index (GWE)": "gwe",
    "Greenwashing Index (GWGHG)": "gwghg"
}

metric_label = st.selectbox(
    "Select Index:",
    list(metric_map.keys())
)

metric = metric_map[metric_label]

df_rank = df.copy()

df_rank["rank"] = (
    df_rank
    .groupby("year")[metric]
    .rank(method="first", ascending=False)
)

df_rank = df_rank[df_rank["rank"] <= 10]
df_rank = df_rank.sort_values(["country", "year"])

fig_bump = px.line(
    df_rank,
    x="year",
    y="rank",
    color="country",
    markers=True,
    title=f"Top 10 Countries by {metric_label} Over Time"
)

fig_bump.update_yaxes(
    autorange="reversed",
    title="Rank (1 = Highest)"
)

fig_bump.update_xaxes(title="Year")

fig_bump.update_layout(
    height=650,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
    legend_title_text="Country",
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig_bump, use_container_width=True)

st.markdown(f"""
Hover over the colored block to view the specific parameters.
""")

# =========================
# 行业层面漂绿 vs 承诺分析（带四象限标注和文字说明）
# =========================

@st.cache_data
def load_industry_data():
    df_ind = pd.read_csv("industrylevel.csv")
    df_ind["year"] = df_ind["year"].astype(int)
    return df_ind

df_ind = load_industry_data()

st.markdown("---")
st.subheader("🏭 Industry-level Climate Commitment vs Greenwashing")

# =========================
# 选择漂绿指标
# =========================
color_metric_map = {
    "Greenwashing Index (GWE)": "gwe",
    "Greenwashing Index (GWGHG)": "gwghg"
}
color_label = st.selectbox(
    "Select Greenwashing Measure for Y-axis:",
    list(color_metric_map.keys()),
    key="industry_scatter_quadrant"
)
y_metric = color_metric_map[color_label]

# =========================
# 绘制动画散点图
# =========================
fig = px.scatter(
    df_ind,
    x="ccii",
    y=y_metric,
    color=y_metric,
    text="industry",
    animation_frame="year",
    color_continuous_scale="RdYlGn_r",
    title=f"Industry CCII vs {color_label} (Animated)"
)

fig.update_traces(
    textposition="top center",
    marker=dict(size=14, line=dict(width=1, color="white"))
)

# =========================
# 添加中心十字线
# =========================
x_center = 0  # CCII 基准
y_center = df_ind[y_metric].mean()  # 漂绿均值

fig.add_shape(type="line", x0=x_center, x1=x_center,
              y0=df_ind[y_metric].min(), y1=df_ind[y_metric].max(),
              line=dict(color="white", dash="dash"))
fig.add_shape(type="line", x0=df_ind["ccii"].min(), x1=df_ind["ccii"].max(),
              y0=y_center, y1=y_center,
              line=dict(color="white", dash="dash"))

# =========================
# 四象限标注文字
# =========================
annotations = [
    dict(x=df_ind["ccii"].max()*0.6, y=df_ind[y_metric].max()*0.9,
         text="High CCII<br>High Greenwashing<br>(Symbolic Commitment)",
         showarrow=False, font=dict(color="white", size=12), align="center"),
    dict(x=df_ind["ccii"].min()*0.6, y=df_ind[y_metric].max()*0.9,
         text="Low CCII<br>High Greenwashing<br>(Formalist / Passive)",
         showarrow=False, font=dict(color="white", size=12), align="center"),
    dict(x=df_ind["ccii"].min()*0.6, y=df_ind[y_metric].min()*0.9,
         text="Low CCII<br>Low Greenwashing<br>(Low-risk Industry)",
         showarrow=False, font=dict(color="white", size=12), align="center"),
    dict(x=df_ind["ccii"].max()*0.6, y=df_ind[y_metric].min()*0.9,
         text="High CCII<br>Low Greenwashing<br>(Substantive Commitment)",
         showarrow=False, font=dict(color="white", size=12), align="center"),
]
fig.update_layout(annotations=annotations)

# =========================
# 图布局
# =========================
fig.update_layout(
    height=650,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
    xaxis_title="Climate Commitment Intensity Index (CCII)",
    yaxis_title=color_label,
    margin=dict(l=40, r=40, t=60, b=40),
    coloraxis_colorbar=dict(title=color_label)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 图下方文字说明
# =========================
st.markdown(f"""
This chart shows the relationship between climate commitment (CCII) and greenwashing indices across industries over time.  
The plot is divided into four quadrants by the dashed lines:
- **Top-right**: High CCII & High Greenwashing → Symbolic commitments, potential greenwashing.  
- **Top-left**: Low CCII & High Greenwashing → Formally disclosed but passive, potential formalism.  
- **Bottom-left**: Low CCII & Low Greenwashing → Low-risk industries.  
- **Bottom-right**: High CCII & Low Greenwashing → Substantive commitments, good alignment of promise and performance.  

Use the animation to see how industries move across quadrants over years.
""")


st.markdown("---")

# =========================
# 计数器
# =========================

st.subheader("Do you like these maps? ⭐")

# 初始化计数器
if "like_count" not in st.session_state:
    st.session_state.like_count = 0
if "star_count" not in st.session_state:
    st.session_state.star_count = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("⭐ Like"):
        st.session_state.like_count += 1
    st.write(f"Likes: {st.session_state.like_count}")

with col2:
    if st.button("⭐⭐ Really Like"):
        st.session_state.star_count += 1
    st.write(f"Really Likes: {st.session_state.star_count}")

st.markdown("---")

# =========================
# References
# =========================
st.markdown(
    """
    **References**  
    Zheng, R., Li, Q., & Mobarek, A. (2026). *Climate Commitments, Greenwashing, and Regulation: Global Evidence from Natural Language Processing Based Indices* (Working Paper).  
    """
)


