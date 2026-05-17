# Order Channel Performance and Market Share Analytics for SkyCity Auckland Restaurants & Bars

## A Comprehensive Research Report on Multi-Channel Ordering Dynamics in Auckland's Hospitality Ecosystem

---

## Abstract

This research paper presents a detailed analysis of order channel performance and market share across SkyCity Auckland's restaurant and bar ecosystem. Drawing on a dataset of 150 restaurants spanning five Auckland subregions, ten cuisine types, and five business segments, we examine how ordering behaviour varies across four parallel channels: In-Store, Uber Eats, DoorDash, and Self-Delivery. Our findings reveal that delivery channels collectively account for 68.6% of total order volume, with In-Store dining retaining only 31.4% of orders despite generating 49.6% of total net profit. We identify significant geographic variation in channel preferences, with Central Auckland exhibiting the highest delivery dependence at 72.0%, and cuisine-specific aggregator reliance patterns that expose Pizza (55.2%) and Indian (52.6%) restaurants to elevated platform dependency risk. The Channel Diversification Score, based on Shannon entropy, demonstrates that most Auckland restaurants maintain relatively well-balanced channel portfolios (mean score: 0.980), though profitability varies dramatically across channels — In-Store operations deliver a 31.1% net profit margin compared to just 9.1% for Uber Eats and 8.8% for DoorDash. These findings carry significant implications for channel strategy, risk mitigation, and sustainable growth in an increasingly delivery-driven market.

---

## 1. Introduction

### 1.1 Background and Context

The Auckland hospitality market has undergone a fundamental transformation over the past decade, driven by the rapid expansion of food delivery aggregators such as Uber Eats and DoorDash, evolving consumer preferences for convenience and contactless ordering, and urban density differences across Auckland's diverse subregions. Restaurants now operate across four parallel order channels — In-Store dining, Uber Eats, DoorDash, and Self-Delivery — each playing a distinctly different strategic role in customer reach, brand visibility, and volume generation.

The emergence of multi-channel ordering has created both opportunities and challenges for restaurant operators. While delivery platforms expand market reach beyond physical restaurant boundaries, they simultaneously introduce commission structures that can erode profitability by 15–30% per order. Self-delivery offers an alternative path, but requires significant operational investment in logistics infrastructure. In-Store dining, while representing the most profitable channel per transaction, faces declining share as consumer behaviour shifts toward convenience-oriented ordering.

### 1.2 Problem Statement

Despite having detailed channel-level data, restaurant operators and analysts in the Auckland market lack clear visibility into channel dependence, understanding of which channels dominate in which subregions, and insight into how cuisine type and restaurant segment influence channel mix. Without this knowledge, restaurants become over-dependent on aggregators, channel strategy decisions remain intuition-based, and market risks remain hidden until they materialise as sudden commission increases, platform policy changes, or demand shifts.

### 1.3 Research Objectives

The primary objectives of this study are to quantify total order volume by channel, measure channel share distribution across restaurants, and identify dominant ordering channels by geography. Secondary objectives include comparing channel mix across cuisine types, assessing channel diversity versus dependency, and supporting strategic channel planning through data-driven recommendations.

### 1.4 Scope and Significance

This study encompasses 150 restaurant establishments across five Auckland subregions (North Shore, West Auckland, Central Auckland, South Auckland, and East Auckland), covering ten cuisine categories and five business segments. The analysis provides actionable insights for restaurant operators, platform strategists, and hospitality industry policymakers seeking to understand the evolving multi-channel landscape.

---

## 2. Literature Review

### 2.1 Multi-Channel Restaurant Operations

The concept of omni-channel retail has been extensively studied in the general retail literature, but its application to the restaurant industry remains relatively nascent. Research by Bimpikis et al. (2019) demonstrated that multi-platform restaurant operations create complex demand interdependencies, where price changes on one channel can cannibalise or complement demand on others. The restaurant-specific context introduces unique challenges including perishable inventory, capacity constraints on kitchen throughput, and the physical separation between food preparation and consumption locations.

### 2.2 Food Delivery Platform Economics

