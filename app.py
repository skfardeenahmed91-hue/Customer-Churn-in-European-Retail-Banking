"""
European Bank | Customer Churn Analytics Dashboard
====================================================
Interactive Streamlit application accompanying the research paper
"Customer Churn Analytics in European Retail Banking".

Run locally with:
    pip install streamlit pandas numpy plotly
    streamlit run app.py

Data file `cleaned_segmented.csv` must sit alongside this script.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# Page configuration & global style
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="European Bank | Churn Analytics",
    page_icon="\U0001F3E6",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#1B2A4A"
NAVY_LIGHT = "#2E4470"
GOLD = "#C9A24B"
RED = "#B33A3A"
GREEN = "#3A7D5C"
GREY = "#6B7280"
LIGHT_BG = "#F7F8FA"

PALETTE = [NAVY, GOLD, RED, GREEN, "#5B7DB1", "#8A8F98"]

CUSTOM_CSS = f"""
<style>
    .main {{ background-color: {LIGHT_BG}; }}
    h1, h2, h3 {{ color: {NAVY}; font-family: 'Segoe UI', sans-serif; }}
    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid #E5E7EB;
        border-left: 5px solid {GOLD};
        border-radius: 8px;
        padding: 14px 18px 10px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    div[data-testid="stMetricLabel"] {{ color: {GREY}; font-weight: 600; }}
    div[data-testid="stMetricValue"] {{ color: {NAVY}; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: white; border-radius: 6px 6px 0 0; padding: 8px 18px;
    }}
    .banner {{
        background: linear-gradient(90deg, {NAVY} 0%, {NAVY_LIGHT} 100%);
        padding: 22px 28px; border-radius: 10px; margin-bottom: 18px;
    }}
    .banner h1 {{ color: white; margin: 0; font-size: 28px; }}
    .banner p {{ color: #D8DEEA; margin: 4px 0 0 0; font-size: 14px; }}
    .insight-box {{
        background-color: #FBF7ED; border-left: 5px solid {GOLD};
        border-radius: 6px; padding: 12px 16px; margin: 10px 0; font-size: 14px; color: #333;
    }}
    footer {{visibility: hidden;}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_segmented.csv")
    order_age = ["<30", "30-45", "46-60", "60+"]
    order_credit = ["Low (<580)", "Medium (580-740)", "High (>740)"]
    order_tenure = ["New (0-2 yrs)", "Mid-term (3-6 yrs)", "Long-term (7-10 yrs)"]
    order_balance = ["Zero-balance", "Low-balance (<100K)", "High-balance (>=100K)"]
    df["AgeGroup"] = pd.Categorical(df["AgeGroup"], categories=order_age, ordered=True)
    df["CreditScoreBand"] = pd.Categorical(df["CreditScoreBand"], categories=order_credit, ordered=True)
    df["TenureGroup"] = pd.Categorical(df["TenureGroup"], categories=order_tenure, ordered=True)
    df["BalanceSegment"] = pd.Categorical(df["BalanceSegment"], categories=order_balance, ordered=True)
    return df

df_full = load_data()

ORDER_AGE = ["<30", "30-45", "46-60", "60+"]
ORDER_CREDIT = ["Low (<580)", "Medium (580-740)", "High (>740)"]
ORDER_TENURE = ["New (0-2 yrs)", "Mid-term (3-6 yrs)", "Long-term (7-10 yrs)"]
ORDER_BALANCE = ["Zero-balance", "Low-balance (<100K)", "High-balance (>=100K)"]


# ----------------------------------------------------------------------------
# Sidebar filters (drive every KPI & chart on the page)
# ----------------------------------------------------------------------------
st.sidebar.markdown(f"## \U0001F3E6 European Bank")
st.sidebar.caption("Customer Churn Analytics \u2014 Filter Panel")
st.sidebar.markdown("---")

geo_sel = st.sidebar.multiselect("Geography", options=sorted(df_full["Geography"].unique()),
                                  default=sorted(df_full["Geography"].unique()))
gender_sel = st.sidebar.multiselect("Gender", options=sorted(df_full["Gender"].unique()),
                                     default=sorted(df_full["Gender"].unique()))
age_sel = st.sidebar.multiselect("Age Group", options=ORDER_AGE, default=ORDER_AGE)
credit_sel = st.sidebar.multiselect("Credit Score Band", options=ORDER_CREDIT, default=ORDER_CREDIT)
tenure_sel = st.sidebar.multiselect("Tenure Group", options=ORDER_TENURE, default=ORDER_TENURE)
balance_sel = st.sidebar.multiselect("Balance Segment", options=ORDER_BALANCE, default=ORDER_BALANCE)
products_sel = st.sidebar.multiselect("Number of Products", options=sorted(df_full["NumOfProducts"].unique()),
                                       default=sorted(df_full["NumOfProducts"].unique()))
activity_sel = st.sidebar.multiselect("Activity Status", options=sorted(df_full["ActivityStatus"].unique()),
                                       default=sorted(df_full["ActivityStatus"].unique()))
hv_sel = st.sidebar.multiselect("Customer Tier", options=sorted(df_full["HighValueCustomer"].unique()),
                                 default=sorted(df_full["HighValueCustomer"].unique()))

st.sidebar.markdown("---")
if st.sidebar.button("\U0001F504 Reset all filters"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: European Bank customer extract, n = 10,000. "
    "Companion to the *Customer Churn Analytics in European Retail Banking* research paper."
)

# Apply filters
df = df_full[
    df_full["Geography"].isin(geo_sel)
    & df_full["Gender"].isin(gender_sel)
    & df_full["AgeGroup"].astype(str).isin(age_sel)
    & df_full["CreditScoreBand"].astype(str).isin(credit_sel)
    & df_full["TenureGroup"].astype(str).isin(tenure_sel)
    & df_full["BalanceSegment"].astype(str).isin(balance_sel)
    & df_full["NumOfProducts"].isin(products_sel)
    & df_full["ActivityStatus"].isin(activity_sel)
    & df_full["HighValueCustomer"].isin(hv_sel)
].copy()

# ----------------------------------------------------------------------------
# Header banner
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="banner">
        <h1>\U0001F3E6 European Bank &mdash; Customer Churn Analytics</h1>
        <p>Segmentation-driven churn intelligence across France, Germany &amp; Spain &nbsp;|&nbsp;
        Live filtered view: <b>{len(df):,}</b> of {len(df_full):,} customers selected</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if len(df) == 0:
    st.warning("No customers match the current filter selection. Please broaden your filters in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------------
# Tabs (Core Modules)
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "\U0001F4CA  Overall Churn Summary",
    "\U0001F310  Geography Explorer",
    "\U0001F465  Age & Tenure Comparison",
    "\U0001F48E  High-Value Customer Explorer",
])

# ============================================================================
# TAB 1 — OVERALL CHURN SUMMARY
# ============================================================================
with tab1:
    total = len(df)
    churned = int(df["Exited"].sum())
    retained = total - churned
    churn_rate = churned / total * 100
    baseline_rate = df_full["Exited"].mean() * 100
    avg_balance_churn = df.loc[df["Exited"] == 1, "Balance"].mean() if churned else 0
    revenue_at_risk = df.loc[df["Exited"] == 1, "Balance"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Customers (filtered)", f"{total:,}")
    c2.metric("Churn Rate", f"{churn_rate:.2f}%",
               delta=f"{churn_rate - baseline_rate:+.2f} pp vs. full portfolio",
               delta_color="inverse")
    c3.metric("Churned Customers", f"{churned:,}")
    c4.metric("Retained Customers", f"{retained:,}")
    c5.metric("Balance at Risk (churned)", f"\u20ac{revenue_at_risk/1e6:,.1f}M")

    st.markdown("---")
    left, right = st.columns([1, 1.4])

    with left:
        st.subheader("Churn Composition")
        pie_df = pd.DataFrame({"Status": ["Retained", "Churned"], "Count": [retained, churned]})
        fig = px.pie(pie_df, names="Status", values="Count", hole=0.55,
                     color="Status", color_discrete_map={"Retained": NAVY, "Churned": RED})
        fig.update_traces(textinfo="percent+label", textfont_size=14)
        fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=340)
        st.plotly_chart(fig, width="stretch")

    with right:
        st.subheader("Churn Rate by Segment Dimension (filtered data)")
        dims = st.multiselect(
            "Compare churn rate across:",
            ["Geography", "Gender", "AgeGroup", "CreditScoreBand", "TenureGroup",
             "BalanceSegment", "ActivityStatus", "HighValueCustomer"],
            default=["Geography"],
            key="t1_dims",
        )
        if dims:
            dim = dims[0]
            order_map = {"AgeGroup": ORDER_AGE, "CreditScoreBand": ORDER_CREDIT,
                         "TenureGroup": ORDER_TENURE, "BalanceSegment": ORDER_BALANCE}
            g = df.groupby(dim, observed=True)["Exited"].agg(["count", "mean"]).reset_index()
            g["mean"] = g["mean"] * 100
            if dim in order_map:
                g[dim] = pd.Categorical(g[dim], categories=order_map[dim], ordered=True)
                g = g.sort_values(dim)
            else:
                g = g.sort_values("mean", ascending=False)
            fig2 = px.bar(g, x=dim, y="mean", text=g["mean"].round(1).astype(str) + "%",
                          color="mean", color_continuous_scale=[GREEN, GOLD, RED],
                          labels={"mean": "Churn Rate (%)"})
            fig2.add_hline(y=churn_rate, line_dash="dash", line_color=GREY,
                            annotation_text=f"Filtered avg {churn_rate:.1f}%", annotation_position="top left")
            fig2.update_traces(textposition="outside")
            fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340, coloraxis_showscale=False)
            st.plotly_chart(fig2, width="stretch")
        else:
            st.info("Select at least one dimension above to compare.")

    st.markdown("---")
    st.subheader("Segment Churn Table")
    dim2 = st.selectbox(
        "Segment dimension for detail table:",
        ["Geography", "Gender", "AgeGroup", "CreditScoreBand", "TenureGroup",
         "BalanceSegment", "NumOfProducts", "ActivityStatus", "HighValueCustomer"],
        key="t1_table_dim",
    )
    order_map2 = {"AgeGroup": ORDER_AGE, "CreditScoreBand": ORDER_CREDIT,
                  "TenureGroup": ORDER_TENURE, "BalanceSegment": ORDER_BALANCE}
    tbl = df.groupby(dim2, observed=True).agg(Customers=("CustomerId", "count"), Churned=("Exited", "sum")).reset_index()
    tbl["Churn Rate %"] = (tbl["Churned"] / tbl["Customers"] * 100).round(2)
    tbl["Share of Base %"] = (tbl["Customers"] / total * 100).round(2)
    tbl["Share of Churn %"] = (tbl["Churned"] / max(churned, 1) * 100).round(2)
    if dim2 in order_map2:
        tbl[dim2] = pd.Categorical(tbl[dim2], categories=order_map2[dim2], ordered=True)
        tbl = tbl.sort_values(dim2)
    else:
        tbl = tbl.sort_values("Churn Rate %", ascending=False)
    st.dataframe(tbl, width="stretch", hide_index=True)

    st.markdown(
        '<div class="insight-box">\U0001F4A1 <b>How to read this tab:</b> '
        'Churn Rate = % of customers within a segment who exited. '
        'Share of Churn = that segment\'s share of all churned customers &mdash; '
        'a segment can have a high churn rate but a small Share of Churn if it is a small group, '
        'and vice versa. Use both figures together when prioritising retention effort.</div>',
        unsafe_allow_html=True,
    )

# ============================================================================
# TAB 2 — GEOGRAPHY EXPLORER
# ============================================================================
with tab2:
    st.subheader("Churn Rate by Geography")
    geo_g = df.groupby("Geography", observed=True).agg(
        Customers=("CustomerId", "count"), Churned=("Exited", "sum")
    ).reset_index()
    geo_g["ChurnRate"] = geo_g["Churned"] / geo_g["Customers"] * 100
    overall_rate = df["Exited"].mean() * 100
    geo_g["RiskIndex"] = (geo_g["ChurnRate"] / overall_rate).round(2) if overall_rate > 0 else 0

    gc1, gc2 = st.columns([1.3, 1])
    with gc1:
        fig = px.bar(geo_g.sort_values("ChurnRate", ascending=False), x="Geography", y="ChurnRate",
                     text=geo_g.sort_values("ChurnRate", ascending=False)["ChurnRate"].round(1).astype(str) + "%",
                     color="Geography", color_discrete_sequence=[RED, GOLD, NAVY])
        fig.add_hline(y=overall_rate, line_dash="dash", line_color=GREY,
                       annotation_text=f"Filtered avg {overall_rate:.1f}%")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=380, margin=dict(t=10, b=10),
                           yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, width="stretch")
    with gc2:
        st.markdown("##### Geographic Risk Index")
        st.caption("Regional churn rate \u00f7 filtered portfolio average (1.0 = average risk)")
        fig_idx = go.Figure(go.Bar(
            x=geo_g["RiskIndex"], y=geo_g["Geography"], orientation="h",
            marker_color=[RED if v > 1 else GREEN for v in geo_g["RiskIndex"]],
            text=geo_g["RiskIndex"].astype(str) + "x", textposition="outside",
        ))
        fig_idx.add_vline(x=1.0, line_dash="dash", line_color=GREY)
        fig_idx.update_layout(height=380, margin=dict(t=10, b=10), xaxis_title="Risk Index")
        st.plotly_chart(fig_idx, width="stretch")

    st.markdown("---")
    st.subheader("Geography \u00d7 Age Interaction")
    pivot = df.pivot_table(index="Geography", columns="AgeGroup", values="Exited", aggfunc="mean", observed=True) * 100
    pivot = pivot.reindex(columns=[a for a in ORDER_AGE if a in pivot.columns])
    fig_hm = px.imshow(pivot, text_auto=".1f", color_continuous_scale="Reds",
                        labels=dict(color="Churn Rate (%)"), aspect="auto")
    fig_hm.update_layout(height=340, margin=dict(t=10, b=10))
    st.plotly_chart(fig_hm, width="stretch")

    st.markdown("---")
    st.subheader("Gender Gap by Geography")
    gg = df.groupby(["Geography", "Gender"], observed=True)["Exited"].mean().reset_index()
    gg["Exited"] = gg["Exited"] * 100
    fig_gg = px.bar(gg, x="Geography", y="Exited", color="Gender", barmode="group",
                     text=gg["Exited"].round(1).astype(str) + "%",
                     color_discrete_map={"Female": GOLD, "Male": NAVY})
    fig_gg.update_traces(textposition="outside")
    fig_gg.update_layout(height=360, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)")
    st.plotly_chart(fig_gg, width="stretch")

    st.markdown(
        '<div class="insight-box">\U0001F4A1 <b>Drill-down tip:</b> Use the sidebar Geography filter '
        'to isolate a single market, then revisit the Age &amp; Tenure tab to see how that market\'s '
        'age profile compares once other markets are excluded.</div>',
        unsafe_allow_html=True,
    )

