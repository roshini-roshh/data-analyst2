import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# --- Configuration ---
n_restaurants = 150

# Restaurant names inspired by SkyCity Auckland Restaurants & Bars
restaurant_names = [
    "The Grill by Sean Connelly", "Bellota", "The Sugar Club", "Masu",
    "Orbit 360° Dining", "Fortuna", "Gordon Bistro", "SkyBreeze Lounge",
    "Harbour Side Kitchen", "Auckland Steakhouse", "The Viaduct Eatery",
    "Queen Street Grill", "Parnell Pantry", "Ponsonby Bites", "Britomart Bar & Dine",
    "Federal Deli", "Depot Eatery", "Cafe Hanoi", "Amano Bakery & Kitchen",
    "Eddie's Noodle House", "The Downs", "K Road Social", "Wynyard Kitchen",
    "Takapuna Tapas", "Devonport Diner", "Milford Kitchen", "Birkenhead Bistro",
    "Northcote Noodle Bar", "Glenfield Grill", "Henderson House", "Waitakere Eatery",
    "New Lynn Noodles", "Avondale Arcade", "Kelston Kitchen", "Titirangi Table",
    "Onehunga Oasis", "Mt Eden Munch", "Kingsland Kitchen", "Sandringham Spice",
    "Mt Roskill Roti", "Three Kings Table", "Epsom Eatery", "Remuera Bistro",
    "Parnell Plate", "Newmarket Nosh", "Greenlane Grill", "Ellerslie Eats",
    "Mission Bay Kitchen", "St Heliers Bistro", "Kohimarama Kitchen",
    "Meadowbank Munch", "Glendowie Grill", "St Johns Kitchen",
    "SkyCity Grand Buffet", "SkyCity Corner Bar", "SkyCity Food Court Express",
    "Federal Street Diner", "Victoria Park Eats", "Wellesley Street Kitchen",
    "Cook Street Bites", "Lorne Street Lounge", "Albert Street Eatery",
    "Customs Street Kitchen", "Quay Street Seafood", "Commerce Street Cafe",
    "Swanson Street Diner", "Karangahape Road Kitchen", "Symonds Street Social",
    "Great North Road Grill", "Lincoln Road Eats", "Rosedale Kitchen",
    "Albany Bistro", "East Coast Bay Diner", "Mairangi Bay Kitchen",
    "Campbells Bay Cafe", "Murrays Bay Eatery", "Rothesay Bay Grill",
    "Brown Bay Kitchen", "Torbay Bistro", "Long Bay Diner",
    "Hobsonville Point Kitchen", "West Harbour Eatery", "Massey Grill",
    "Ranui Kitchen", "Te Atatu Bistro", "Point Chevalier Diner",
    "Western Springs Kitchen", "Westmere Eatery", "Herne Bay Grill",
    "Grey Lynn Kitchen", "Arch Hill Eats", "Newton Bistro",
    "Grafton Grill", "Eden Terrace Kitchen", "Mount Eden Village Eatery",
    "Balmoral Bites", "Lynfield Kitchen", "Hillsborough Grill",
    "One Tree Hill Diner", "Royal Oak Eatery", "Greenwoods Corner Kitchen",
    "Penrose Grill", "Otahuhu Kitchen", "Mangere Bridge Bistro",
    "Mangere East Eats", "Papatoetoe Diner", "Manukau Kitchen",
    "Clendon Grill", "Takanini Eatery", "Papakura Kitchen",
    "Pukekohe Bistro", "Wiri Kitchen", "Weymouth Grill",
    "Clevedon Eatery", "Beachlands Kitchen", "Maraetai Diner",
    "Half Moon Bay Bistro", "Howick Kitchen", "Pakuranga Grill",
    "Bucklands Beach Eatery", "Highland Park Kitchen", "Dannemora Diner",
    "Botany Downs Bistro", "Ormiston Kitchen", "Flat Bush Grill",
    "Manukau Heads Eatery", "Waiuku Kitchen", "Pukekohe East Diner",
    "Tuakau Bistro", "Waimauku Kitchen", "Helensville Grill",
    "Kumeu Eatery", "Riverhead Kitchen", "Wellsford Diner",
    "Warkworth Bistro", "Snells Beach Kitchen", "Orewa Grill",
    "Hatfields Beach Eatery", "Silverdale Kitchen", "Red Beach Diner",
    "Whangaparaoa Bistro", "Stanmore Bay Kitchen", "Gulf Harbour Grill",
    "Puhoi Eatery", "Leigh Kitchen", "Matakana Diner",
    "SkyCity VIP Lounge", "SkyCity Horizon Bar", "SkyCity Fusion House"
]