The economics of food delivery platforms have been examined through multiple lenses. Cummings and Doherty (2021) highlighted the "platform dependency trap" where restaurants initially benefit from aggregator-generated demand but subsequently face margin erosion as commission rates increase. The typical commission structure ranges from 15–30% of order value, which, when combined with cost of goods sold (COGS) of 20–40% and operating expenses (OPEX) of 20–55%, leaves minimal room for profit on aggregator-generated orders.

### 2.3 Geographic Influences on Ordering Behaviour

Urban density and demographic composition significantly influence channel preference patterns. Research in the Australian and New Zealand markets has shown that inner-city areas with higher population density and younger demographics exhibit stronger delivery adoption, while suburban and peri-urban areas retain higher in-store dining shares. Auckland's geographic diversity — from the dense Central Business District to the sprawling suburban landscapes of West and South Auckland — provides a natural laboratory for studying these geographic effects.

### 2.4 Channel Diversification and Risk Management

Portfolio theory, originally developed for financial markets, has been adapted to channel diversification analysis. The Shannon entropy measure provides a principled approach to quantifying how evenly distributed a restaurant's orders are across channels. A perfectly balanced four-channel portfolio yields a normalised entropy score of 1.0, while complete concentration on a single channel yields 0.0. Restaurants with low diversification scores face heightened vulnerability to channel-specific disruptions.

---

## 3. Methodology

### 3.1 Data Collection and Description

The dataset comprises 150 restaurant records from the SkyCity Auckland Restaurants & Bars network, with 30 variables capturing restaurant characteristics, order volumes, revenue, costs, profits, and channel shares. Each restaurant is characterised by a unique identifier, name, cuisine type, business segment, and subregion location. The four order channels — In-Store, Uber Eats, DoorDash, and Self-Delivery — are tracked for both order counts and revenue generation.

### 3.2 Data Validation

Rigorous validation procedures were applied to ensure data integrity. First, channel order counts (InStoreOrdersCount + UberEatsOrdersCount + DoorDashOrdersCount + SelfDeliveryOrdersCount) were verified to sum exactly to MonthlyOrders for all 150 records. Second, channel share percentages (InStoreShare + UE_share + DD_share + SD_share) were confirmed to sum within the range 99.99%–100.01%, with minor rounding-induced variance. Third, outlier detection using the Interquartile Range (IQR) method identified 22 records with anomalous Average Order Values (14.7% of the dataset), which is consistent with the natural variance expected across different restaurant segments (from QSR to Fine Dining).

### 3.3 Analytical Framework

The analysis follows a structured five-step methodology:

**Step 1: Data Validation and Consistency Checks** — Verification of data integrity and identification of anomalies.

**Step 2: Channel Volume Aggregation** — Aggregation of total orders by channel, subregion, cuisine type, and restaurant segment.

**Step 3: Channel Market Share Analysis** — Computation of overall channel market share by both order volume and revenue, comparison of delivery versus in-store dominance, and channel ranking by order contribution.

**Step 4: Geographic Channel Preference Analysis** — Comparison of channel share distributions across the five Auckland subregions, with specific attention to urban (Central Auckland) versus suburban ordering behaviour differences.

**Step 5: Cuisine and Segment Channel Patterns** — Analysis of channel mix variation by cuisine type and business segment, identification of aggregator-heavy categories, and computation of dependency risk metrics.

### 3.4 Key Performance Indicators

Five core KPIs were defined to capture the essential dynamics of channel performance:

- **Channel Order Share (%)**: Volume contribution by each channel, measuring reach and customer engagement.
- **Aggregator Dependence Index**: Combined Uber Eats and DoorDash share, measuring platform reliance.
- **In-Store Reliance Ratio**: Walk-in order strength, indicating traditional dining resilience.
- **Channel Diversification Score**: Normalised Shannon entropy (0–1 scale), measuring operational resilience through channel balance.
- **Subregion Channel Dominance**: Geographic ordering behaviour patterns, identifying spatial variation.

### 3.5 Channel Diversification Score Computation

The Channel Diversification Score is computed using Shannon entropy, normalised by the maximum possible entropy for a four-channel system:

$$D_i = -\frac{1}{\log_2(4)} \sum_{c=1}^{4} p_{ic} \log_2(p_{ic})$$

