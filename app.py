import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Profit Leak Finder | Hospitality Solutions WA",
    page_icon="🍳",
    layout="centered"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; }
    .brand-header {
        font-size: 0.85rem; letter-spacing: 0.12em;
        text-transform: uppercase; color: #888; margin-bottom: 4px;
    }
    .big-number {
        font-family: 'Playfair Display', serif; font-size: 3.2rem;
        color: #c0392b; font-weight: 700; line-height: 1.1;
    }
    .leak-item {
        background: #fff8f7; border-left: 4px solid #c0392b;
        padding: 10px 16px; margin: 6px 0;
        border-radius: 0 6px 6px 0; font-size: 0.95rem;
    }
    .benchmark-box {
        background: #f4f8ff; border-left: 4px solid #2980b9;
        padding: 12px 16px; margin: 8px 0;
        border-radius: 0 6px 6px 0; font-size: 0.92rem;
    }
    .strategy-box {
        background: #f9fff4; border-left: 4px solid #27ae60;
        padding: 12px 16px; margin: 8px 0;
        border-radius: 0 6px 6px 0; font-size: 0.9rem;
    }
    .psychosocial-box {
        background: #fff8e1; border-left: 4px solid #f39c12;
        padding: 12px 16px; margin: 8px 0;
        border-radius: 0 6px 6px 0; font-size: 0.9rem;
    }
    .warning-box {
        background: #fff3f3; border-left: 4px solid #e74c3c;
        padding: 12px 16px; margin: 8px 0;
        border-radius: 0 6px 6px 0; font-size: 0.9rem;
    }
    .founding-box {
        background: #f0f7f0; border: 1px solid #27ae60;
        border-radius: 8px; padding: 16px 20px; margin-top: 20px;
    }
    .prefill-note { font-size: 0.8rem; color: #888; font-style: italic; }
    .deep-dive-header {
        background: #1a1a2e; color: white;
        padding: 12px 16px; border-radius: 6px;
        margin: 12px 0; font-size: 0.95rem;
    }
    .stButton > button {
        background-color: #c0392b; color: white; font-size: 1.1rem;
        font-weight: 600; border: none; padding: 0.6rem 2rem;
        border-radius: 6px; width: 100%;
    }
    .stButton > button:hover { background-color: #a93226; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INIT — preserves results across widget interactions
# ============================================================
if 'audit_run' not in st.session_state:
    st.session_state.audit_run = False
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = {}


# ============================================================
# SECTOR BENCHMARKS & STRATEGIES
# ============================================================
SECTOR_DATA = {
    "Cafe": {
        "cogs_low": 0.33, "cogs_high": 0.38,
        "wage_low": 0.30, "wage_high": 0.35,
        "prime_low": 0.63, "prime_high": 0.73,
        "bar_cogs_target": 0.22,
        "top_leak": "Alternative milk waste & over-portioning",
        "strategies": [
            {"name": "The Add-On Engine",
             "detail": "Coffee bean COGS is stable — but milk and labour are rising. Track modifier capture: syrups, extra shots, and alt-milk upsells carry 70%+ margins and directly subsidise the cost of a skilled barista. One extra modifier per transaction across 100 covers adds up fast."},
            {"name": "Batching Prep Cycles",
             "detail": "Shift from order-to-make for food items to batch-and-finish. Preparing components in 2-hour blocks rather than per-order reduces active labour minutes per plate and directly lowers your wage % per transaction."}
        ]
    },
    "Bistro / European": {
        "cogs_low": 0.28, "cogs_high": 0.32,
        "wage_low": 0.25, "wage_high": 0.30,
        "prime_low": 0.53, "prime_high": 0.62,
        "bar_cogs_target": 0.25,
        "top_leak": "Protein yield loss & menu bloat",
        "strategies": [
            {"name": "Secondary Cut Engineering",
             "detail": "Replace primary cuts (eye fillet) with high-flavour secondary cuts (bavette, beef cheek, oyster blade). Lower buy-in, higher yield, lower food cost — and a more interesting menu story."},
            {"name": "Dynamic Mid-Week Menus",
             "detail": "Reduce your menu by 40% Tuesday to Thursday. Less prep labour, less spoilage, cleaner execution on lower-volume days."}
        ]
    },
    "Hotel (F&B)": {
        "cogs_low": 0.25, "cogs_high": 0.30,
        "wage_low": 0.32, "wage_high": 0.38,
        "prime_low": 0.57, "prime_high": 0.68,
        "bar_cogs_target": 0.23,
        "top_leak": "Buffet waste & last-minute shift cancellations",
        "strategies": [
            {"name": "Cross-Departmental Floaters",
             "detail": "Train front-desk staff on basic F&B service. A multi-skilled internal pool lets you scale labour up or down without agency staff — and cancelled-shift costs are significant in 2026."},
            {"name": "Occupancy-Driven Buffet Yields",
             "detail": "Use occupancy data to adjust hot-holding volumes in 30-minute increments. Hotel breakfasts average 15% waste on fixed buffet models. Dynamic portioning halves that figure."}
        ]
    },
    "Pub / Bar": {
        "cogs_low": 0.30, "cogs_high": 0.36,
        "wage_low": 0.28, "wage_high": 0.34,
        "prime_low": 0.58, "prime_high": 0.70,
        "bar_cogs_target": 0.22,
        "top_leak": "Beverage over-pouring & untracked tab variances",
        "strategies": [
            {"name": "Pour Cost Discipline",
             "detail": "Beverage COGS should sit at 18–24%. Free-pouring, untracked staff drinks, and tab variances blow that number fast. A weekly spot-count on your top 5 spirits tells you everything."},
            {"name": "Kitchen Simplification",
             "detail": "Pub kitchens running restaurant-quality menus pay restaurant-quality labour. A tight 8–12 item menu with strong GP outperforms a 25-item menu requiring a full brigade."}
        ]
    },
    "Fine Dining": {
        "cogs_low": 0.28, "cogs_high": 0.35,
        "wage_low": 0.30, "wage_high": 0.35,
        "prime_low": 0.58, "prime_high": 0.70,
        "bar_cogs_target": 0.28,
        "top_leak": "Prep labour on from-scratch items & high-value ingredient variance",
        "strategies": [
            {"name": "The Two-Speed Menu",
             "detail": "Run a high-labour tasting menu alongside a low-labour bar or express menu. High-margin, low-prep bar items offset the intense labour of fine-dining plating and capture covers not committing to the full experience."},
            {"name": "Micro-Count Inventory",
             "detail": "Count your top 10 high-value items weekly — wagyu, truffle oil, premium spirits. A 2% variance on a $400 product is more impactful than a 10% variance in flour. Weekly visibility closes the gap fast."}
        ]
    }
}

# In-house production context labels
INHOUSE_LABELS = {
    10: "Dressings and sauces made in-house",
    20: "Plus crumbing items",
    30: "Plus house-made burgers, crumbing, dressings and sauces",
    40: "Plus trimming and portioning seafood and meats",
    50: "Plus all desserts made in-house",
    60: "Getting into everything territory — stocks, pastas, cures",
    70: "High-labour kitchen — most components produced from scratch",
    80: "Baking breads and making virtually everything from scratch"
}


# --- BRAND HEADER ---
st.markdown("<div class='brand-header'>Hospitality Solutions WA</div>", unsafe_allow_html=True)
st.markdown("<h1 style='margin-bottom:0'>The Profit Leak Finder</h1>", unsafe_allow_html=True)
st.markdown("""
**You already know something's off. Let's find out what it's actually costing you.**

No paywall. No pitch halfway through. Fill this in honestly and you'll have a real number in under three minutes.
""")
st.divider()


# ============================================================
# SECTION 1: CONTACT & BUSINESS DETAILS
# ============================================================
st.subheader("1. Tell Us About Your Venue")
st.caption("We use this to follow up with your results and to improve the tool.")

c1, c2 = st.columns(2)
with c1:
    contact_name = st.text_input("Your name")
    contact_email = st.text_input("Email address")
    contact_phone = st.text_input("Contact phone")
with c2:
    business_name = st.text_input("Business / venue name")
    business_website = st.text_input("Website", placeholder="e.g. www.yourvenue.com.au")
    years_operation = st.number_input("Years in operation", min_value=0, max_value=60, step=1)

c3, c4 = st.columns(2)
with c3:
    seating_capacity = st.number_input("Seating capacity (covers)", min_value=0, step=5)
    days_operation = st.multiselect(
        "Days of operation",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        default=["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
with c4:
    kitchen_staff = st.number_input("Kitchen staff (incl. casuals)", min_value=0, step=1)
    foh_staff = st.number_input("Front of house staff (incl. casuals)", min_value=0, step=1)

st.divider()


# ============================================================
# SECTION 2: THE NUMBERS
# ============================================================
st.subheader("2. The Numbers")
st.caption("Enter figures ex-GST. Weekly or monthly — your choice. Estimates are fine.")

col_v1, col_v2 = st.columns(2)
with col_v1:
    venue_type = st.selectbox(
        "Type of operation",
        ["Cafe", "Bistro / European", "Hotel (F&B)", "Pub / Bar", "Fine Dining"]
    )
    revenue_period = st.radio("Report your figures as", ["Weekly", "Monthly"])
    gross_sales_input = st.number_input(
        f"Gross sales (ex-GST) — {revenue_period} ($)", min_value=0, step=500
    )
    weekly_rev = gross_sales_input if revenue_period == "Weekly" else gross_sales_input / 4.33

with col_v2:
    food_costs_input = st.number_input(
        f"Food & beverage cost — {revenue_period} ($)", min_value=0, step=100
    )
    food_costs_weekly = food_costs_input if revenue_period == "Weekly" else food_costs_input / 4.33
    inflation_buffer = st.select_slider(
        "Supplier cost increase in the last 12 months (%)",
        options=[0, 5, 10, 15, 20], value=10
    )

st.markdown("**Wages**")
wage_split = st.radio("Can you separate kitchen wages from front-of-house?", ["Yes", "No — it's one number"])
wc1, wc2 = st.columns(2)
if wage_split == "Yes":
    with wc1:
        k_wages_input = st.number_input(f"Kitchen wages — {revenue_period} ($)", min_value=0, step=100)
    with wc2:
        foh_wages_input = st.number_input(f"FOH wages — {revenue_period} ($)", min_value=0, step=100)
    k_wages = k_wages_input if revenue_period == "Weekly" else k_wages_input / 4.33
    foh_wages = foh_wages_input if revenue_period == "Weekly" else foh_wages_input / 4.33
    total_wages = k_wages + foh_wages
else:
    with wc1:
        total_wages_input = st.number_input(f"Total wages — {revenue_period} ($)", min_value=0, step=100)
    total_wages = total_wages_input if revenue_period == "Weekly" else total_wages_input / 4.33
    k_wages = total_wages * 0.45
    foh_wages = total_wages * 0.55

st.divider()


# ============================================================
# SECTION 3: ONLINE ORDERING
# ============================================================
st.subheader("3. Online Ordering")
st.caption("If you're not on a platform, skip this section.")

uses_online = st.checkbox("We use third-party online ordering (Uber Eats, DoorDash, me&u, Mr Yum etc.)")

platform_leak_weekly = 0.0
platform_details = {}

if uses_online:
    st.multiselect("Which platforms?", ["Uber Eats", "DoorDash", "HungryPanda", "me&u", "Mr Yum", "Other"])
    platform_fee_pct = st.slider(
        "Average platform commission rate (%)",
        min_value=15, max_value=35, value=25, step=1,
        help="Uber Eats / DoorDash typically 25–35%. me&u / Mr Yum typically 5–15%."
    )
    online_sales_pct = st.number_input(
        "What % of your total sales comes through these platforms?",
        min_value=0.0, max_value=100.0, step=1.0, value=20.0
    )
    if weekly_rev > 0 and online_sales_pct > 0:
        online_sales_weekly = weekly_rev * (online_sales_pct / 100)
        platform_fee_weekly = online_sales_weekly * (platform_fee_pct / 100)
        direct_recovery = platform_fee_weekly * 0.20
        platform_leak_weekly = platform_fee_weekly
        platform_details = {
            "platform_fee_weekly": platform_fee_weekly,
            "direct_recovery": direct_recovery,
            "platform_fee_pct": platform_fee_pct,
            "online_sales_pct": online_sales_pct
        }

st.divider()


# ============================================================
# SECTION 4: OPERATIONAL AUDIT
# ============================================================
st.subheader("4. What's Actually Happening on the Floor")
st.caption("Tick what's true. No judgement.")

col3, col4 = st.columns(2)
with col3:
    retail_runs = st.checkbox("Retail runs to Coles/Woolies/IGA happen 2+ times a week")
    poor_layout = st.checkbox("Staff constantly crossing paths — kitchen flow is inefficient")
    old_gear = st.checkbox("Key equipment is 7+ years old (oven, fridge, dishwasher, combi)")
    stale_menu = st.checkbox("Menu hasn't been reviewed or updated in 12+ months")
with col4:
    hands_off_mgr = st.checkbox("Manager spends most time off the floor / in the office")
    no_wastage = st.checkbox("No wastage tracking — food goes in the bin, nobody records it")
    no_costing = st.checkbox("Dishes haven't been properly costed — pricing is based on feel")
    staff_turnover = st.checkbox("Lost 2+ key staff in the last 6 months")

st.markdown("---")
st.markdown("**Staffing Model**")
relies_on_casual = st.radio(
    "Does your roster rely on casual staff to fill shifts?",
    ["No — mostly permanent / part-time", "Yes — we regularly use casuals"]
)
labour_hire_weekly = 0.0
if relies_on_casual == "Yes — we regularly use casuals":
    casual_type = st.radio(
        "Are those casuals your own employees or through an agency / labour hire firm?",
        ["Our own casual employees", "Agency / Labour hire", "Mix of both"]
    )
    if casual_type in ["Agency / Labour hire", "Mix of both"]:
        lh_hours_band = st.select_slider(
            "Hours per week filled by agency / labour hire staff?",
            options=["Less than 10 hrs", "10–20 hrs", "20–30 hrs", "30+ hrs"],
            value="10–20 hrs"
        )
        hours_map = {"Less than 10 hrs": 7, "10–20 hrs": 15, "20–30 hrs": 25, "30+ hrs": 35}
        labour_hire_weekly = hours_map[lh_hours_band] * 8.00
        st.info(f"Estimated agency premium: **${labour_hire_weekly:,.0f}/week** above direct casual cost.")

st.divider()


# ============================================================
# SPLIT TEST: QUICK OR DEEP DIVE
# ============================================================
st.subheader("5. How Deep Do You Want to Go?")
st.markdown("""
The questions above will give you a solid starting number.

If you're willing to spend another 3–4 minutes, the deeper diagnostic will give you a significantly more accurate picture — and sector-specific financial analysis you can actually act on.
""")

deep_dive = st.toggle("I want the full diagnostic — give me the deeper questions")

# Deep dive variables — defaults
inhouse_pct = 0
specials_freq = "Never"
specials_sales_pct = 0.0
specials_cogs_pct = 0.0
themed_nights = False
themed_sales_pct = 0.0
set_menu = False
set_menu_sales_pct = 0.0
set_menu_cogs_pct = 0.0
eftpos_fee_pct = 1.5
staff_meals_tracked = True
packaging_tracked = True
packaging_pct = 0.0
is_licensed = False
alcohol_sales_pct = 0.0
has_tap_beer = False
tap_ownership = "Venue owns the taps"
line_clean_freq = "Weekly"
drink_menu_costed_months = 1
bar_cogs_pct = 0.0

if deep_dive:
    st.markdown("<div class='deep-dive-header'>🔬 Full Diagnostic — Kitchen</div>", unsafe_allow_html=True)

    # --- IN-HOUSE PRODUCTION ---
    st.markdown("**In-House Production**")
    inhouse_pct = st.select_slider(
        "What % of your ingredients / components are made in-house?",
        options=[10, 20, 30, 40, 50, 60, 70, 80],
        value=30
    )
    if inhouse_pct in INHOUSE_LABELS:
        st.caption(f"At {inhouse_pct}%: *{INHOUSE_LABELS[inhouse_pct]}*")

    # --- SPECIALS ---
    st.markdown("**Kitchen Specials**")
    st.caption("Specials = new dishes created daily, weekly or monthly. Not your parmi night price promotion.")
    specials_freq = st.radio(
        "How often does your kitchen run specials (new dishes)?",
        ["Never", "Daily", "Weekly", "Monthly"]
    )
    if specials_freq != "Never":
        specials_sales_pct = st.slider(
            "What % of total sales come from specials?",
            min_value=5, max_value=40, value=10, step=5,
            help="5% = specials barely register. 40% = your specials are carrying the menu."
        )
        specials_cogs_pct = st.number_input(
            "What is the average COGS % on your specials?",
            min_value=0.0, max_value=80.0, step=1.0, value=32.0,
            help="If you don't know, use your overall food cost % as a starting point."
        ) / 100

    # --- THEMED NIGHTS ---
    st.markdown("**Themed Nights / Promotional Events**")
    st.caption("Burger & beer nights, pizza deals, parmi nights, wing nights, trivia — any regular promotional event.")
    themed_nights = st.checkbox("We run regular themed nights or promotional food/drink events")
    if themed_nights:
        themed_sales_pct = st.slider(
            "What % of your weekly sales come from themed nights?",
            min_value=5, max_value=75, value=20, step=5,
            help="10% = themed nights add value but aren't critical. 75% = they're carrying your week."
        )

    # --- SET MENU ---
    st.markdown("**Set / Chef's Menu**")
    set_menu = st.checkbox("We offer a set menu (2 or 3 course, Chef's menu, Feed Me menu)")
    if set_menu:
        set_menu_sales_pct = st.slider(
            "What % of dinner service sales come from the set menu?",
            min_value=5, max_value=50, value=15, step=5
        )
        set_menu_cogs_pct = st.number_input(
            "COGS % on your set menu?",
            min_value=0.0, max_value=80.0, step=1.0, value=30.0
        ) / 100

    st.markdown("<div class='deep-dive-header'>🍸 Full Diagnostic — Front of House & Bar</div>", unsafe_allow_html=True)

    # --- EFTPOS / PAYMENT PROCESSING ---
    st.markdown("**Payment Processing**")
    eftpos_fee_pct = st.slider(
        "Average EFTPOS / payment processing fee (%)",
        min_value=0.5, max_value=3.0, value=1.5, step=0.1,
        help="Most venues pay 1.2–2.5% on all transactions. Check your merchant statement."
    )

    # --- STAFF MEALS ---
    st.markdown("**Staff Meals**")
    staff_meals_tracked = st.radio(
        "Are staff meals tracked and costed?",
        ["Yes — we have a policy and it's counted", "No — it's untracked / left to the team"]
    ) == "Yes — we have a policy and it's counted"

    # --- PACKAGING ---
    st.markdown("**Packaging & Consumables**")
    st.caption("Takeaway containers, coffee cups, bags, napkins, straws, sauce portions, biodegradable ware — anything that leaves the venue with the product.")
    packaging_tracked = st.radio(
        "Do you track packaging costs as a cost of sale?",
        ["Yes — it's in the COGS calculation", "No — it's absorbed as a general overhead"]
    ) == "Yes — it's in the COGS calculation"
    if not packaging_tracked:
        packaging_applies = st.checkbox("We use packaging (takeaway, coffee cups, delivery containers, condiment sachets etc.)")
        if packaging_applies:
            packaging_pct = st.slider(
                "Estimate what % of revenue goes to packaging and consumables",
                min_value=0.5, max_value=6.0, value=2.0, step=0.5,
                help="Cafes typically 1.5–3%. Delivery-heavy venues 3–6%. Dine-in restaurants 0.5–1.5%."
            )
        else:
            packaging_pct = 0.0
    else:
        packaging_pct = 0.0

    # --- LICENSED VENUE ---
    st.markdown("**Bar & Beverage**")
    is_licensed = st.checkbox("The venue is licensed (sells alcohol)")

    if is_licensed:
        alcohol_sales_pct = st.slider(
            "What % of total sales is alcohol / beverage?",
            min_value=5, max_value=80, value=30, step=5,
            help="Pubs typically 40–60%. Restaurants 25–35%. Cafes typically under 10%."
        )
        bar_cogs_pct = st.number_input(
            "Current bar COGS % (cost of alcohol sold as % of bar revenue)",
            min_value=0.0, max_value=60.0, step=1.0, value=25.0,
            help="Target for most venues: 18–28% depending on mix."
        ) / 100

        has_tap_beer = st.checkbox("We sell tap / draught beer")
        if has_tap_beer:
            tap_ownership = st.radio(
                "Who owns the beer taps?",
                ["Venue owns the taps", "Supplier / brewery owns the taps (free-on-loan)"],
                help="Supplier-owned taps lock you into their product and their pricing. You lose margin control."
            )
            line_clean_freq = st.radio(
                "How often are the beer lines cleaned?",
                ["Weekly", "Fortnightly", "Monthly or less", "We don't have a schedule"]
            )

        drink_menu_costed_months = st.radio(
            "When were your drink prices last reviewed and costed?",
            ["Within the last 3 months", "3–6 months ago", "6–12 months ago", "More than 12 months ago / never"]
        )

st.divider()


# ============================================================
# CALCULATION ENGINE
# ============================================================
sector = SECTOR_DATA[venue_type]
leaks = []
leak_total_weekly = 0.0
deep_dive_flags = []  # Non-dollar flags and warnings to surface in report

if weekly_rev > 0:

    # --- BASELINE ---
    amt = weekly_rev * 0.02
    leak_total_weekly += amt
    leaks.append({"label": "Baseline Invisible Slippage", "amount": amt,
        "note": "Even well-run venues lose ~2% to untracked micro-losses — mis-fires, portioning drift, unrecorded comps.",
        "fix": "A simple end-of-day waste log. A whiteboard in the kitchen is enough to start.",
        "psychosocial": None})

    if retail_runs:
        amt = weekly_rev * 0.035
        leak_total_weekly += amt
        leaks.append({"label": "Procurement / Retail Runs", "amount": amt,
            "note": "Retail prices run 30–60% above wholesale. Two runs a week adds up faster than it looks.",
            "fix": "A 14-day wholesale-only discipline with a single emergency cap per week typically closes this gap.",
            "psychosocial": None})

    if poor_layout and k_wages > 0:
        amt = k_wages * 0.12
        leak_total_weekly += amt
        leaks.append({"label": "Labour Inefficiency (Kitchen Flow)", "amount": amt,
            "note": "Poor flow means more labour hours for the same output. 10–15% of kitchen wages is conservative.",
            "fix": "Map where your team walks during a service. Move one piece of equipment. The difference is usually immediate.",
            "psychosocial": None})

    if old_gear:
        amt = weekly_rev * 0.02
        leak_total_weekly += amt
        leaks.append({"label": "Equipment Inefficiency", "amount": amt,
            "note": "Old equipment runs hotter, longer, and breaks. Gas, power, and call-out costs erode margin quietly.",
            "fix": "Get a single energy audit quote — most utility providers offer them free.",
            "psychosocial": None})

    if stale_menu or no_costing:
        amt = weekly_rev * 0.025
        leak_total_weekly += amt
        note = "If your menu hasn't moved but your costs have, you're subsidising your customers' meals." if stale_menu else "Uncosted dishes hide your worst performers. You may be losing money on your most popular item."
        leaks.append({"label": "Menu / Pricing Drift", "amount": amt, "note": note,
            "fix": "Cost your top 10 sellers first. Just those. The rest can wait.",
            "psychosocial": None})

    if hands_off_mgr and total_wages > 0:
        amt = total_wages * 0.08
        leak_total_weekly += amt
        leaks.append({"label": "Management Presence Gap", "amount": amt,
            "note": "A manager not on the floor during service is a cost without its return.",
            "fix": "Define when floor presence is non-negotiable. Structure the expectation, not the person.",
            "psychosocial": None})

    if no_wastage:
        amt = weekly_rev * 0.025
        leak_total_weekly += amt
        leaks.append({"label": "Untracked Wastage", "amount": amt,
            "note": "If you're not measuring it, it's not being managed. Untracked waste typically runs 2–4% of revenue.",
            "fix": "A $2 notebook and a daily tally changes behaviour immediately.",
            "psychosocial": None})

    if staff_turnover:
        amt = 1800 / 4
        leak_total_weekly += amt
        leaks.append({"label": "Staff Turnover Cost", "amount": amt,
            "note": "Replacing one experienced staff member costs $1,500–$3,000+ in recruitment, training, and lost productivity.",
            "fix": "Retention is cheaper than recruitment. What's one thing you could change this week your best person would notice?",
            "psychosocial": None})

    if platform_leak_weekly > 0:
        leak_total_weekly += platform_leak_weekly
        leaks.append({"label": f"Online Platform Fees ({platform_details['platform_fee_pct']}% commission)",
            "amount": platform_leak_weekly,
            "note": f"You're sending {platform_details['online_sales_pct']:.0f}% of revenue through platforms taking {platform_details['platform_fee_pct']}%.",
            "fix": f"Moving just 20% of those orders to direct ordering could recover ~${platform_details['direct_recovery']:,.0f}/week.",
            "psychosocial": None})

    if labour_hire_weekly > 0:
        leak_total_weekly += labour_hire_weekly
        leaks.append({"label": "Agency / Labour Hire Premium", "amount": labour_hire_weekly,
            "note": f"Estimated ${labour_hire_weekly:,.0f}/week in agency margin above direct casual employment cost.",
            "fix": "Build a direct casual pool of 3–5 reliable people. One month of recruitment removes agency dependency for most venues.",
            "psychosocial": "Your permanent staff work alongside strangers every week — different standards, different pace, no shared investment. Research links heavy agency reliance to lower morale, higher stress, and accelerated turnover in permanent staff."})

    # ---- DEEP DIVE LEAKS ----
    if deep_dive:

        # EFTPOS fees — always a real number
        if eftpos_fee_pct > 0:
            amt = weekly_rev * (eftpos_fee_pct / 100)
            leak_total_weekly += amt
            leaks.append({"label": f"Payment Processing Fees ({eftpos_fee_pct}%)", "amount": amt,
                "note": f"At {eftpos_fee_pct}%, you're paying ${amt:,.0f}/week in merchant fees. Most operators absorb this without tracking it.",
                "fix": "Review your merchant agreement. Switching providers or adding a surcharge on card payments can recover most of this.",
                "psychosocial": None})

        # Staff meals — untracked
        if not staff_meals_tracked:
            amt = (food_costs_weekly * 0.025) if food_costs_weekly > 0 else (weekly_rev * 0.008)
            leak_total_weekly += amt
            leaks.append({"label": "Staff Meals — Uncosted (Not Unvalued)", "amount": amt,
                "note": f"Untracked staff meals typically run 1.5–3% of food cost — around ${amt:,.0f}/week. This is not a cost to cut. A well-run staff meal program is one of the cheapest culture investments in hospitality. The goal is to own it: cost it, policy it, and make it intentional rather than invisible.",
                "fix": "Define a staff meal policy — one meal per shift from a set list. Cost it, track it, and own it as a deliberate investment in your team. The difference between a structured staff meal and an uncontrolled one isn't the food — it's the culture signal it sends.",
                "psychosocial": "Staff who eat well at work perform better, stay longer, and feel more respected. In an industry with chronic retention problems, a genuine staff meal policy is a retention tool as much as it is a food cost line. Don't eliminate it — illuminate it."})

        # Packaging — untracked
        if not packaging_tracked and packaging_pct > 0:
            amt = weekly_rev * (packaging_pct / 100)
            leak_total_weekly += amt
            leaks.append({"label": "Untracked Packaging & Consumables", "amount": amt,
                "note": f"At an estimated {packaging_pct}% of revenue, packaging is a real cost of sale — not overhead. At ${amt:,.0f}/week it belongs in your COGS calculation, not buried in a general expenses line.",
                "fix": "Add packaging to your COGS. It changes your true margin on every takeaway and delivery item, and gives you a lever to pull when costs rise — whether that's switching suppliers, reducing portion sachets, or adjusting pricing.",
                "psychosocial": None})

        # In-house production vs wages check
        if inhouse_pct >= 50 and total_wages > 0:
            wage_ratio_check = total_wages / weekly_rev if weekly_rev > 0 else 0
            if wage_ratio_check < sector["wage_low"]:
                deep_dive_flags.append({
                    "type": "warning",
                    "message": (
                        f"Your kitchen produces {inhouse_pct}% of components in-house — "
                        f"that's a significant labour investment. But your recorded wages sit below the "
                        f"sector benchmark. Either your labour is undercosted, or your in-house production "
                        f"isn't being reflected in your menu pricing. Check both."
                    )
                })
            if food_costs_weekly > 0:
                food_ratio = food_costs_weekly / weekly_rev
                if food_ratio > sector["cogs_high"]:
                    amt = weekly_rev * 0.02
                    leak_total_weekly += amt
                    leaks.append({"label": "In-House Production Yield Loss", "amount": amt,
                        "note": f"At {inhouse_pct}% in-house production, your food cost is still above benchmark. High production + high food cost = a yield or portioning discipline problem, not just a supplier cost problem.",
                        "fix": "Audit your top 5 in-house produced items for yield. Compare theoretical vs actual COGS on each.",
                        "psychosocial": None})

        # Specials analysis
        if specials_freq != "Never" and specials_sales_pct > 0:
            specials_revenue_weekly = weekly_rev * (specials_sales_pct / 100)
            sector_cogs_mid = (sector["cogs_low"] + sector["cogs_high"]) / 2
            if specials_cogs_pct > sector_cogs_mid + 0.05:
                amt = specials_revenue_weekly * (specials_cogs_pct - sector_cogs_mid)
                leak_total_weekly += amt
                leaks.append({"label": "Specials COGS Overrun", "amount": amt,
                    "note": f"Your specials COGS ({specials_cogs_pct*100:.0f}%) is running above your sector benchmark ({sector_cogs_mid*100:.0f}%). Specials should be engineered to improve margin, not erode it.",
                    "fix": "Specials exist to move high-yield product or tell a story. If the COGS is higher than your standard menu, they're working against you.",
                    "psychosocial": None})
            if specials_sales_pct < 8:
                deep_dive_flags.append({
                    "type": "info",
                    "message": f"Your specials account for less than 8% of sales. Given the prep, creativity, and communication effort involved, that return doesn't justify the investment. Either the concept, the price point, or the communication to customers needs work."
                })

        # Themed nights analysis
        if themed_nights and themed_sales_pct > 0:
            if themed_sales_pct < 10:
                deep_dive_flags.append({
                    "type": "warning",
                    "message": f"Your themed nights are generating less than 10% of weekly sales. The operational effort — dedicated prep, marketing, staffing adjustments — isn't being recouped at that level. Consider whether the concept is right or whether the resource is better directed elsewhere."
                })
            elif themed_sales_pct > 60:
                amt = weekly_rev * 0.03
                leak_total_weekly += amt
                leaks.append({"label": "Themed Night Revenue Concentration Risk", "amount": amt,
                    "note": f"Themed nights account for {themed_sales_pct}% of your weekly revenue. That's a structural dependency. If the concept loses popularity, a supplier issue interrupts it, or a competitor copies it — most of your week goes with it. The rest of your trade nights are functionally dead.",
                    "fix": "Start building a second revenue stream that works independently of the themed night. Even shifting 15% of that reliance to a different driver changes your risk profile significantly.",
                    "psychosocial": None})

        # Set menu analysis
        if set_menu and set_menu_sales_pct > 0 and set_menu_cogs_pct > 0:
            sector_cogs_mid = (sector["cogs_low"] + sector["cogs_high"]) / 2
            if set_menu_cogs_pct > sector_cogs_mid + 0.04:
                set_menu_rev = weekly_rev * (set_menu_sales_pct / 100)
                amt = set_menu_rev * (set_menu_cogs_pct - sector_cogs_mid)
                leak_total_weekly += amt
                leaks.append({"label": "Set Menu COGS Overrun", "amount": amt,
                    "note": f"Your set menu COGS ({set_menu_cogs_pct*100:.0f}%) is running above benchmark. Set menus should offer better COGS control than à la carte — predetermined quantities, no wastage variance.",
                    "fix": "Review portion sizes and the sourcing of the most expensive items in each course. Set menus that run high COGS are usually over-engineered for the price point.",
                    "psychosocial": None})

        # Bar / beverage leaks
        if is_licensed and alcohol_sales_pct > 0:
            bar_rev_weekly = weekly_rev * (alcohol_sales_pct / 100)
            bar_target = sector.get("bar_cogs_target", 0.25)

            if bar_cogs_pct > bar_target + 0.03:
                amt = bar_rev_weekly * (bar_cogs_pct - bar_target)
                leak_total_weekly += amt
                leaks.append({"label": "Bar COGS Above Target", "amount": amt,
                    "note": f"Your bar COGS is running at {bar_cogs_pct*100:.0f}% against a target of {bar_target*100:.0f}% for a {venue_type}. Over-pouring, untracked staff drinks, or stale pricing are the most common causes.",
                    "fix": "Weekly spot-count your top 5 spirits. Compare theoretical vs actual pour counts. The variance tells you where the leak is.",
                    "psychosocial": None})

            if has_tap_beer:
                if tap_ownership == "Supplier / brewery owns the taps (free-on-loan)":
                    deep_dive_flags.append({
                        "type": "warning",
                        "message": "Supplier-owned taps mean the supplier sets the product and effectively the margin. You lose the ability to negotiate, switch products, or optimise your pour cost. The 'free' tap equipment is not actually free — it's priced into the keg rate."
                    })
                if line_clean_freq in ["Monthly or less", "We don't have a schedule"]:
                    amt = bar_rev_weekly * 0.03
                    leak_total_weekly += amt
                    leaks.append({"label": "Tap Beer Line Wastage (Cleaning)", "amount": amt,
                        "note": "Lines not cleaned at least fortnightly accumulate bacterial build-up that requires extended purging before a clean pour. That's product waste, plus off-flavour beer that customers don't reorder.",
                        "fix": "Weekly line cleaning is best practice. Budget for the product waste in the cleaning cycle and track it separately.",
                        "psychosocial": None})

            if drink_menu_costed_months in ["3–6 months ago", "6–12 months ago", "More than 12 months ago / never"]:
                age_factor = {"3–6 months ago": 0.02, "6–12 months ago": 0.03, "More than 12 months ago / never": 0.04}
                factor = age_factor[drink_menu_costed_months]
                amt = bar_rev_weekly * factor
                leak_total_weekly += amt
                leaks.append({"label": "Stale Drink Pricing", "amount": amt,
                    "note": f"Drink prices not reviewed in over 3 months add an estimated {factor*100:.0f}% to your bar COGS as supplier costs move and your margin erodes. Spirits, wine, and tap beer pricing from distributors changes frequently.",
                    "fix": "A drink menu cost review takes one afternoon. Price increases of $0.50–$1.00 on key lines are rarely noticed by regular customers but add up significantly.",
                    "psychosocial": None})


# Ratios for benchmark panel
food_cost_ratio = (food_costs_weekly / weekly_rev) if weekly_rev > 0 and food_costs_weekly > 0 else 0
wage_ratio = (total_wages / weekly_rev) if weekly_rev > 0 and total_wages > 0 else 0
prime_cost_ratio = food_cost_ratio + wage_ratio
adjusted_cogs_high = sector["cogs_high"] + (inflation_buffer / 100)


# ============================================================
# RUN AUDIT BUTTON
# ============================================================
run_audit = st.button("SHOW ME WHERE IT'S GOING →")

if run_audit:
    if weekly_rev == 0:
        st.warning("Add your revenue figure above to get your number.")
    else:
        # Store everything in session state so widget interactions don't reset the results
        st.session_state.audit_run = True
        st.session_state.audit_results = {
            "annual_recovery": leak_total_weekly * 52,
            "leak_total_weekly": leak_total_weekly,
            "leaks": leaks,
            "deep_dive_flags": deep_dive_flags,
            "food_cost_ratio": food_cost_ratio,
            "wage_ratio": wage_ratio,
            "prime_cost_ratio": prime_cost_ratio,
            "adjusted_cogs_high": adjusted_cogs_high,
            "venue_type": venue_type,
            "sector": sector,
            "inflation_buffer": inflation_buffer,
            "wage_split": wage_split,
            "themed_nights": themed_nights,
            "themed_sales_pct": themed_sales_pct if themed_nights else 0,
            "days_operation": days_operation,
            "platform_leak_weekly": platform_leak_weekly,
            "labour_hire_weekly": labour_hire_weekly,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "business_name": business_name,
            "business_website": business_website,
        }

if st.session_state.audit_run and st.session_state.audit_results:
    r = st.session_state.audit_results
    annual_recovery = r["annual_recovery"]
    leaks = r["leaks"]
    deep_dive_flags = r["deep_dive_flags"]
    food_cost_ratio = r["food_cost_ratio"]
    wage_ratio = r["wage_ratio"]
    prime_cost_ratio = r["prime_cost_ratio"]
    adjusted_cogs_high = r["adjusted_cogs_high"]
    venue_type = r["venue_type"]
    sector = r["sector"]
    inflation_buffer = r["inflation_buffer"]
    wage_split = r["wage_split"]
    themed_nights = r["themed_nights"]
    themed_sales_pct = r["themed_sales_pct"]
    days_operation = r["days_operation"]
    platform_leak_weekly = r["platform_leak_weekly"]
    labour_hire_weekly = r["labour_hire_weekly"]
    contact_name = r["contact_name"]
    contact_email = r["contact_email"]
    contact_phone = r["contact_phone"]
    business_name = r["business_name"]
    business_website = r["business_website"]

    st.markdown("### Your estimated annual profit leakage:")
    st.markdown(f"<div class='big-number'>${annual_recovery:,.0f}</div>", unsafe_allow_html=True)
    st.caption("Directional, not exact — but real enough to act on.")
    st.markdown("")

    # BENCHMARK PANEL
    st.markdown("---")
    st.subheader(f"How Your {venue_type} Stacks Up Against 2026 Benchmarks")

    b1, b2, b3 = st.columns(3)
    with b1:
        cogs_target = f"{sector['cogs_low']*100:.0f}%–{adjusted_cogs_high*100:.0f}%"
        cogs_actual = f"{food_cost_ratio*100:.1f}%" if food_cost_ratio > 0 else "Not entered"
        cogs_status = "🔴" if food_cost_ratio > adjusted_cogs_high else ("🟡" if food_cost_ratio > sector["cogs_low"] else "🟢")
        st.metric("Food & Bev COGS", cogs_actual, f"Target: {cogs_target}")
        st.caption(f"{cogs_status} Benchmark (incl. {inflation_buffer}% pressure): {cogs_target}")
    with b2:
        wage_target = f"{sector['wage_low']*100:.0f}%–{sector['wage_high']*100:.0f}%"
        wage_actual = f"{wage_ratio*100:.1f}%" if wage_ratio > 0 else "Not entered"
        wage_status = "🔴" if wage_ratio > sector["wage_high"] else ("🟡" if wage_ratio > sector["wage_low"] else "🟢")
        st.metric("Wage %", wage_actual, f"Target: {wage_target}")
        st.caption(f"{wage_status} Benchmark: {wage_target}")
    with b3:
        prime_target = f"{sector['prime_low']*100:.0f}%–{sector['prime_high']*100:.0f}%"
        prime_actual = f"{prime_cost_ratio*100:.1f}%" if prime_cost_ratio > 0 else "Not entered"
        prime_status = "🔴" if prime_cost_ratio > sector["prime_high"] else ("🟡" if prime_cost_ratio > sector["prime_low"] else "🟢")
        st.metric("Prime Cost", prime_actual, f"Target: {prime_target}")
        st.caption(f"{prime_status} Benchmark: {prime_target}")

    st.markdown(f"""
    <div class='benchmark-box'>
        <strong>Top 2026 cost leak for {venue_type} operators:</strong> {sector['top_leak']}
    </div>
    """, unsafe_allow_html=True)

    # Revenue concentration warning (themed nights)
    if themed_nights and themed_sales_pct >= 60:
        other_nights = len(days_operation) - 1 if days_operation else 5
        st.markdown(f"""
        <div class='warning-box'>
            <strong>⚠️ Revenue Concentration Alert</strong><br>
            Your themed nights account for {themed_sales_pct}% of weekly revenue.
            That means your other {other_nights} trading days are generating only {100-themed_sales_pct}% of your income combined.
            When your most profitable night was making $30k and the rest of the week contributes $5k — that's not a well-run business, that's a one-trick operation with expensive overheads.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # LEAK REPORT
    st.subheader("Your Free Report: Where the Money is Going")
    st.markdown("Ranked by estimated weekly impact. Suggestions only — your venue is yours to run.")

    for i, leak in enumerate(sorted(leaks, key=lambda x: x["amount"], reverse=True), 1):
        st.markdown(f"""
        <div class='leak-item'>
            <strong>#{i} — {leak['label']}</strong><br>
            Weekly: <strong>${leak['amount']:,.0f}</strong> &nbsp;|&nbsp; Annual: <strong>${leak['amount']*52:,.0f}</strong><br>
            <span style='color:#555'>{leak['note']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"💡 One place to start: {leak['fix']}")
        if leak.get("psychosocial"):
            st.markdown(f"<div class='psychosocial-box'>⚠️ <strong>Beyond the invoice:</strong> {leak['psychosocial']}</div>", unsafe_allow_html=True)

    # Deep dive flags (non-dollar observations)
    if deep_dive_flags:
        st.markdown("---")
        st.markdown("**📋 Additional Observations**")
        for flag in deep_dive_flags:
            if flag["type"] == "warning":
                st.warning(flag["message"])
            elif flag["type"] == "info":
                st.info(flag["message"])

    if wage_split == "No — it's one number":
        st.info("📌 Kitchen wages estimated at 45% of total wage bill. Separating these will sharpen your picture.")

    # 2026 STRATEGIES
    st.divider()
    st.subheader(f"2026 Strategies for {venue_type} Operators")
    for s in sector["strategies"]:
        st.markdown(f"<div class='strategy-box'><strong>💡 {s['name']}</strong><br>{s['detail']}</div>", unsafe_allow_html=True)

    st.divider()

    # PREFILLED CTA
    st.subheader("Want to Go Deeper?")
    st.markdown("<p class='prefill-note'>Details pre-filled from above. Correct anything before submitting.</p>", unsafe_allow_html=True)
    cf1, cf2 = st.columns(2)
    with cf1:
        cta_name = st.text_input("Your name ", value=contact_name)
        cta_email = st.text_input("Email address ", value=contact_email)
        cta_phone = st.text_input("Contact phone ", value=contact_phone)
    with cf2:
        cta_business = st.text_input("Business name ", value=business_name)
        st.text_input("Website ", value=business_website)
        st.text_area("Anything specific you want to cover?",
            placeholder="e.g. struggling most with staffing costs and delivery platform margins...")

    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("👥 Join the Free Group Sessions", "https://hospitalitysolutions.com.au/")
    with col_b:
        st.link_button("📞 Book a Direct Conversation", "https://hospitalitysolutions.com.au/")

    st.caption("Hospitality Solutions WA · hospitalitysolutions.com.au")
    st.divider()

    # FOUNDING 250
    st.markdown("<div class='founding-box'>", unsafe_allow_html=True)
    st.markdown("#### You're one of the first 250 people to use this.")
    st.markdown("""
    This tool was built on experience, not a survey. Spend 90 seconds telling us what it missed or got wrong and we'll give you **four weeks of free group drop-in sessions** plus access to an AI assistant built on 20+ years of hospitality operations experience. No charge. No obligation.
    """)
    provide_feedback = st.toggle("Yes — I'll share feedback and claim my 4 weeks access")
    if provide_feedback:
        name_display = contact_name
        st.success(f"Thank you{', ' + name_display if name_display else ''}. You'll hear from us within 24 hours.")
        st.text_area("What did this tool miss?", placeholder="e.g. seasonal swings, rostering complexity...")
        st.text_area("What felt inaccurate?", placeholder="e.g. the agency cost estimate felt off...")
        st.text_area("What question should have been asked?", placeholder="e.g. 'Do you have a head chef or are you cooking yourself?'")
        st.selectbox("State / Territory", ["WA", "NSW", "VIC", "QLD", "SA", "TAS", "ACT", "NT"])
        if st.button("Submit My Feedback"):
            st.balloons()
            st.success("Received. Watch your inbox — thank you for making this better.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Version 2 — Built by someone who's worked the floor, not just studied it.")