cuisine_types = ["Burgers", "Pizza", "Asian Fusion", "Seafood", "Steak & Grill",
                 "Cafe & Brunch", "Indian", "Mexican", "Mediterranean", "Sushi & Japanese"]

segments = ["Cafe", "QSR", "Casual Dining", "Fine Dining", "Fast Casual"]

subregions = ["North Shore", "West Auckland", "Central Auckland",
              "South Auckland", "East Auckland"]

# Subregion weight influences channel distribution
subregion_profiles = {
    "North Shore": {"instore": 0.30, "ubereats": 0.25, "doordash": 0.20, "selfdelivery": 0.25},
    "West Auckland": {"instore": 0.35, "ubereats": 0.20, "doordash": 0.25, "selfdelivery": 0.20},
    "Central Auckland": {"instore": 0.22, "ubereats": 0.30, "doordash": 0.28, "selfdelivery": 0.20},
    "South Auckland": {"instore": 0.32, "ubereats": 0.22, "doordash": 0.18, "selfdelivery": 0.28},
    "East Auckland": {"instore": 0.33, "ubereats": 0.24, "doordash": 0.22, "selfdelivery": 0.21},
}

# Cuisine influences
cuisine_profiles = {
    "Burgers": {"instore": 0.25, "ubereats": 0.30, "doordash": 0.25, "selfdelivery": 0.20},
    "Pizza": {"instore": 0.20, "ubereats": 0.30, "doordash": 0.30, "selfdelivery": 0.20},
    "Asian Fusion": {"instore": 0.28, "ubereats": 0.28, "doordash": 0.22, "selfdelivery": 0.22},
    "Seafood": {"instore": 0.40, "ubereats": 0.20, "doordash": 0.15, "selfdelivery": 0.25},
    "Steak & Grill": {"instore": 0.42, "ubereats": 0.20, "doordash": 0.18, "selfdelivery": 0.20},
    "Cafe & Brunch": {"instore": 0.50, "ubereats": 0.18, "doordash": 0.12, "selfdelivery": 0.20},
    "Indian": {"instore": 0.22, "ubereats": 0.32, "doordash": 0.28, "selfdelivery": 0.18},
    "Mexican": {"instore": 0.28, "ubereats": 0.28, "doordash": 0.24, "selfdelivery": 0.20},
    "Mediterranean": {"instore": 0.35, "ubereats": 0.25, "doordash": 0.20, "selfdelivery": 0.20},
    "Sushi & Japanese": {"instore": 0.30, "ubereats": 0.28, "doordash": 0.22, "selfdelivery": 0.20},
}

# Segment influences
segment_profiles = {
    "Cafe": {"monthly_orders_range": (300, 1200), "aov_range": (18, 35)},
    "QSR": {"monthly_orders_range": (800, 3000), "aov_range": (15, 28)},
    "Casual Dining": {"monthly_orders_range": (500, 2500), "aov_range": (30, 50)},
    "Fine Dining": {"monthly_orders_range": (200, 800), "aov_range": (55, 120)},
    "Fast Casual": {"monthly_orders_range": (600, 2200), "aov_range": (22, 40)},
}

# --- Generate Records ---
records = []
used_names = random.sample(restaurant_names, min(n_restaurants, len(restaurant_names)))
if n_restaurants > len(restaurant_names):
    for i in range(n_restaurants - len(restaurant_names)):
        used_names.append(f"SkyCity Restaurant {i+1}")