where $p_{ic}$ is the share of restaurant $i$'s orders through channel $c$. A score of 1.0 indicates perfectly equal distribution across all four channels (25% each), while a score approaching 0.0 indicates near-total concentration on a single channel.

---

## 4. Results and Analysis

### 4.1 Channel Volume Aggregation

The 150 restaurants in the dataset generate a combined 180,702 monthly orders across all channels. The distribution of these orders across the four channels reveals a clear hierarchy:

**Table 1: Total Orders by Channel**

| Channel | Orders | Share (%) |
|---------|--------|-----------|
| In-Store | 56,662 | 31.4% |
| Uber Eats | 45,211 | 25.0% |
| DoorDash | 40,533 | 22.4% |
| Self-Delivery | 38,296 | 21.2% |
| **Total** | **180,702** | **100.0%** |

In-Store dining remains the single largest channel by order volume, commanding 31.4% of all transactions. However, the aggregate delivery channels (Uber Eats + DoorDash + Self-Delivery) account for 68.6% of total orders, underscoring the dominance of delivery-oriented ordering in the current market. Among delivery channels, Uber Eats leads with 25.0%, followed by DoorDash at 22.4%, and Self-Delivery at 21.2%.

Revenue distribution follows a similar pattern but with a notable emphasis on In-Store's revenue contribution:

**Table 2: Total Revenue by Channel**

| Channel | Revenue ($) | Share (%) |
|---------|------------|-----------|
| In-Store | 1,869,967.98 | 29.2% |
| Uber Eats | 1,697,357.44 | 26.5% |
| DoorDash | 1,487,054.23 | 23.2% |
| Self-Delivery | 1,343,979.76 | 21.0% |
| **Total** | **6,398,359.41** | **100.0%** |

The higher revenue share of In-Store relative to its order share reflects the higher average order values associated with dine-in experiences, where customers tend to order additional items, beverages, and desserts that are less common in delivery orders.

### 4.2 Channel Market Share Analysis

The overall channel market share analysis reveals that In-Store dining, while leading in both orders (31.4%) and revenue (29.2%), is increasingly marginalised by the collective weight of delivery channels. The In-Store versus Delivery split stands at 31.4% to 68.6% by orders, a striking indicator of the delivery-first shift in consumer behaviour.

When examining revenue, the gap narrows slightly — In-Store accounts for 29.2% of revenue versus 70.8% for delivery — suggesting that delivery orders generate proportionally less revenue per transaction than their order share would indicate. This is partially attributable to commission structures on aggregator platforms and the higher average order values in dine-in settings.

Among the three delivery channels, Uber Eats holds the dominant position with 25.0% order share and 26.5% revenue share, making it the leading delivery aggregator in the Auckland market. DoorDash follows with 22.4% of orders and 23.2% of revenue. Self-Delivery, while having the lowest order share (21.2%), offers restaurants the advantage of direct customer relationships and absence of third-party commission fees.

### 4.3 Geographic Channel Preference Analysis

Channel preferences vary significantly across Auckland's five subregions, reflecting differences in urban density, demographic composition, and delivery infrastructure maturity.

**Table 3: Channel Share by Subregion**

| Subregion | In-Store | Uber Eats | DoorDash | Self-Delivery |
|-----------|----------|-----------|----------|---------------|
| Central Auckland | 28.0% | 26.7% | 25.3% | 20.0% |
| East Auckland | 32.3% | 25.5% | 22.2% | 20.0% |
| North Shore | 30.8% | 25.7% | 22.1% | 21.4% |
| South Auckland | 32.0% | 23.6% | 19.3% | 25.1% |
| West Auckland | 33.2% | 23.8% | 23.0% | 20.0% |

Central Auckland exhibits the lowest In-Store share (28.0%) and the highest aggregator reliance, with Uber Eats (26.7%) and DoorDash (25.3%) together accounting for 52.0% of all orders. This reflects the urban density effect, where proximity to a large number of restaurants and the convenience culture of the central business district drive strong delivery adoption. The delivery-to-in-store ratio in Central Auckland is 72.0% to 28.0%, the most delivery-skewed of any subregion.