# ============================================================================
# TAB 3 — AGE & TENURE COMPARISON
# ============================================================================
with tab3:
    ac1, ac2 = st.columns(2)

    with ac1:
        st.subheader("Churn Rate by Age Group")
        ag = df.groupby("AgeGroup", observed=True)["Exited"].agg(["count", "mean"]).reindex(ORDER_AGE).reset_index()
        ag = ag.dropna()
        ag["mean"] = ag["mean"] * 100
        fig_a = px.bar(ag, x="AgeGroup", y="mean", text=ag["mean"].round(1).astype(str) + "%",
                        color_discrete_sequence=[NAVY])
        fig_a.update_traces(textposition="outside", marker_color=NAVY)
        fig_a.update_layout(height=360, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig_a, width="stretch")

    with ac2:
        st.subheader("Churn Rate by Tenure Group")
        tg = df.groupby("TenureGroup", observed=True)["Exited"].agg(["count", "mean"]).reindex(ORDER_TENURE).reset_index()
        tg = tg.dropna()
        tg["mean"] = tg["mean"] * 100
        fig_t = px.bar(tg, x="TenureGroup", y="mean", text=tg["mean"].round(1).astype(str) + "%",
                        color_discrete_sequence=[GOLD])
        fig_t.update_traces(textposition="outside", marker_color=GOLD)
        fig_t.update_layout(height=360, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig_t, width="stretch")

    st.markdown("---")
    st.subheader("Age \u00d7 Tenure Heatmap")
    pivot2 = df.pivot_table(index="AgeGroup", columns="TenureGroup", values="Exited", aggfunc="mean", observed=True) * 100
    pivot2 = pivot2.reindex(index=[a for a in ORDER_AGE if a in pivot2.index],
                             columns=[t for t in ORDER_TENURE if t in pivot2.columns])
    fig_hm2 = px.imshow(pivot2, text_auto=".1f", color_continuous_scale="Reds",
                         labels=dict(color="Churn Rate (%)"), aspect="auto")
    fig_hm2.update_layout(height=340, margin=dict(t=10, b=10))
    st.plotly_chart(fig_hm2, width="stretch")

    st.markdown("---")
    st.subheader("Product Holding \u2014 the Strongest Predictor")
    pg = df.groupby("NumOfProducts")["Exited"].agg(["count", "mean"]).reset_index()
    pg["mean"] = pg["mean"] * 100
    fig_p = px.bar(pg, x="NumOfProducts", y="mean",
                    text=pg["mean"].round(1).astype(str) + "% (n=" + pg["count"].astype(str) + ")",
                    color="mean", color_continuous_scale=[GREEN, GOLD, RED])
    fig_p.update_traces(textposition="outside")
    fig_p.update_layout(height=380, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)",
                         xaxis_title="Number of Products Held", coloraxis_showscale=False)
    st.plotly_chart(fig_p, width="stretch")

    st.markdown(
        '<div class="insight-box">\U0001F4A1 <b>Key pattern:</b> churn is lowest among customers holding '
        'exactly two products and rises sharply at three or four products &mdash; a U-shaped relationship '
        'that a simple correlation coefficient does not reveal (see research paper, Section 6.9).</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("Engagement Drop Indicator")
    ec1, ec2 = st.columns([1, 1])
    with ec1:
        act = df.groupby("ActivityStatus")["Exited"].mean().reset_index()
        act["Exited"] = act["Exited"] * 100
        fig_act = px.bar(act, x="ActivityStatus", y="Exited", text=act["Exited"].round(1).astype(str) + "%",
                          color="ActivityStatus", color_discrete_map={"Active": GREEN, "Inactive": RED})
        fig_act.update_traces(textposition="outside")
        fig_act.update_layout(showlegend=False, height=320, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig_act, width="stretch")
    with ec2:
        inactive_rate = df.loc[df["ActivityStatus"] == "Inactive", "Exited"].mean() * 100 if "Inactive" in df["ActivityStatus"].values else 0
        active_rate = df.loc[df["ActivityStatus"] == "Active", "Exited"].mean() * 100 if "Active" in df["ActivityStatus"].values else 0
        st.metric("Inactive Member Churn", f"{inactive_rate:.2f}%")
        st.metric("Active Member Churn", f"{active_rate:.2f}%")
        st.metric("Engagement Gap", f"{inactive_rate - active_rate:+.2f} pp")

# ============================================================================
# TAB 4 — HIGH-VALUE CUSTOMER EXPLORER
# ============================================================================
with tab4:
    hv = df[df["HighValueCustomer"] == "High-Value"]
    std = df[df["HighValueCustomer"] == "Standard"]

    hv_rate = hv["Exited"].mean() * 100 if len(hv) else 0
    std_rate = std["Exited"].mean() * 100 if len(std) else 0
    hv_balance_at_risk = hv.loc[hv["Exited"] == 1, "Balance"].sum() if len(hv) else 0
    total_balance_at_risk = df.loc[df["Exited"] == 1, "Balance"].sum()

    h1, h2c, h3c, h4c = st.columns(4)
    h1.metric("High-Value Customers", f"{len(hv):,}", f"{len(hv)/max(len(df),1)*100:.1f}% of filtered base")
    h2c.metric("High-Value Churn Rate", f"{hv_rate:.2f}%",
               delta=f"{hv_rate - std_rate:+.2f} pp vs. Standard", delta_color="inverse")
    h3c.metric("High-Value Balance at Risk", f"\u20ac{hv_balance_at_risk/1e6:,.1f}M")
    h4c.metric("Share of Total Balance at Risk", f"{(hv_balance_at_risk/total_balance_at_risk*100) if total_balance_at_risk else 0:.1f}%")

    st.caption(
        "High-Value definition: account balance \u2265 66th percentile of the full portfolio "
        "AND estimated salary \u2265 median of the full portfolio."
    )

    st.markdown("---")
    vc1, vc2 = st.columns(2)
    with vc1:
        st.subheader("High-Value vs. Standard Churn")
        tier = df.groupby("HighValueCustomer")["Exited"].mean().reset_index()
        tier["Exited"] = tier["Exited"] * 100
        fig_tier = px.bar(tier, x="HighValueCustomer", y="Exited", text=tier["Exited"].round(1).astype(str) + "%",
                           color="HighValueCustomer", color_discrete_map={"High-Value": GOLD, "Standard": GREY})
        fig_tier.update_traces(textposition="outside")
        fig_tier.update_layout(showlegend=False, height=340, margin=dict(t=10, b=10), yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig_tier, width="stretch")
    with vc2:
        st.subheader("Balance Distribution: Churned vs. Retained")
        fig_box = px.box(df, x="ChurnStatus", y="Balance", color="ChurnStatus",
                          color_discrete_map={"Churned": RED, "Retained": NAVY})
        fig_box.update_layout(showlegend=False, height=340, margin=dict(t=10, b=10))
        st.plotly_chart(fig_box, width="stretch")

    st.markdown("---")
    st.subheader("Salary vs. Balance \u2014 Churn Signal Comparison")
    comp = pd.DataFrame({
        "Metric": ["Avg. Balance", "Avg. Balance", "Avg. Estimated Salary", "Avg. Estimated Salary"],
        "Status": ["Churned", "Retained", "Churned", "Retained"],
        "Value": [
            df.loc[df["Exited"] == 1, "Balance"].mean() if churned else 0,
            df.loc[df["Exited"] == 0, "Balance"].mean() if retained else 0,
            df.loc[df["Exited"] == 1, "EstimatedSalary"].mean() if churned else 0,
            df.loc[df["Exited"] == 0, "EstimatedSalary"].mean() if retained else 0,
        ],
    })
    fig_comp = px.bar(comp, x="Metric", y="Value", color="Status", barmode="group",
                       text=comp["Value"].round(0).apply(lambda v: f"\u20ac{v:,.0f}"),
                       color_discrete_map={"Churned": RED, "Retained": NAVY})
    fig_comp.update_traces(textposition="outside")
    fig_comp.update_layout(height=360, margin=dict(t=10, b=10), yaxis_title="Average (\u20ac)")
    st.plotly_chart(fig_comp, width="stretch")

    st.markdown(
        '<div class="insight-box">\U0001F4A1 <b>Why this matters:</b> Balance shows a meaningful gap between '
        'churned and retained customers; estimated salary does not. Balance &mdash; not income &mdash; is the '
        'more reliable signal for identifying at-risk premium customers (see research paper, Section 8.3).</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("High-Value Customer Drill-Down Table")
    hv_table = hv.sort_values("Balance", ascending=False)[
        ["CustomerId", "Geography", "Gender", "Age", "Balance", "EstimatedSalary",
         "NumOfProducts", "ActivityStatus", "TenureGroup", "ChurnStatus"]
    ]
    st.dataframe(hv_table, width="stretch", hide_index=True, height=320)

    csv = hv_table.to_csv(index=False).encode("utf-8")
    st.download_button("\U0001F4E5 Download High-Value customer list (CSV)", data=csv,
                        file_name="high_value_customers_filtered.csv", mime="text/csv")

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "European Bank Customer Churn Analytics Dashboard \u00b7 Companion to the Customer Churn Analytics in "
    "European Retail Banking research paper \u00b7 Data: European Bank customer extract (n = 10,000) \u00b7 "
    "Internal / stakeholder use."
)
