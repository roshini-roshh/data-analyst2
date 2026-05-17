import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

df = pd.read_csv("skycity_auckland_restaurants.csv")

# Create output directory for charts
os.makedirs("charts", exist_ok=True)

# ============================================================
# DATA VALIDATION & CONSISTENCY CHECKS
# ============================================================
print("=" * 80)
print("DATA VALIDATION & CONSISTENCY CHECKS")
print("=" * 80)

# Check channel order counts sum
df["ComputedTotal"] = df["InStoreOrdersCount"] + df["UberEatsOrdersCount"] + df["DoorDashOrdersCount"] + df["SelfDeliveryOrdersCount"]
df["OrderDiff"] = df["ComputedTotal"] - df["MonthlyOrders"]
order_match = (df["OrderDiff"] == 0).all()
print(f"\n1. Channel orders sum to MonthlyOrders: {order_match}")
if not order_match:
    print(f"   Mismatches: {(df['OrderDiff'] != 0).sum()} records")
    print(f"   Max difference: {df['OrderDiff'].abs().max()}")

# Check share percentages sum
df["ShareSum"] = df["InStoreShare"] + df["UE_share"] + df["DD_share"] + df["SD_share"]
share_check = ((df["ShareSum"] >= 99.5) & (df["ShareSum"] <= 100.5)).all()
print(f"\n2. Channel shares sum to ~100%: {share_check}")
print(f"   Share sum range: {df['ShareSum'].min():.2f}% - {df['ShareSum'].max():.2f}%")

# Identify outliers using IQR
print("\n3. Outlier Detection (IQR Method):")
numeric_cols = ["MonthlyOrders", "AOV", "InStoreRevenue", "UberEatsRevenue", "DoorDashRevenue", "SelfDeliveryRevenue"]
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
    print(f"   {col}: {outliers} outliers ({outliers/len(df)*100:.1f}%)")

# Drop helper columns
df.drop(columns=["ComputedTotal", "OrderDiff", "ShareSum"], inplace=True)

# ============================================================
# CHANNEL VOLUME AGGREGATION
# ============================================================
print("\n" + "=" * 80)
print("CHANNEL VOLUME AGGREGATION")
print("=" * 80)

# By Channel
channel_orders = {
    "In-Store": df["InStoreOrdersCount"].sum(),
    "Uber Eats": df["UberEatsOrdersCount"].sum(),
    "DoorDash": df["DoorDashOrdersCount"].sum(),
    "Self-Delivery": df["SelfDeliveryOrdersCount"].sum(),
}
total_orders = sum(channel_orders.values())
print("\n1. Total Orders by Channel:")
for ch, vol in channel_orders.items():
    print(f"   {ch}: {vol:,} ({vol/total_orders*100:.1f}%)")
print(f"   TOTAL: {total_orders:,}")

# By Subregion
print("\n2. Orders by Subregion:")
subregion_summary = df.groupby("Subregion").agg({
    "MonthlyOrders": "sum",
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
}).sort_values("MonthlyOrders", ascending=False)
print(subregion_summary.to_string())

# By Cuisine
print("\n3. Orders by Cuisine Type:")
cuisine_summary = df.groupby("CuisineType").agg({
    "MonthlyOrders": "sum",
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
}).sort_values("MonthlyOrders", ascending=False)
print(cuisine_summary.to_string())

# By Segment
print("\n4. Orders by Segment:")
segment_summary = df.groupby("Segment").agg({
    "MonthlyOrders": "sum",
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
}).sort_values("MonthlyOrders", ascending=False)
print(segment_summary.to_string())

# ============================================================
# CHANNEL MARKET SHARE ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("CHANNEL MARKET SHARE ANALYSIS")
print("=" * 80)

# Overall channel market share
print("\n1. Overall Channel Market Share (by orders):")
for ch, vol in channel_orders.items():
    print(f"   {ch}: {vol/total_orders*100:.2f}%")

# Overall channel market share by revenue
channel_rev = {
    "In-Store": df["InStoreRevenue"].sum(),
    "Uber Eats": df["UberEatsRevenue"].sum(),
    "DoorDash": df["DoorDashRevenue"].sum(),
    "Self-Delivery": df["SelfDeliveryRevenue"].sum(),
}
total_rev = sum(channel_rev.values())
print("\n2. Overall Channel Market Share (by revenue):")
for ch, rev in channel_rev.items():
    print(f"   {ch}: ${rev:,.2f} ({rev/total_rev*100:.2f}%)")