In contrast, West Auckland shows the highest In-Store share at 33.2%, suggesting a more traditional dining culture or lower delivery infrastructure penetration. South Auckland presents an interesting pattern with the highest Self-Delivery share (25.1%), potentially reflecting lower aggregator coverage in some areas and a stronger tradition of restaurant-managed delivery.

The urban-suburban divide is starkly illustrated by comparing Central Auckland (72.0% delivery) with the rest of Auckland (67.8% delivery). While the difference of 4.2 percentage points may seem modest, it represents approximately 1,500 additional delivery orders per month in Central Auckland that would be In-Store orders in suburban locations, all else being equal.

**Table 4: Urban vs Suburban Ordering Behaviour**

| Metric | Central Auckland (Urban) | Rest of Auckland (Suburban) |
|--------|--------------------------|------------------------------|
| In-Store Share | 28.0% | 32.2% |
| Delivery Share | 72.0% | 67.8% |
| Uber Eats Share | 26.7% | 24.8% |
| DoorDash Share | 25.3% | 21.8% |
| Self-Delivery Share | 20.0% | 21.2% |

The key urban-suburban differentiator is aggregator usage: Central Auckland restaurants see 52.0% of orders through Uber Eats and DoorDash combined, compared to 46.6% in suburban areas. Self-Delivery share is marginally higher in suburban areas (21.2% vs 20.0%), suggesting that restaurants outside the urban core may be more motivated to build their own delivery capabilities.

### 4.4 Cuisine and Segment Channel Patterns

#### 4.4.1 Channel Mix by Cuisine Type

Cuisine type is a powerful predictor of channel mix, reflecting both the inherent delivery-friendliness of different food categories and the strategic choices made by operators within each cuisine segment.

**Table 5: Channel Mix by Cuisine Type**

| Cuisine | In-Store | Uber Eats | DoorDash | Self-Delivery | Aggregator % |
|---------|----------|-----------|----------|---------------|-------------|
| Pizza | 25.0% | 27.4% | 27.8% | 19.8% | 55.2% |
| Indian | 28.5% | 27.9% | 24.7% | 18.9% | 52.6% |
| Sushi & Japanese | 29.5% | 27.0% | 22.2% | 21.3% | 49.2% |
| Burgers | 28.2% | 24.6% | 23.4% | 23.8% | 48.0% |
| Mexican | 29.9% | 25.6% | 22.1% | 22.4% | 47.7% |
| Mediterranean | 32.1% | 25.9% | 20.6% | 21.4% | 46.5% |
| Asian Fusion | 32.2% | 23.9% | 21.5% | 22.4% | 45.4% |
| Steak & Grill | 35.2% | 23.1% | 21.1% | 20.6% | 44.2% |
| Cafe & Brunch | 38.9% | 21.7% | 19.7% | 19.8% | 41.4% |
| Seafood | 36.5% | 20.9% | 18.2% | 24.4% | 39.1% |

Pizza restaurants exhibit the highest aggregator dependence at 55.2%, with more than half of all orders flowing through Uber Eats or DoorDash. This is consistent with the historical dominance of pizza delivery and the natural fit between pizza's delivery-friendly characteristics (hot-holding capability, uniform preparation, broad appeal) and aggregator platforms. Indian cuisine follows closely at 52.6%, reflecting the strong delivery demand for Indian food and the relatively limited dine-in infrastructure of many Indian restaurants in Auckland.

At the other end of the spectrum, Seafood restaurants show the lowest aggregator reliance (39.1%), paired with the highest Self-Delivery share (24.4%). This pattern likely reflects the premium nature of seafood dining, concerns about quality degradation during third-party delivery, and the investment many seafood restaurants have made in their own temperature-controlled delivery systems. Cafe & Brunch establishments also show relatively low aggregator reliance (41.4%), driven by the inherently in-person nature of the cafe experience and the lower delivery demand for breakfast and brunch items.

The In-Store share ranges from a low of 25.0% (Pizza) to a high of 38.9% (Cafe & Brunch), representing a 13.9 percentage point spread that underscores the significant influence of cuisine type on channel strategy.

#### 4.4.2 Channel Reliance by Business Segment

Business segment analysis reveals more nuanced patterns, with less dramatic variation across segments than across cuisine types.

**Table 6: Channel Reliance by Segment**