for i in range(n_restaurants):
    rid = f"R{1001+i}"
    rname = used_names[i]
    cuisine = random.choice(cuisine_types)
    segment = random.choice(segments)
    subregion = random.choice(subregions)

    # Blended channel shares from subregion + cuisine
    sr_p = subregion_profiles[subregion]
    cu_p = cuisine_profiles[cuisine]
    # 50/50 blend with some noise
    instore_s = 0.5 * sr_p["instore"] + 0.5 * cu_p["instore"] + np.random.normal(0, 0.03)
    ue_s = 0.5 * sr_p["ubereats"] + 0.5 * cu_p["ubereats"] + np.random.normal(0, 0.03)
    dd_s = 0.5 * sr_p["doordash"] + 0.5 * cu_p["doordash"] + np.random.normal(0, 0.03)
    sd_s = 0.5 * sr_p["selfdelivery"] + 0.5 * cu_p["selfdelivery"] + np.random.normal(0, 0.03)

    # Normalize to sum to 1
    total = instore_s + ue_s + dd_s + sd_s
    instore_s /= total
    ue_s /= total
    dd_s /= total
    sd_s /= total

    # Clamp and renormalize
    instore_s = max(0.05, instore_s)
    ue_s = max(0.05, ue_s)
    dd_s = max(0.05, dd_s)
    sd_s = max(0.05, sd_s)
    total = instore_s + ue_s + dd_s + sd_s
    instore_s /= total
    ue_s /= total
    dd_s /= total
    sd_s /= total

    # Monthly orders
    seg = segment_profiles[segment]
    monthly_orders = int(np.random.randint(seg["monthly_orders_range"][0], seg["monthly_orders_range"][1]))

    # Channel order counts
    instore_orders = int(round(monthly_orders * instore_s))
    ue_orders = int(round(monthly_orders * ue_s))
    dd_orders = int(round(monthly_orders * dd_s))
    sd_orders = monthly_orders - instore_orders - ue_orders - dd_orders
    if sd_orders < 0:
        sd_orders = 0
        # Recalculate
        total_assigned = instore_orders + ue_orders + dd_orders
        if total_assigned > monthly_orders:
            diff = total_assigned - monthly_orders
            ue_orders -= diff // 2
            dd_orders -= diff - (diff // 2)

    # AOV
    base_aov = np.random.uniform(seg["aov_range"][0], seg["aov_range"][1])
    # Delivery AOVs slightly higher (delivery fees, larger orders)
    instore_aov = round(base_aov * np.random.uniform(0.90, 1.05), 2)
    ue_aov = round(base_aov * np.random.uniform(1.05, 1.20), 2)
    dd_aov = round(base_aov * np.random.uniform(1.03, 1.18), 2)
    sd_aov = round(base_aov * np.random.uniform(0.98, 1.12), 2)

    # Revenue
    instore_rev = round(instore_orders * instore_aov, 2)
    ue_rev = round(ue_orders * ue_aov, 2)
    dd_rev = round(dd_orders * dd_aov, 2)
    sd_rev = round(sd_orders * sd_aov, 2)

    # Growth factor
    growth_factor = round(np.random.uniform(0.99, 1.05), 4)

    # AOV (weighted average)
    total_rev = instore_rev + ue_rev + dd_rev + sd_rev
    weighted_aov = round(total_rev / monthly_orders, 2) if monthly_orders > 0 else 0

    # COGS and OPEX rates
    cogs_rate = round(np.random.uniform(0.20, 0.40), 4)
    opex_rate = round(np.random.uniform(0.20, 0.55), 4)

    # Commission rate (for aggregators)
    commission_rate = round(np.random.uniform(0.15, 0.30), 4)

    # Delivery parameters
    delivery_radius = round(np.random.uniform(3, 18), 1)
    delivery_cost_order = round(np.random.uniform(0.89, 5.31), 2)

    # Self-delivery total cost
    sd_delivery_total_cost = round(sd_orders * delivery_cost_order, 2)

    # Net profits
    # In-Store: Revenue - COGS - OPEX
    instore_net = round(instore_rev * (1 - cogs_rate - opex_rate), 2)
    # Uber Eats: Revenue - COGS - OPEX - Commission
    ue_net = round(ue_rev * (1 - cogs_rate - opex_rate - commission_rate), 2)
    # DoorDash: Revenue - COGS - OPEX - Commission
    dd_net = round(dd_rev * (1 - cogs_rate - opex_rate - commission_rate), 2)
    # Self-Delivery: Revenue - COGS - OPEX - Delivery Cost
    sd_net = round(sd_rev * (1 - cogs_rate - opex_rate) - sd_delivery_total_cost, 2)

    # Channel shares (recomputed from actual orders)
    if monthly_orders > 0:
        instore_share = round(instore_orders / monthly_orders * 100, 2)
        ue_share = round(ue_orders / monthly_orders * 100, 2)
        dd_share = round(dd_orders / monthly_orders * 100, 2)
        sd_share = round(sd_orders / monthly_orders * 100, 2)
    else:
        instore_share = ue_share = dd_share = sd_share = 0

    records.append({
        "RestaurantID": rid,
        "RestaurantName": rname,
        "CuisineType": cuisine,
        "Segment": segment,
        "Subregion": subregion,
        "GrowthFactor": growth_factor,
        "AOV": weighted_aov,
        "MonthlyOrders": monthly_orders,
        "InStoreOrdersCount": instore_orders,
        "UberEatsOrdersCount": ue_orders,
        "DoorDashOrdersCount": dd_orders,
        "SelfDeliveryOrdersCount": sd_orders,
        "InStoreRevenue": instore_rev,
        "UberEatsRevenue": ue_rev,
        "DoorDashRevenue": dd_rev,
        "SelfDeliveryRevenue": sd_rev,
        "COGSRate": cogs_rate,
        "OPEXRate": opex_rate,
        "CommissionRate": commission_rate,
        "DeliveryRadiusKM": delivery_radius,
        "DeliveryCostOrder": delivery_cost_order,
        "SD_DeliveryTotalCost": sd_delivery_total_cost,
        "InStoreNetProfit": instore_net,
        "UberEatsNetProfit": ue_net,
        "DoorDashNetProfit": dd_net,
        "SelfDeliveryNetProfit": sd_net,
        "InStoreShare": instore_share,
        "UE_share": ue_share,
        "DD_share": dd_share,
        "SD_share": sd_share,
    })

df = pd.DataFrame(records)

# --- Validation ---
df["ComputedTotal"] = df["InStoreOrdersCount"] + df["UberEatsOrdersCount"] + df["DoorDashOrdersCount"] + df["SelfDeliveryOrdersCount"]
df["OrdersMatch"] = df["ComputedTotal"] == df["MonthlyOrders"]
mismatches = df[~df["OrdersMatch"]]
if len(mismatches) > 0:
    print(f"WARNING: {len(mismatches)} records have order count mismatches. Fixing...")
    # Fix by adjusting SelfDeliveryOrdersCount
    df.loc[~df["OrdersMatch"], "SelfDeliveryOrdersCount"] = (
        df.loc[~df["OrdersMatch"], "MonthlyOrders"]
        - df.loc[~df["OrdersMatch"], "InStoreOrdersCount"]
        - df.loc[~df["OrdersMatch"], "UberEatsOrdersCount"]
        - df.loc[~df["OrdersMatch"], "DoorDashOrdersCount"]
    )
    # Recalculate shares
    df["InStoreShare"] = round(df["InStoreOrdersCount"] / df["MonthlyOrders"] * 100, 2)
    df["UE_share"] = round(df["UberEatsOrdersCount"] / df["MonthlyOrders"] * 100, 2)
    df["DD_share"] = round(df["DoorDashOrdersCount"] / df["MonthlyOrders"] * 100, 2)
    df["SD_share"] = round(df["SelfDeliveryOrdersCount"] / df["MonthlyOrders"] * 100, 2)
    # Recalculate Self-Delivery Revenue and Net Profit
    df["SelfDeliveryRevenue"] = round(df["SelfDeliveryOrdersCount"] * (df["SelfDeliveryRevenue"] / (df["SelfDeliveryOrdersCount"].replace(0, 1))), 2)

df["ShareSum"] = df["InStoreShare"] + df["UE_share"] + df["DD_share"] + df["SD_share"]
print(f"Share sum stats: min={df['ShareSum'].min():.2f}, max={df['ShareSum'].max():.2f}, mean={df['ShareSum'].mean():.2f}")

# Drop helper columns
df.drop(columns=["ComputedTotal", "OrdersMatch", "ShareSum"], inplace=True)

# Save
df.to_csv("skycity_auckland_restaurants.csv", index=False)
print(f"\nDataset generated: {len(df)} restaurants, {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")
print(f"\nSubregion distribution:\n{df['Subregion'].value_counts()}")
print(f"\nCuisine distribution:\n{df['CuisineType'].value_counts()}")
print(f"\nSegment distribution:\n{df['Segment'].value_counts()}")
print(f"\nSample data (first 3 rows):")
print(df.head(3).to_string())