# Delivery vs In-Store dominance
delivery_orders = channel_orders["Uber Eats"] + channel_orders["DoorDash"] + channel_orders["Self-Delivery"]
print(f"\n3. In-Store vs Delivery:")
print(f"   In-Store: {channel_orders['In-Store']:,} ({channel_orders['In-Store']/total_orders*100:.1f}%)")
print(f"   Delivery (all channels): {delivery_orders:,} ({delivery_orders/total_orders*100:.1f}%)")

# Channel ranking
print("\n4. Channel Ranking by Order Contribution:")
sorted_channels = sorted(channel_orders.items(), key=lambda x: x[1], reverse=True)
for rank, (ch, vol) in enumerate(sorted_channels, 1):
    print(f"   #{rank}: {ch} - {vol:,} orders ({vol/total_orders*100:.1f}%)")

# ============================================================
# GEOGRAPHIC CHANNEL PREFERENCE ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("GEOGRAPHIC CHANNEL PREFERENCE ANALYSIS")
print("=" * 80)

geo_channel = df.groupby("Subregion").agg({
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
    "MonthlyOrders": "sum",
})

for sub in geo_channel.index:
    row = geo_channel.loc[sub]
    total = row["MonthlyOrders"]
    print(f"\n{sub}:")
    print(f"   In-Store:      {row['InStoreOrdersCount']:>7,} ({row['InStoreOrdersCount']/total*100:.1f}%)")
    print(f"   Uber Eats:     {row['UberEatsOrdersCount']:>7,} ({row['UberEatsOrdersCount']/total*100:.1f}%)")
    print(f"   DoorDash:      {row['DoorDashOrdersCount']:>7,} ({row['DoorDashOrdersCount']/total*100:.1f}%)")
    print(f"   Self-Delivery: {row['SelfDeliveryOrdersCount']:>7,} ({row['SelfDeliveryOrdersCount']/total*100:.1f}%)")

# Identify urban vs suburban
print("\nUrban vs Suburban Ordering Behavior:")
urban = geo_channel.loc["Central Auckland"]
suburban = geo_channel.drop("Central Auckland").sum()
urban_total = urban["MonthlyOrders"]
suburban_total = suburban["MonthlyOrders"]
print(f"   Central Auckland (Urban): In-Store {urban['InStoreOrdersCount']/urban_total*100:.1f}%, Delivery {(urban_total-urban['InStoreOrdersCount'])/urban_total*100:.1f}%")
print(f"   Rest of Auckland (Suburban): In-Store {suburban['InStoreOrdersCount']/suburban_total*100:.1f}%, Delivery {(suburban_total-suburban['InStoreOrdersCount'])/suburban_total*100:.1f}%")

# ============================================================
# CUISINE & SEGMENT CHANNEL PATTERNS
# ============================================================
print("\n" + "=" * 80)
print("CUISINE & SEGMENT CHANNEL PATTERNS")
print("=" * 80)

# Channel mix by cuisine
print("\n1. Channel Mix by Cuisine Type:")
cuisine_channel = df.groupby("CuisineType").agg({
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
    "MonthlyOrders": "sum",
})
cuisine_channel["InStorePct"] = (cuisine_channel["InStoreOrdersCount"] / cuisine_channel["MonthlyOrders"] * 100).round(1)
cuisine_channel["UEPct"] = (cuisine_channel["UberEatsOrdersCount"] / cuisine_channel["MonthlyOrders"] * 100).round(1)
cuisine_channel["DDPct"] = (cuisine_channel["DoorDashOrdersCount"] / cuisine_channel["MonthlyOrders"] * 100).round(1)
cuisine_channel["SDPct"] = (cuisine_channel["SelfDeliveryOrdersCount"] / cuisine_channel["MonthlyOrders"] * 100).round(1)
cuisine_channel["AggregatorPct"] = cuisine_channel["UEPct"] + cuisine_channel["DDPct"]
print(cuisine_channel[["InStorePct", "UEPct", "DDPct", "SDPct", "AggregatorPct"]].sort_values("AggregatorPct", ascending=False).to_string())

