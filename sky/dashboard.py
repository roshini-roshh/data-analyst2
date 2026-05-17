import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SkyCity Auckland - Order Channel Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a237e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #546e7a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .kpi-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .risk-high {
        background-color: #ffebee;
        border-left: 4px solid #c62828;
        padding: 0.8rem;
        border-radius: 4px;
    }
    .risk-moderate {
        background-color: #fff8e1;
        border-left: 4px solid #f57f17;
        padding: 0.8rem;
        border-radius: 4px;
    }
    .risk-low {
        background-color: #e8f5e9;
        border-left: 4px solid #2e7d32;
        padding: 0.8rem;
        border-radius: 4px;
    }
    .channel-instore { color: #2196F3; font-weight: bold; }
    .channel-ue { color: #FF9800; font-weight: bold; }
    .channel-dd { color: #E91E63; font-weight: bold; }
    .channel-sd { color: #4CAF50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("sky/skycity_auckland_restaurants.csv")
    # Compute additional columns
    df["TotalDeliveryOrders"] = df["UberEatsOrdersCount"] + df["DoorDashOrdersCount"] + df["SelfDeliveryOrdersCount"]
    df["AggregatorDependence"] = df["UE_share"] + df["DD_share"]
    df["MaxAggregatorShare"] = df[["UE_share", "DD_share"]].max(axis=1)
    df["MaxChannelShare"] = df[["InStoreShare", "UE_share", "DD_share", "SD_share"]].max(axis=1)
    
    # Diversification Score
    def calc_div_score(row):
        shares = [row["InStoreShare"]/100, row["UE_share"]/100, row["DD_share"]/100, row["SD_share"]/100]
        entropy = 0
        for s in shares:
            if s > 0:
                entropy -= s * np.log2(s)
        return entropy / 2
    df["DiversificationScore"] = df.apply(calc_div_score, axis=1)
    
    # Risk category
    def risk_category(row):
        if row["MaxAggregatorShare"] >= 70:
            return "High Risk"
        elif row["MaxAggregatorShare"] >= 50:
            return "Moderate Risk"
        else:
            return "Low Risk"
    df["RiskCategory"] = df.apply(risk_category, axis=1)
    
    # Diversification category
    df["DivCategory"] = pd.cut(df["DiversificationScore"], bins=[0, 0.5, 0.75, 1.0],
                                labels=["Highly Concentrated", "Moderately Diversified", "Well Diversified"])
    
    # Net profit margins
    df["InStoreMargin"] = (df["InStoreNetProfit"] / df["InStoreRevenue"] * 100).round(1)
    df["UEMargin"] = (df["UberEatsNetProfit"] / df["UberEatsRevenue"] * 100).round(1)
    df["DDMargin"] = (df["DoorDashNetProfit"] / df["DoorDashRevenue"] * 100).round(1)
    df["SDMargin"] = (df["SelfDeliveryNetProfit"] / df["SelfDeliveryRevenue"] * 100).round(1)
    
    return df

df = load_data()

# Color scheme
CHANNEL_COLORS = {
    "In-Store": "#2196F3",
    "Uber Eats": "#FF9800",
    "DoorDash": "#E91E63",
    "Self-Delivery": "#4CAF50"
}

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.image("https://img.icons8.com/color/80/restaurant.png", width=60)
st.sidebar.title("🍽️ SkyCity Auckland")
st.sidebar.markdown("---")

# Filters
st.sidebar.subheader("🔍 Filters")

subregion_filter = st.sidebar.multiselect(
    "Select Subregion",
    options=sorted(df["Subregion"].unique()),
    default=sorted(df["Subregion"].unique())
)

cuisine_filter = st.sidebar.multiselect(
    "Select Cuisine Type",
    options=sorted(df["CuisineType"].unique()),
    default=sorted(df["CuisineType"].unique())
)

segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

channel_toggle = st.sidebar.radio(
    "Channel View",
    options=["All Channels", "In-Store Only", "Delivery Only"],
    index=0
)

# Apply filters
filtered_df = df[
    (df["Subregion"].isin(subregion_filter)) &
    (df["CuisineType"].isin(cuisine_filter)) &
    (df["Segment"].isin(segment_filter))
]

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🍽️ SkyCity Auckland Restaurants & Bars</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Order Channel Performance & Market Share Analytics</div>', unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
total_orders = filtered_df["MonthlyOrders"].sum()
total_revenue = filtered_df[["InStoreRevenue", "UberEatsRevenue", "DoorDashRevenue", "SelfDeliveryRevenue"]].sum().sum()
total_profit = filtered_df[["InStoreNetProfit", "UberEatsNetProfit", "DoorDashNetProfit", "SelfDeliveryNetProfit"]].sum().sum()
avg_div_score = filtered_df["DiversificationScore"].mean()
avg_agg_dep = filtered_df["AggregatorDependence"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{total_orders:,}</div><div class="kpi-label">Total Monthly Orders</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">${total_revenue:,.0f}</div><div class="kpi-label">Total Revenue</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">${total_profit:,.0f}</div><div class="kpi-label">Total Net Profit</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{avg_div_score:.3f}</div><div class="kpi-label">Avg Diversification Score</div></div>""", unsafe_allow_html=True)
with col5:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{avg_agg_dep:.1f}%</div><div class="kpi-label">Avg Aggregator Dependence</div></div>""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Channel Mix Overview",
    "🗺️ Subregion Analysis",
    "🍕 Cuisine & Segment Patterns",
    "⚠️ Dependency Risk",
    "💰 Profitability"
])

# ============================================================
# TAB 1: CHANNEL MIX OVERVIEW
# ============================================================
with tab1:
    st.subheader("📊 Channel Mix Overview Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Channel Order Share - Pie Chart
        channel_orders = {
            "In-Store": filtered_df["InStoreOrdersCount"].sum(),
            "Uber Eats": filtered_df["UberEatsOrdersCount"].sum(),
            "DoorDash": filtered_df["DoorDashOrdersCount"].sum(),
            "Self-Delivery": filtered_df["SelfDeliveryOrdersCount"].sum(),
        }
        if channel_toggle == "In-Store Only":
            channel_orders = {k: v for k, v in channel_orders.items() if k == "In-Store"}
        elif channel_toggle == "Delivery Only":
            channel_orders = {k: v for k, v in channel_orders.items() if k != "In-Store"}
        
        fig_pie = px.pie(
            values=list(channel_orders.values()),
            names=list(channel_orders.keys()),
            title="Channel Order Share (%)",
            color=list(channel_orders.keys()),
            color_discrete_map=CHANNEL_COLORS,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=13)
        fig_pie.update_layout(height=450, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Channel Revenue Share - Bar Chart
        channel_rev = {
            "In-Store": filtered_df["InStoreRevenue"].sum(),
            "Uber Eats": filtered_df["UberEatsRevenue"].sum(),
            "DoorDash": filtered_df["DoorDashRevenue"].sum(),
            "Self-Delivery": filtered_df["SelfDeliveryRevenue"].sum(),
        }
        if channel_toggle == "In-Store Only":
            channel_rev = {k: v for k, v in channel_rev.items() if k == "In-Store"}
        elif channel_toggle == "Delivery Only":
            channel_rev = {k: v for k, v in channel_rev.items() if k != "In-Store"}
        
        fig_bar = px.bar(
            x=list(channel_rev.keys()),
            y=list(channel_rev.values()),
            title="Channel Revenue ($)",
            color=list(channel_rev.keys()),
            color_discrete_map=CHANNEL_COLORS,
        )
        fig_bar.update_layout(
            xaxis_title="Channel",
            yaxis_title="Revenue ($)",
            showlegend=False,
            height=450,
            yaxis_tickformat="$,.0f"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Channel comparison table
    st.subheader("📋 Channel Performance Summary")
    
    channel_summary = pd.DataFrame({
        "Channel": ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"],
        "Orders": [
            filtered_df["InStoreOrdersCount"].sum(),
            filtered_df["UberEatsOrdersCount"].sum(),
            filtered_df["DoorDashOrdersCount"].sum(),
            filtered_df["SelfDeliveryOrdersCount"].sum()
        ],
        "Revenue ($)": [
            filtered_df["InStoreRevenue"].sum(),
            filtered_df["UberEatsRevenue"].sum(),
            filtered_df["DoorDashRevenue"].sum(),
            filtered_df["SelfDeliveryRevenue"].sum()
        ],
        "Net Profit ($)": [
            filtered_df["InStoreNetProfit"].sum(),
            filtered_df["UberEatsNetProfit"].sum(),
            filtered_df["DoorDashNetProfit"].sum(),
            filtered_df["SelfDeliveryNetProfit"].sum()
        ],
        "Profit Margin (%)": [
            round(filtered_df["InStoreNetProfit"].sum() / max(filtered_df["InStoreRevenue"].sum(), 1) * 100, 1),
            round(filtered_df["UberEatsNetProfit"].sum() / max(filtered_df["UberEatsRevenue"].sum(), 1) * 100, 1),
            round(filtered_df["DoorDashNetProfit"].sum() / max(filtered_df["DoorDashRevenue"].sum(), 1) * 100, 1),
            round(filtered_df["SelfDeliveryNetProfit"].sum() / max(filtered_df["SelfDeliveryRevenue"].sum(), 1) * 100, 1),
        ],
        "Avg AOV ($)": [
            round(filtered_df["InStoreRevenue"].sum() / max(filtered_df["InStoreOrdersCount"].sum(), 1), 2),
            round(filtered_df["UberEatsRevenue"].sum() / max(filtered_df["UberEatsOrdersCount"].sum(), 1), 2),
            round(filtered_df["DoorDashRevenue"].sum() / max(filtered_df["DoorDashOrdersCount"].sum(), 1), 2),
            round(filtered_df["SelfDeliveryRevenue"].sum() / max(filtered_df["SelfDeliveryOrdersCount"].sum(), 1), 2),
        ]
    })
    
    # Format for display
    display_summary = channel_summary.copy()
    display_summary["Orders"] = display_summary["Orders"].apply(lambda x: f"{x:,}")
    display_summary["Revenue ($)"] = display_summary["Revenue ($)"].apply(lambda x: f"${x:,.2f}")
    display_summary["Net Profit ($)"] = display_summary["Net Profit ($)"].apply(lambda x: f"${x:,.2f}")
    display_summary["Profit Margin (%)"] = display_summary["Profit Margin (%)"].apply(lambda x: f"{x}%")
    display_summary["Avg AOV ($)"] = display_summary["Avg AOV ($)"].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(display_summary, use_container_width=True, hide_index=True)
    
    # In-Store vs Delivery
    instore_total = filtered_df["InStoreOrdersCount"].sum()
    delivery_total = filtered_df["TotalDeliveryOrders"].sum()
    total = instore_total + delivery_total
    
    col1, col2 = st.columns(2)
    with col1:
        fig_gauge = go.Figure()
        fig_gauge.add_trace(go.Indicator(
            mode="gauge+number",
            value=round(instore_total/total*100, 1) if total > 0 else 0,
            title={'text': "In-Store Order Share (%)", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2196F3"},
                'steps': [
                    {'range': [0, 30], 'color': '#e3f2fd'},
                    {'range': [30, 60], 'color': '#bbdefb'},
                    {'range': [60, 100], 'color': '#90caf9'},
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 50}
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        fig_gauge2 = go.Figure()
        fig_gauge2.add_trace(go.Indicator(
            mode="gauge+number",
            value=round(delivery_total/total*100, 1) if total > 0 else 0,
            title={'text': "Delivery Order Share (%)", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FF9800"},
                'steps': [
                    {'range': [0, 30], 'color': '#fff3e0'},
                    {'range': [30, 60], 'color': '#ffe0b2'},
                    {'range': [60, 100], 'color': '#ffcc80'},
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
            }
        ))
        fig_gauge2.update_layout(height=300)
        st.plotly_chart(fig_gauge2, use_container_width=True)

# ============================================================
# TAB 2: SUBREGION ANALYSIS
# ============================================================
with tab2:
    st.subheader("🗺️ Subregion-wise Channel Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stacked bar - channel distribution by subregion
        sub_ch = filtered_df.groupby("Subregion").agg({
            "InStoreOrdersCount": "sum",
            "UberEatsOrdersCount": "sum",
            "DoorDashOrdersCount": "sum",
            "SelfDeliveryOrdersCount": "sum",
        }).reset_index()
        
        sub_ch_melted = sub_ch.melt(
            id_vars=["Subregion"],
            value_vars=["InStoreOrdersCount", "UberEatsOrdersCount", "DoorDashOrdersCount", "SelfDeliveryOrdersCount"],
            var_name="Channel",
            value_name="Orders"
        )
        sub_ch_melted["Channel"] = sub_ch_melted["Channel"].map({
            "InStoreOrdersCount": "In-Store",
            "UberEatsOrdersCount": "Uber Eats",
            "DoorDashOrdersCount": "DoorDash",
            "SelfDeliveryOrdersCount": "Self-Delivery"
        })
        
        fig_sub = px.bar(
            sub_ch_melted, x="Subregion", y="Orders", color="Channel",
            title="Order Volume by Subregion & Channel",
            color_discrete_map=CHANNEL_COLORS,
            barmode="stack"
        )
        fig_sub.update_layout(height=450, xaxis_tickangle=-30)
        st.plotly_chart(fig_sub, use_container_width=True)
    
    with col2:
        # Heatmap - percentage shares
        sub_ch_pct = filtered_df.groupby("Subregion").agg({
            "InStoreShare": "mean",
            "UE_share": "mean",
            "DD_share": "mean",
            "SD_share": "mean",
        }).reset_index()
        sub_ch_pct = sub_ch_pct.rename(columns={
            "InStoreShare": "In-Store", "UE_share": "Uber Eats",
            "DD_share": "DoorDash", "SD_share": "Self-Delivery"
        })
        
        fig_heat = px.imshow(
            sub_ch_pct.set_index("Subregion"),
            labels=dict(x="Channel", y="Subregion", color="Avg Share (%)"),
            title="Average Channel Share by Subregion (%)",
            color_continuous_scale="YlOrRd",
            text_auto=".1f"
        )
        fig_heat.update_layout(height=450)
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # Subregion comparison details
    st.subheader("📋 Subregion Channel Breakdown")
    for subregion in sorted(filtered_df["Subregion"].unique()):
        sub_df = filtered_df[filtered_df["Subregion"] == subregion]
        total_sub = sub_df["MonthlyOrders"].sum()
        
        with st.expander(f"📍 {subregion} — {total_sub:,} total monthly orders"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("In-Store", f"{sub_df['InStoreOrdersCount'].sum():,}", f"{sub_df['InStoreShare'].mean():.1f}%")
            with col2:
                st.metric("Uber Eats", f"{sub_df['UberEatsOrdersCount'].sum():,}", f"{sub_df['UE_share'].mean():.1f}%")
            with col3:
                st.metric("DoorDash", f"{sub_df['DoorDashOrdersCount'].sum():,}", f"{sub_df['DD_share'].mean():.1f}%")
            with col4:
                st.metric("Self-Delivery", f"{sub_df['SelfDeliveryOrdersCount'].sum():,}", f"{sub_df['SD_share'].mean():.1f}%")
    
    # Urban vs Suburban comparison
    st.subheader("🏙️ Urban vs Suburban Ordering Behavior")
    
    if "Central Auckland" in subregion_filter:
        urban_df = filtered_df[filtered_df["Subregion"] == "Central Auckland"]
        suburban_df = filtered_df[filtered_df["Subregion"] != "Central Auckland"]
        
        col1, col2 = st.columns(2)
        with col1:
            urban_delivery = urban_df["TotalDeliveryOrders"].sum()
            urban_total = urban_df["MonthlyOrders"].sum()
            fig_urban = px.pie(
                values=[urban_df["InStoreOrdersCount"].sum(), urban_delivery],
                names=["In-Store", "Delivery"],
                title=f"Central Auckland (Urban)<br>Delivery: {urban_delivery/urban_total*100:.1f}%",
                color=["In-Store", "Delivery"],
                color_discrete_map={"In-Store": "#2196F3", "Delivery": "#FF9800"},
                hole=0.4
            )
            fig_urban.update_layout(height=350)
            st.plotly_chart(fig_urban, use_container_width=True)
        
        with col2:
            sub_delivery = suburban_df["TotalDeliveryOrders"].sum()
            sub_total = suburban_df["MonthlyOrders"].sum()
            fig_suburban = px.pie(
                values=[suburban_df["InStoreOrdersCount"].sum(), sub_delivery],
                names=["In-Store", "Delivery"],
                title=f"Rest of Auckland (Suburban)<br>Delivery: {sub_delivery/sub_total*100:.1f}%",
                color=["In-Store", "Delivery"],
                color_discrete_map={"In-Store": "#2196F3", "Delivery": "#FF9800"},
                hole=0.4
            )
            fig_suburban.update_layout(height=350)
            st.plotly_chart(fig_suburban, use_container_width=True)
    else:
        st.info("Select 'Central Auckland' in the sidebar to see Urban vs Suburban comparison.")

# ============================================================
# TAB 3: CUISINE & SEGMENT PATTERNS
# ============================================================
with tab3:
    st.subheader("🍕 Cuisine & Segment Channel Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cuisine heatmap
        cuisine_ch = filtered_df.groupby("CuisineType").agg({
            "InStoreShare": "mean",
            "UE_share": "mean",
            "DD_share": "mean",
            "SD_share": "mean",
        }).reset_index()
        cuisine_ch = cuisine_ch.rename(columns={
            "InStoreShare": "In-Store", "UE_share": "Uber Eats",
            "DD_share": "DoorDash", "SD_share": "Self-Delivery"
        })
        
        fig_cuisine_heat = px.imshow(
            cuisine_ch.set_index("CuisineType"),
            labels=dict(x="Channel", y="Cuisine", color="Avg Share (%)"),
            title="Channel Share by Cuisine Type (%)",
            color_continuous_scale="Viridis",
            text_auto=".1f"
        )
        fig_cuisine_heat.update_layout(height=500)
        st.plotly_chart(fig_cuisine_heat, use_container_width=True)
    
    with col2:
        # Segment stacked bar
        seg_ch = filtered_df.groupby("Segment").agg({
            "InStoreShare": "mean",
            "UE_share": "mean",
            "DD_share": "mean",
            "SD_share": "mean",
        }).reset_index()
        seg_ch_melted = seg_ch.melt(
            id_vars=["Segment"],
            value_vars=["In-Store" if "In-Store" in seg_ch.columns else "InStoreShare",
                        "Uber Eats" if "Uber Eats" in seg_ch.columns else "UE_share",
                        "DoorDash" if "DoorDash" in seg_ch.columns else "DD_share",
                        "Self-Delivery" if "Self-Delivery" in seg_ch.columns else "SD_share"],
            var_name="Channel",
            value_name="Avg Share (%)"
        )
        # Rename columns properly
        seg_ch_melted2 = seg_ch.melt(id_vars=["Segment"], value_vars=["InStoreShare", "UE_share", "DD_share", "SD_share"],
                                     var_name="Channel", value_name="Avg Share (%)")
        seg_ch_melted2["Channel"] = seg_ch_melted2["Channel"].map({
            "InStoreShare": "In-Store", "UE_share": "Uber Eats",
            "DD_share": "DoorDash", "SD_share": "Self-Delivery"
        })
        
        fig_seg = px.bar(
            seg_ch_melted2, x="Segment", y="Avg Share (%)", color="Channel",
            title="Channel Mix by Segment",
            color_discrete_map=CHANNEL_COLORS,
            barmode="stack"
        )
        fig_seg.update_layout(height=500)
        st.plotly_chart(fig_seg, use_container_width=True)
    
    # Aggregator dependence by cuisine
    st.subheader("🔗 Aggregator Dependence by Cuisine Type")
    
    cuisine_agg = filtered_df.groupby("CuisineType")["AggregatorDependence"].mean().sort_values(ascending=True).reset_index()
    
    fig_agg = px.bar(
        cuisine_agg, x="AggregatorDependence", y="CuisineType",
        title="Average Aggregator Dependence by Cuisine (%)",
        color="AggregatorDependence",
        color_continuous_scale="Oranges",
        orientation='h'
    )
    fig_agg.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="High Risk (70%)")
    fig_agg.add_vline(x=50, line_dash="dash", line_color="orange", annotation_text="Moderate Risk (50%)")
    fig_agg.update_layout(height=450, yaxis_title="Cuisine Type", xaxis_title="Aggregator Dependence (%)")
    st.plotly_chart(fig_agg, use_container_width=True)
    
    # Cuisine-Channel detailed table
    st.subheader("📋 Cuisine-Channel Detailed Breakdown")
    cuisine_detail = filtered_df.groupby("CuisineType").agg({
        "MonthlyOrders": "sum",
        "InStoreShare": "mean",
        "UE_share": "mean",
        "DD_share": "mean",
        "SD_share": "mean",
        "AggregatorDependence": "mean",
        "DiversificationScore": "mean"
    }).round(2).sort_values("AggregatorDependence", ascending=False)
    cuisine_detail.columns = ["Total Orders", "In-Store %", "Uber Eats %", "DoorDash %", 
                               "Self-Delivery %", "Aggregator Dep. %", "Div. Score"]
    st.dataframe(cuisine_detail, use_container_width=True)

# ============================================================
# TAB 4: DEPENDENCY RISK
# ============================================================
with tab4:
    st.subheader("⚠️ Channel Dependency Risk Identification")
    
    # Risk summary
    high_risk_count = len(filtered_df[filtered_df["RiskCategory"] == "High Risk"])
    moderate_risk_count = len(filtered_df[filtered_df["RiskCategory"] == "Moderate Risk"])
    low_risk_count = len(filtered_df[filtered_df["RiskCategory"] == "Low Risk"])
    total_rest = len(filtered_df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="risk-high"><h3>🔴 High Risk (≥70% on one aggregator)</h3><h2>{high_risk_count} ({high_risk_count/total_rest*100:.1f}%)</h2></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="risk-moderate"><h3>🟡 Moderate Risk (50-69%)</h3><h2>{moderate_risk_count} ({moderate_risk_count/total_rest*100:.1f}%)</h2></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="risk-low"><h3>🟢 Low Risk (<50%)</h3><h2>{low_risk_count} ({low_risk_count/total_rest*100:.1f}%)</h2></div>""", unsafe_allow_html=True)
    
    # Diversification Score Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig_div = px.histogram(
            filtered_df, x="DiversificationScore",
            title="Channel Diversification Score Distribution",
            nbins=30,
            color_discrete_sequence=["#673AB7"]
        )
        fig_div.add_vline(x=filtered_df["DiversificationScore"].mean(), line_dash="dash", 
                          line_color="red", annotation_text=f"Mean: {filtered_df['DiversificationScore'].mean():.3f}")
        fig_div.update_layout(height=400, xaxis_title="Diversification Score (0=Concentrated, 1=Balanced)")
        st.plotly_chart(fig_div, use_container_width=True)
    
    with col2:
        # Max Channel Share Distribution
        fig_max = px.histogram(
            filtered_df, x="MaxChannelShare",
            title="Maximum Channel Share Distribution",
            nbins=30,
            color_discrete_sequence=["#FF5722"]
        )
        fig_max.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="High Risk (70%)")
        fig_max.update_layout(height=400, xaxis_title="Max Channel Share (%)")
        st.plotly_chart(fig_max, use_container_width=True)
    
    # Risk by subregion and cuisine
    col1, col2 = st.columns(2)
    
    with col1:
        risk_by_sub = filtered_df.groupby("Subregion")["AggregatorDependence"].mean().sort_values(ascending=False).reset_index()
        fig_risk_sub = px.bar(
            risk_by_sub, x="Subregion", y="AggregatorDependence",
            title="Avg Aggregator Dependence by Subregion",
            color="AggregatorDependence",
            color_continuous_scale="Reds"
        )
        fig_risk_sub.add_hline(y=70, line_dash="dash", line_color="red")
        fig_risk_sub.add_hline(y=50, line_dash="dash", line_color="orange")
        fig_risk_sub.update_layout(height=400, yaxis_title="Aggregator Dependence (%)")
        st.plotly_chart(fig_risk_sub, use_container_width=True)
    
    with col2:
        risk_by_cuisine = filtered_df.groupby("CuisineType")["AggregatorDependence"].mean().sort_values(ascending=False).reset_index()
        fig_risk_cuisine = px.bar(
            risk_by_cuisine, x="CuisineType", y="AggregatorDependence",
            title="Avg Aggregator Dependence by Cuisine",
            color="AggregatorDependence",
            color_continuous_scale="Oranges"
        )
        fig_risk_cuisine.add_hline(y=70, line_dash="dash", line_color="red")
        fig_risk_cuisine.add_hline(y=50, line_dash="dash", line_color="orange")
        fig_risk_cuisine.update_layout(height=400, xaxis_tickangle=-45, yaxis_title="Aggregator Dependence (%)")
        st.plotly_chart(fig_risk_cuisine, use_container_width=True)
    
    # Restaurant-level risk table
    st.subheader("📋 Restaurant Channel Risk Assessment")
    
    risk_table = filtered_df[["RestaurantName", "CuisineType", "Segment", "Subregion",
                               "InStoreShare", "UE_share", "DD_share", "SD_share",
                               "MaxChannelShare", "AggregatorDependence", "DiversificationScore", "RiskCategory"]].copy()
    risk_table = risk_table.sort_values("AggregatorDependence", ascending=False)
    risk_table.columns = ["Restaurant", "Cuisine", "Segment", "Subregion",
                           "In-Store %", "UE %", "DD %", "SD %",
                           "Max Channel %", "Agg. Dep. %", "Div. Score", "Risk"]
    
    st.dataframe(risk_table, use_container_width=True, hide_index=True)

# ============================================================
# TAB 5: PROFITABILITY
# ============================================================
with tab5:
    st.subheader("💰 Channel Profitability Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Net profit by channel
        profit_data = {
            "Channel": ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"],
            "Net Profit": [
                filtered_df["InStoreNetProfit"].sum(),
                filtered_df["UberEatsNetProfit"].sum(),
                filtered_df["DoorDashNetProfit"].sum(),
                filtered_df["SelfDeliveryNetProfit"].sum()
            ]
        }
        fig_profit = px.bar(
            profit_data, x="Channel", y="Net Profit",
            title="Net Profit by Channel",
            color="Channel",
            color_discrete_map=CHANNEL_COLORS
        )
        fig_profit.update_layout(height=400, yaxis_tickformat="$,.0f", showlegend=False)
        st.plotly_chart(fig_profit, use_container_width=True)
    
    with col2:
        # Profit margin by channel
        margin_data = {
            "Channel": ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"],
            "Profit Margin (%)": [
                round(filtered_df["InStoreNetProfit"].sum() / max(filtered_df["InStoreRevenue"].sum(), 1) * 100, 1),
                round(filtered_df["UberEatsNetProfit"].sum() / max(filtered_df["UberEatsRevenue"].sum(), 1) * 100, 1),
                round(filtered_df["DoorDashNetProfit"].sum() / max(filtered_df["DoorDashRevenue"].sum(), 1) * 100, 1),
                round(filtered_df["SelfDeliveryNetProfit"].sum() / max(filtered_df["SelfDeliveryRevenue"].sum(), 1) * 100, 1),
            ]
        }
        fig_margin = px.bar(
            margin_data, x="Channel", y="Profit Margin (%)",
            title="Net Profit Margin by Channel",
            color="Channel",
            color_discrete_map=CHANNEL_COLORS
        )
        fig_margin.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_margin, use_container_width=True)
    
    # Profit by segment
    st.subheader("📊 Profitability by Restaurant Segment")
    
    seg_profit = filtered_df.groupby("Segment").agg({
        "InStoreNetProfit": "sum",
        "UberEatsNetProfit": "sum",
        "DoorDashNetProfit": "sum",
        "SelfDeliveryNetProfit": "sum",
    }).reset_index()
    seg_profit_melted = seg_profit.melt(
        id_vars=["Segment"],
        value_vars=["InStoreNetProfit", "UberEatsNetProfit", "DoorDashNetProfit", "SelfDeliveryNetProfit"],
        var_name="Channel",
        value_name="Net Profit"
    )
    seg_profit_melted["Channel"] = seg_profit_melted["Channel"].map({
        "InStoreNetProfit": "In-Store",
        "UberEatsNetProfit": "Uber Eats",
        "DoorDashNetProfit": "DoorDash",
        "SelfDeliveryNetProfit": "Self-Delivery"
    })
    
    fig_seg_profit = px.bar(
        seg_profit_melted, x="Segment", y="Net Profit", color="Channel",
        title="Net Profit by Segment & Channel",
        color_discrete_map=CHANNEL_COLORS,
        barmode="group"
    )
    fig_seg_profit.update_layout(height=400, yaxis_tickformat="$,.0f")
    st.plotly_chart(fig_seg_profit, use_container_width=True)
    
    # Commission impact analysis
    st.subheader("💸 Commission Rate Impact on Profitability")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_scatter = px.scatter(
            filtered_df, x="CommissionRate", y="UEMargin",
            title="Commission Rate vs Uber Eats Profit Margin",
            color="Segment",
            hover_data=["RestaurantName", "CuisineType"],
            labels={"CommissionRate": "Commission Rate", "UEMargin": "UE Profit Margin (%)"}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_scatter2 = px.scatter(
            filtered_df, x="CommissionRate", y="DDMargin",
            title="Commission Rate vs DoorDash Profit Margin",
            color="Segment",
            hover_data=["RestaurantName", "CuisineType"],
            labels={"CommissionRate": "Commission Rate", "DDMargin": "DD Profit Margin (%)"}
        )
        fig_scatter2.update_layout(height=400)
        st.plotly_chart(fig_scatter2, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #78909c;'>
    <p>SkyCity Auckland Restaurants & Bars — Order Channel Performance & Market Share Analytics</p>
    <p>Data generated for analytical purposes | Dashboard built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