| Segment | In-Store | Uber Eats | DoorDash | Self-Delivery | Aggregator % |
|---------|----------|-----------|----------|---------------|-------------|
| Casual Dining | 29.7% | 25.7% | 23.7% | 20.9% | 49.4% |
| QSR | 31.5% | 25.0% | 22.4% | 21.1% | 47.4% |
| Fast Casual | 31.6% | 25.2% | 22.1% | 21.1% | 47.3% |
| Cafe | 31.2% | 24.6% | 22.5% | 21.7% | 47.1% |
| Fine Dining | 33.0% | 24.3% | 21.1% | 21.5% | 45.4% |

Casual Dining shows the highest aggregator dependence (49.4%), reflecting the competitive pressure on mid-market restaurants to maintain visibility on delivery platforms. Fine Dining, conversely, retains the highest In-Store share (33.0%) and the lowest aggregator reliance (45.4%), consistent with the premium dine-in experience that defines this segment and the logistical challenges of delivering high-end cuisine.

The relatively narrow range of aggregator dependence across segments (45.4% to 49.4%, a spread of just 4.0 percentage points) suggests that business segment is a less powerful predictor of channel mix than cuisine type. This finding implies that the nature of the food itself, rather than the operational model, is the primary driver of channel preference.

### 4.5 Channel Dependency Risk Identification

#### 4.5.1 Aggregator Dependency Assessment

The Aggregator Dependence Index, calculated as the combined Uber Eats and DoorDash share, reveals the average restaurant channels 47.0% of orders through third-party aggregators. At the subregion level, Central Auckland restaurants face the highest aggregator dependence (51.9%), while South Auckland restaurants have the lowest (42.6%).

Under the risk classification framework where restaurants with 70% or more reliance on a single aggregator are classified as "High Risk," the current dataset reveals that no restaurants meet this threshold. However, 0 restaurants fall in the "Moderate Risk" category (50–69% reliance on a single aggregator), and all 150 restaurants are classified as "Low Risk" (less than 50% reliance on any single aggregator). This broadly healthy distribution should not breed complacency — the average aggregator dependence of 47.0% means restaurants are operating close to the moderate risk threshold, and shifts in platform dynamics could quickly push many into riskier territory.

#### 4.5.2 Channel Diversification Score Analysis

The Channel Diversification Score, based on normalised Shannon entropy, provides a comprehensive measure of how balanced a restaurant's channel portfolio is. The distribution across all 150 restaurants shows:

- **Mean Diversification Score**: 0.980
- **Median Diversification Score**: 0.985
- **Standard Deviation**: 0.016
- **Range**: 0.929 to 0.999

The high mean and median scores indicate that most Auckland restaurants maintain relatively well-balanced channel portfolios. The narrow standard deviation (0.016) suggests limited variation in diversification quality across the market.

**Table 7: Diversification Category Distribution**

| Category | Score Range | Count | Percentage |
|----------|------------|-------|------------|
| Well Diversified | 0.75–1.00 | 150 | 100.0% |
| Moderately Diversified | 0.50–0.75 | 0 | 0.0% |
| Highly Concentrated | 0.00–0.50 | 0 | 0.0% |

While the universal "Well Diversified" classification is encouraging, the most concentrated restaurants in the dataset — Britomart Bar & Dine (0.929) and Mt Eden Munch (0.930) — still exhibit relatively high entropy scores, reflecting the fundamental structure of the Auckland market where no single channel dominates overwhelmingly.

At the cuisine level, Cafe & Brunch restaurants show the lowest average diversification score (0.957), reflecting their heavier tilt toward In-Store dining. Mexican restaurants achieve the highest average diversification (0.991), indicating the most balanced channel distribution of any cuisine type.

### 4.6 Profitability Analysis

The profitability analysis reveals dramatic differences across channels, with significant implications for strategic channel management.

**Table 8: Net Profit by Channel**

| Channel | Net Profit ($) | Share (%) | Profit Margin (%) |
|---------|---------------|-----------|-------------------|
| In-Store | 582,113.76 | 49.6% | 31.1% |
| Uber Eats | 154,228.98 | 13.1% | 9.1% |
| DoorDash | 130,383.60 | 11.1% | 8.8% |
| Self-Delivery | 307,472.47 | 26.2% | 22.9% |
| **Total** | **1,174,198.81** | **100.0%** | — |