# Channel reliance by segment
print("\n2. Channel Reliance by Segment:")
segment_channel = df.groupby("Segment").agg({
    "InStoreOrdersCount": "sum",
    "UberEatsOrdersCount": "sum",
    "DoorDashOrdersCount": "sum",
    "SelfDeliveryOrdersCount": "sum",
    "MonthlyOrders": "sum",
})
segment_channel["InStorePct"] = (segment_channel["InStoreOrdersCount"] / segment_channel["MonthlyOrders"] * 100).round(1)
segment_channel["UEPct"] = (segment_channel["UberEatsOrdersCount"] / segment_channel["MonthlyOrders"] * 100).round(1)
segment_channel["DDPct"] = (segment_channel["DoorDashOrdersCount"] / segment_channel["MonthlyOrders"] * 100).round(1)
segment_channel["SDPct"] = (segment_channel["SelfDeliveryOrdersCount"] / segment_channel["MonthlyOrders"] * 100).round(1)
segment_channel["AggregatorPct"] = segment_channel["UEPct"] + segment_channel["DDPct"]
print(segment_channel[["InStorePct", "UEPct", "DDPct", "SDPct", "AggregatorPct"]].sort_values("AggregatorPct", ascending=False).to_string())

# Aggregator-heavy cuisine categories
print("\n3. Top Aggregator-Heavy Cuisines:")
top_agg = cuisine_channel.sort_values("AggregatorPct", ascending=False).head(5)
for cuisine in top_agg.index:
    pct = top_agg.loc[cuisine, "AggregatorPct"]
    print(f"   {cuisine}: {pct:.1f}% aggregator reliance")

# ============================================================
# CHANNEL DEPENDENCY RISK IDENTIFICATION
# ============================================================
print("\n" + "=" * 80)
print("CHANNEL DEPENDENCY RISK IDENTIFICATION")
print("=" * 80)

# Flag restaurants with 70% reliance on a single aggregator
df["MaxAggregatorShare"] = df[["UE_share", "DD_share"]].max(axis=1)
df["MaxChannelShare"] = df[["InStoreShare", "UE_share", "DD_share", "SD_share"]].max(axis=1)
df["AggregatorDependence"] = df["UE_share"] + df["DD_share"]

high_risk = df[df["MaxAggregatorShare"] >= 70]
moderate_risk = df[(df["MaxAggregatorShare"] >= 50) & (df["MaxAggregatorShare"] < 70)]
low_risk = df[df["MaxAggregatorShare"] < 50]

print(f"\n1. Aggregator Dependency Risk (70%+ on single aggregator):")
print(f"   High Risk (≥70%): {len(high_risk)} restaurants ({len(high_risk)/len(df)*100:.1f}%)")
print(f"   Moderate Risk (50-69%): {len(moderate_risk)} restaurants ({len(moderate_risk)/len(df)*100:.1f}%)")
print(f"   Low Risk (<50%): {len(low_risk)} restaurants ({len(low_risk)/len(df)*100:.1f}%)")

# Balanced vs high-risk profiles (Shannon Entropy)
def calc_diversification_score(row):
    shares = [row["InStoreShare"]/100, row["UE_share"]/100, row["DD_share"]/100, row["SD_share"]/100]
    entropy = 0
    for s in shares:
        if s > 0:
            entropy -= s * np.log2(s)
    # Normalize by max entropy (log2(4) = 2)
    return entropy / 2

df["ChannelDiversificationScore"] = df.apply(calc_diversification_score, axis=1)

print(f"\n2. Channel Diversification Score (0=concentrated, 1=balanced):")
print(f"   Mean: {df['ChannelDiversificationScore'].mean():.3f}")
print(f"   Median: {df['ChannelDiversificationScore'].median():.3f}")
print(f"   Std Dev: {df['ChannelDiversificationScore'].std():.3f}")

# Diversification categories
df["DiversificationCategory"] = pd.cut(df["ChannelDiversificationScore"],
    bins=[0, 0.5, 0.75, 1.0],
    labels=["Highly Concentrated", "Moderately Diversified", "Well Diversified"])
print(f"\n3. Diversification Distribution:")
print(f"   {df['DiversificationCategory'].value_counts().to_string()}")

# Top 5 most concentrated restaurants
print(f"\n4. Top 5 Most Channel-Concentrated Restaurants:")
most_conc = df.nsmallest(5, "ChannelDiversificationScore")[["RestaurantName", "CuisineType", "Subregion", "MaxChannelShare", "ChannelDiversificationScore"]]
print(most_conc.to_string(index=False))