The profitability disparity is striking. In-Store operations, despite representing only 31.4% of order volume, generate 49.6% of total net profit with a margin of 31.1%. This profitability advantage stems from the absence of commission fees and the higher average order values associated with dine-in experiences. Self-Delivery emerges as the second most profitable channel, generating 26.2% of total net profit with a 22.9% margin — a meaningful premium over aggregator channels despite the delivery cost per order ($0.89–$5.31).

The aggregator channels paint a sobering picture. Uber Eats, despite being the largest delivery channel by volume, delivers only a 9.1% net profit margin — roughly one-third of the In-Store margin. DoorDash is marginally worse at 8.8%. These low margins reflect the combined impact of commission rates (15–30%), COGS, and OPEX on what are already lower-value transactions relative to dine-in orders.

The profit-per-order differential is even more revealing. In-Store generates approximately $10.28 net profit per order, Self-Delivery yields approximately $8.03 per order, while Uber Eats and DoorDash deliver only $3.41 and $3.21 per order respectively. This 3:1 profit ratio between In-Store and aggregator channels represents a critical strategic consideration for restaurants seeking to optimise their channel mix.

---

## 5. Key Findings and Discussion

### 5.1 Delivery Dominance with Profitability Trade-offs

The most significant finding is the substantial gap between delivery's share of orders (68.6%) and its share of profits (50.4%). While delivery channels are essential for market reach and customer acquisition, they are significantly less profitable than In-Store dining. This creates a fundamental tension: restaurants need delivery to remain competitive and visible, but over-reliance on delivery channels erodes overall profitability.

### 5.2 Geographic Channel Polarisation

Central Auckland's 72.0% delivery share represents a qualitatively different operating environment from suburban areas. Restaurants in Central Auckland are operating in a delivery-first market, where aggregator relationships are not optional but existential. This has implications for lease negotiations, kitchen design, staffing models, and brand strategy. Suburban restaurants, while still delivery-heavy, have more flexibility to emphasise In-Store experiences.

### 5.3 Cuisine-Specific Aggregator Vulnerability

Pizza (55.2%) and Indian (52.6%) restaurants face meaningfully higher aggregator dependence than the market average (47.0%). For these cuisines, aggregator platforms are not merely a channel but a critical customer acquisition vehicle. Any disruption to aggregator relationships — through commission increases, algorithmic visibility changes, or competitive dynamics — would disproportionately impact these categories.

### 5.4 Self-Delivery as a Strategic Hedge

Self-Delivery, while the smallest channel by volume (21.2%), delivers the second-highest profit margin (22.9%) and provides a crucial hedge against aggregator dependency. Restaurants that have invested in self-delivery infrastructure enjoy both better per-order economics and greater strategic flexibility in negotiating with aggregators.

### 5.5 Diversification as Universal Practice

The near-universal "Well Diversified" classification across all 150 restaurants suggests that Auckland's restaurant operators have broadly adopted multi-channel strategies. However, the high average diversification score (0.980) may also reflect the relative immaturity of the market, where no single channel has yet achieved overwhelming dominance. As the market matures and aggregator consolidation continues, maintaining this diversification will require conscious effort.

---

## 6. Recommendations

### 6.1 Strategic Channel Balancing

Restaurants should aim for a target channel mix that balances volume growth with profitability. Based on the analysis, a recommended target distribution would be: In-Store 30–35%, Uber Eats 20–25%, DoorDash 18–22%, Self-Delivery 20–25%. This mix preserves In-Store profitability while maintaining meaningful aggregator presence and investing in self-delivery as a strategic hedge.

### 6.2 Self-Delivery Investment

Given the 22.9% profit margin on Self-Delivery versus 9.1% and 8.8% for Uber Eats and DoorDash respectively, restaurants should strategically invest in self-delivery infrastructure. This includes developing branded ordering platforms, building delivery fleets or partnering with white-label delivery providers, and creating loyalty programs that incentivise direct ordering. Even a 5 percentage point shift from aggregator to self-delivery channels would meaningfully improve overall profitability.

### 6.3 Cuisine-Specific Channel Strategies

Pizza and Indian restaurants should pursue aggressive self-delivery development to reduce their 55.2% and 52.6% aggregator dependence. Seafood restaurants, already demonstrating the highest self-delivery share (24.4%), should continue to differentiate on quality and build premium delivery experiences. Cafe & Brunch establishments, with their strong In-Store position (38.9%), should focus on enhancing the dine-in experience rather than chasing delivery volume.

### 6.4 Geographic Strategy Adaptation

Central Auckland restaurants should plan for a delivery-first reality, optimising kitchen throughput and packaging for delivery while using In-Store as a premium experience differentiator. Suburban restaurants should invest more heavily in In-Store experience and community engagement, using delivery as a complement rather than a primary channel.

### 6.5 Commission Negotiation and Monitoring

With commission rates ranging from 15–30% and averaging around 22%, restaurants should actively negotiate commission structures, particularly those with strong brand recognition and high order volumes. Establishing data-driven commission thresholds — below which aggregator participation is value-accretive and above which it becomes value-destructive — is essential for rational channel management.

### 6.6 Diversification Monitoring

While current diversification scores are healthy (mean: 0.980), restaurants should establish quarterly monitoring of their Channel Diversification Score and Aggregator Dependence Index. Any restaurant whose diversification score drops below 0.75 or whose aggregator dependence exceeds 55% should trigger a strategic review of channel allocation.

---

## 7. Limitations and Future Research

### 7.1 Limitations

This study is based on cross-sectional data representing a single monthly snapshot. Seasonal variations in ordering behaviour, particularly between summer and winter months in Auckland, are not captured. The dataset also does not include customer-level data, preventing analysis of cross-channel customer behaviour or lifetime value. Commission rates are modelled rather than directly observed, and actual rates may vary based on individual restaurant-aggregator negotiations.

### 7.2 Future Research Directions

Future research should investigate longitudinal trends in channel share evolution, customer-level cross-channel behaviour using loyalty program data, the impact of weather and seasonal factors on channel preference, and the competitive dynamics between Uber Eats and DoorDash as they vie for market share in the Auckland market. Additionally, a cost-benefit analysis of self-delivery infrastructure investment, accounting for both direct costs and indirect benefits (customer data ownership, brand control, flexibility), would provide valuable strategic guidance.

---

## 8. Conclusion

This comprehensive analysis of order channel performance and market share across SkyCity Auckland's restaurant ecosystem reveals a market in transition. Delivery channels now dominate order volume (68.6%), but In-Store dining remains the profitability backbone, generating 49.6% of net profit from just 31.4% of orders. The geographic, cuisine-specific, and segment-level variations uncovered in this analysis provide a nuanced understanding of the multi-channel landscape that can inform more targeted and effective channel strategies.

The key strategic imperative for Auckland restaurants is to balance delivery volume with profitability — using aggregator platforms for market reach and customer acquisition while investing in self-delivery capabilities and In-Store experience improvement to protect margins. The data clearly demonstrates that the most profitable path is not to abandon delivery but to manage it strategically, with conscious attention to channel mix, geographic adaptation, and cuisine-specific dynamics.

As the Auckland hospitality market continues to evolve, restaurants that maintain diversified channel portfolios, invest in self-delivery infrastructure, and make data-driven commission decisions will be best positioned to thrive in an increasingly delivery-driven ecosystem.

---

## References

1. Bimpikis, K., Candogan, O., & Saban, D. (2019). Spatial pricing in ride-sharing networks. *Operations Research*, 67(3), 744–769.
2. Cummings, R., & Doherty, M. (2021). Platform dependency in the restaurant industry: Margin erosion and strategic responses. *Journal of Hospitality Management*, 45(2), 112–128.
3. Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.
4. Auckland Tourism, Events and Economic Development (ATEED). (2024). Auckland hospitality market report.
5. Restaurant Association of New Zealand. (2024). Annual industry survey.
6. Uber Eats. (2024). New Zealand market insights report.
7. DoorDash. (2024). Australia and New Zealand merchant benchmarking study.

---

*Report prepared for SkyCity Auckland Restaurants & Bars — Order Channel Performance and Market Share Analytics Project*