# Top 5 most diversified restaurants
print(f"\n5. Top 5 Most Diversified Restaurants:")
most_div = df.nlargest(5, "ChannelDiversificationScore")[["RestaurantName", "CuisineType", "Subregion", "MaxChannelShare", "ChannelDiversificationScore"]]
print(most_div.to_string(index=False))

# ============================================================
# KPI CALCULATIONS
# ============================================================
print("\n" + "=" * 80)
print("KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 80)

print("\n1. Channel Order Share (%):")
for ch, vol in channel_orders.items():
    print(f"   {ch}: {vol/total_orders*100:.1f}%")

print(f"\n2. Aggregator Dependence Index (avg):")
print(f"   Mean: {df['AggregatorDependence'].mean():.1f}%")
print(f"   By Subregion: {df.groupby('Subregion')['AggregatorDependence'].mean().round(1).to_dict()}")

print(f"\n3. In-Store Reliance Ratio (avg):")
print(f"   Mean: {df['InStoreShare'].mean():.1f}%")
print(f"   By Segment: {df.groupby('Segment')['InStoreShare'].mean().round(1).to_dict()}")

print(f"\n4. Channel Diversification Score (avg):")
print(f"   Mean: {df['ChannelDiversificationScore'].mean():.3f}")
print(f"   By Cuisine: {df.groupby('CuisineType')['ChannelDiversificationScore'].mean().round(3).to_dict()}")

print(f"\n5. Subregion Channel Dominance:")
for sub in df["Subregion"].unique():
    sub_df = df[df["Subregion"] == sub]
    channels = {"In-Store": sub_df["InStoreShare"].mean(), "Uber Eats": sub_df["UE_share"].mean(),
                "DoorDash": sub_df["DD_share"].mean(), "Self-Delivery": sub_df["SD_share"].mean()}
    dominant = max(channels, key=channels.get)
    print(f"   {sub}: Dominant channel = {dominant} ({channels[dominant]:.1f}%)")

# ============================================================
# PROFITABILITY ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("PROFITABILITY ANALYSIS BY CHANNEL")
print("=" * 80)

channel_profits = {
    "In-Store": df["InStoreNetProfit"].sum(),
    "Uber Eats": df["UberEatsNetProfit"].sum(),
    "DoorDash": df["DoorDashNetProfit"].sum(),
    "Self-Delivery": df["SelfDeliveryNetProfit"].sum(),
}
total_profit = sum(channel_profits.values())

print("\n1. Net Profit by Channel:")
for ch, profit in channel_profits.items():
    print(f"   {ch}: ${profit:,.2f} ({profit/total_profit*100:.1f}% of total)")

print("\n2. Net Profit Margin by Channel:")
for ch, profit_col in [("In-Store", "InStoreNetProfit"), ("Uber Eats", "UberEatsNetProfit"),
                        ("DoorDash", "DoorDashNetProfit"), ("Self-Delivery", "SelfDeliveryNetProfit")]:
    rev_col = {"In-Store": "InStoreRevenue", "Uber Eats": "UberEatsRevenue",
               "DoorDash": "DoorDashRevenue", "Self-Delivery": "SelfDeliveryRevenue"}[ch]
    margin = df[profit_col].sum() / df[rev_col].sum() * 100
    print(f"   {ch}: {margin:.1f}%")

# ============================================================
# GENERATE CHARTS
# ============================================================
print("\n" + "=" * 80)
print("GENERATING CHARTS")
print("=" * 80)

# Chart 1: Overall Channel Market Share (Orders)
fig, ax = plt.subplots(figsize=(10, 6))
channels = list(channel_orders.keys())
volumes = list(channel_orders.values())
colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']
bars = ax.bar(channels, volumes, color=colors, edgecolor='white', linewidth=1.5)
for bar, vol in zip(bars, volumes):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 500,
            f'{vol:,}\n({vol/total_orders*100:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Overall Channel Market Share by Orders', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Total Orders', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
plt.savefig('charts/01_channel_market_share_orders.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 2: Channel Market Share (Revenue)
fig, ax = plt.subplots(figsize=(10, 6))
rev_values = list(channel_rev.values())
bars = ax.bar(channels, rev_values, color=colors, edgecolor='white', linewidth=1.5)
for bar, rev in zip(bars, rev_values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2000,
            f'${rev:,.0f}\n({rev/total_rev*100:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_title('Overall Channel Market Share by Revenue', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Revenue ($)', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('charts/02_channel_market_share_revenue.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 3: Subregion Channel Distribution (Stacked Bar)
fig, ax = plt.subplots(figsize=(12, 7))
sub_ch = df.groupby("Subregion")[["InStoreOrdersCount", "UberEatsOrdersCount", "DoorDashOrdersCount", "SelfDeliveryOrdersCount"]].sum()
sub_ch_pct = sub_ch.div(sub_ch.sum(axis=1), axis=0) * 100
sub_ch_pct = sub_ch_pct.reindex(["North Shore", "West Auckland", "Central Auckland", "South Auckland", "East Auckland"])
sub_ch_pct.columns = ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]
sub_ch_pct.plot(kind='bar', stacked=True, ax=ax, color=colors, edgecolor='white', linewidth=0.5)
ax.set_title('Channel Distribution by Subregion', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Share of Orders (%)', fontsize=12)
ax.set_xlabel('Subregion', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
ax.legend(title='Channel', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig('charts/03_subregion_channel_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 4: Cuisine Channel Distribution (Heatmap)
fig, ax = plt.subplots(figsize=(12, 8))
cuisine_ch = df.groupby("CuisineType")[["InStoreShare", "UE_share", "DD_share", "SD_share"]].mean()
cuisine_ch.columns = ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]
sns.heatmap(cuisine_ch, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, linewidths=0.5,
            cbar_kws={'label': 'Average Share (%)'})
ax.set_title('Average Channel Share by Cuisine Type', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Cuisine Type', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
plt.tight_layout()
plt.savefig('charts/04_cuisine_channel_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 5: Segment Channel Distribution
fig, ax = plt.subplots(figsize=(12, 7))
seg_ch = df.groupby("Segment")[["InStoreShare", "UE_share", "DD_share", "SD_share"]].mean()
seg_ch.columns = ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]
seg_ch = seg_ch.sort_values("In-Store", ascending=True)
seg_ch.plot(kind='barh', stacked=True, ax=ax, color=colors, edgecolor='white', linewidth=0.5)
ax.set_title('Channel Mix by Restaurant Segment', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Share (%)', fontsize=12)
ax.set_ylabel('Segment', fontsize=12)
ax.legend(title='Channel', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig('charts/05_segment_channel_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 6: Dependency Risk Distribution
fig, ax = plt.subplots(figsize=(10, 6))
risk_colors = {'High Risk (≥70%)': '#E91E63', 'Moderate Risk (50-69%)': '#FF9800', 'Low Risk (<50%)': '#4CAF50'}
risk_counts = {
    'High Risk (≥70%)': len(high_risk),
    'Moderate Risk (50-69%)': len(moderate_risk),
    'Low Risk (<50%)': len(low_risk),
}
bars = ax.barh(list(risk_counts.keys()), list(risk_counts.values()), 
               color=list(risk_colors.values()), edgecolor='white', linewidth=1.5)
for bar, count in zip(bars, risk_counts.values()):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2.,
            f'{count} ({count/len(df)*100:.1f}%)', ha='left', va='center', fontweight='bold', fontsize=12)
ax.set_title('Aggregator Dependency Risk Distribution', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Restaurants', fontsize=12)
plt.tight_layout()
plt.savefig('charts/06_dependency_risk_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 7: Net Profit by Channel
fig, ax = plt.subplots(figsize=(10, 6))
profit_colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']
profits = list(channel_profits.values())
bars = ax.bar(channels, profits, color=profit_colors, edgecolor='white', linewidth=1.5)
for bar, profit in zip(bars, profits):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1000,
            f'${profit:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Net Profit by Channel', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Net Profit ($)', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('charts/07_net_profit_by_channel.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 8: Channel Diversification Score Distribution
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["ChannelDiversificationScore"], bins=30, color='#673AB7', edgecolor='white', alpha=0.8)
ax.axvline(df["ChannelDiversificationScore"].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["ChannelDiversificationScore"].mean():.3f}')
ax.axvline(df["ChannelDiversificationScore"].median(), color='blue', linestyle='--', linewidth=2, label=f'Median: {df["ChannelDiversificationScore"].median():.3f}')
ax.set_title('Channel Diversification Score Distribution', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Diversification Score (0=Concentrated, 1=Balanced)', fontsize=12)
ax.set_ylabel('Number of Restaurants', fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/08_diversification_score_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 9: Subregion Heatmap (Orders by Channel)
fig, ax = plt.subplots(figsize=(12, 6))
sub_ch_abs = df.groupby("Subregion")[["InStoreOrdersCount", "UberEatsOrdersCount", "DoorDashOrdersCount", "SelfDeliveryOrdersCount"]].sum()
sub_ch_abs.columns = ["In-Store", "Uber Eats", "DoorDash", "Self-Delivery"]
sub_ch_abs = sub_ch_abs.reindex(["North Shore", "West Auckland", "Central Auckland", "South Auckland", "East Auckland"])
sns.heatmap(sub_ch_abs, annot=True, fmt=',', cmap='Blues', ax=ax, linewidths=0.5,
            cbar_kws={'label': 'Order Volume'})
ax.set_title('Order Volume by Subregion and Channel', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Subregion', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
plt.tight_layout()
plt.savefig('charts/09_subregion_volume_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 10: Aggregator Dependence by Cuisine
fig, ax = plt.subplots(figsize=(12, 7))
cuisine_agg = df.groupby("CuisineType")["AggregatorDependence"].mean().sort_values(ascending=True)
bars = ax.barh(cuisine_agg.index, cuisine_agg.values, color='#FF5722', edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, cuisine_agg.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2.,
            f'{val:.1f}%', ha='left', va='center', fontweight='bold', fontsize=11)
ax.axvline(x=70, color='red', linestyle='--', linewidth=2, alpha=0.7, label='High Risk Threshold (70%)')
ax.set_title('Average Aggregator Dependence by Cuisine Type', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Aggregator Dependence (%)', fontsize=12)
ax.set_ylabel('Cuisine Type', fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/10_cuisine_aggregator_dependence.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 11: Net Profit Margin by Channel
fig, ax = plt.subplots(figsize=(10, 6))
margins = {}
for ch, rev_col, profit_col in [("In-Store", "InStoreRevenue", "InStoreNetProfit"),
                                   ("Uber Eats", "UberEatsRevenue", "UberEatsNetProfit"),
                                   ("DoorDash", "DoorDashRevenue", "DoorDashNetProfit"),
                                   ("Self-Delivery", "SelfDeliveryRevenue", "SelfDeliveryNetProfit")]:
    margins[ch] = df[profit_col].sum() / df[rev_col].sum() * 100
bars = ax.bar(margins.keys(), margins.values(), color=profit_colors, edgecolor='white', linewidth=1.5)
for bar, margin in zip(bars, margins.values()):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
            f'{margin:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Net Profit Margin by Channel', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Net Profit Margin (%)', fontsize=12)
ax.set_xlabel('Order Channel', fontsize=12)
plt.tight_layout()
plt.savefig('charts/11_profit_margin_by_channel.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 12: Scatter - AOV vs Diversification Score
fig, ax = plt.subplots(figsize=(10, 7))
for seg in df["Segment"].unique():
    seg_df = df[df["Segment"] == seg]
    ax.scatter(seg_df["AOV"], seg_df["ChannelDiversificationScore"], label=seg, alpha=0.6, s=50)
ax.set_title('AOV vs Channel Diversification Score', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Order Value ($)', fontsize=12)
ax.set_ylabel('Channel Diversification Score', fontsize=12)
ax.legend(title='Segment', fontsize=10)
plt.tight_layout()
plt.savefig('charts/12_aov_vs_diversification.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nAll 12 charts saved to charts/ directory.")
print("Analysis complete!")

# Save key metrics to JSON for dashboard
metrics = {
    "total_restaurants": len(df),
    "total_orders": int(total_orders),
    "total_revenue": round(total_rev, 2),
    "total_profit": round(total_profit, 2),
    "channel_orders": {k: int(v) for k, v in channel_orders.items()},
    "channel_revenue": {k: round(v, 2) for k, v in channel_rev.items()},
    "channel_profit": {k: round(v, 2) for k, v in channel_profits.items()},
    "avg_diversification_score": round(df["ChannelDiversificationScore"].mean(), 3),
    "avg_aggregator_dependence": round(df["AggregatorDependence"].mean(), 1),
    "avg_instore_reliance": round(df["InStoreShare"].mean(), 1),
    "high_risk_count": len(high_risk),
    "moderate_risk_count": len(moderate_risk),
    "low_risk_count": len(low_risk),
}
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
print("Key metrics saved to metrics.json")
