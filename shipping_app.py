import streamlit as st
from babel.numbers import format_currency

# Page configuration
st.set_page_config(
    page_title="Shipping Cost Calculator",
    page_icon="🚚",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🚚 Shipping Cost Calculator</div>', unsafe_allow_html=True)

# Constants
dt = 75000  # 20FT container cost
df = 150000  # 40FT container cost

def format_amount_in_currency(amount, currency='TZS', locale='en'):
    return format_currency(amount, currency, locale=locale)

def calculate_shipping_cost(d, pr, t, tri, wt, pro, car_type=None, fuel_efficiency=None):
    """Calculate shipping costs based on your business logic"""
    
    if t == "LCL":
        if car_type == "OTHER":  # Non-DOW ELEF truck
            d1 = d * 2
            f = round(d1 / fuel_efficiency)
            prc = f * pr
            al = tri * 31800
            tot = (prc + al + wt) * 1.18
            pre = pro / 100
            su = (tot * pre) + tot
            
        else:  # DOW ELEF trucks
            d1 = d * 2
            if car_type == "HOWO":
                f = round(d1 / 4)
            elif car_type == "FORD":
                f = round(d1 / 7)
            elif car_type == "BENZ":
                f = round(d1 / 7.5)
            elif car_type == "CANTER":
                f = round(d1 / 7)
            else:
                return None, None, None, None
                
            prc = f * pr
            al = tri * 40000
            tot = (prc + al + wt) * 1.18
            pre = pro / 100
            su = (tot * pre) + tot
            
    elif t == "20FT":
        d1 = d * 2
        f = round(d1 / 2)
        prc = f * pr
        al = tri * 31800
        tot = (prc + al + dt + wt) * 1.18
        pre = pro / 100
        su = (tot * pre) + tot
        
    elif t == "40FT":
        d1 = d * 2
        f = round(d1 / 2)
        prc = f * pr
        al = tri * 31800
        tot = (prc + al + df + wt) * 1.18
        pre = pro / 100
        su = (tot * pre) + tot
        
    else:
        return None, None, None, None
        
    return prc, al, tot, su

# Main form
with st.form("shipping_calculator"):
    st.header("📊 Enter Shipping Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        d = st.number_input("Delivery Distance (km)", min_value=1, value=100, step=10)
        pr = st.number_input("Fuel Price (TZS per liter)", min_value=1, value=2500, step=100)
        t = st.selectbox("Type of Shipment", ["LCL", "20FT", "40FT"])
        
    with col2:
        tri = st.number_input("Number of Days", min_value=1, value=3, step=1)
        wt = st.number_input("Wear and Tear Value (TZS)", min_value=0, value=50000, step=5000)
        pro = st.slider("Profit Margin (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
    
    # Conditional inputs for LCL shipments
    car_type = None
    fuel_efficiency = None
    
    if t == "LCL":
        st.subheader("🚛 Truck Details")
        lcl_col1, lcl_col2 = st.columns(2)
        
        with lcl_col1:
            is_dow_elef = st.radio("Is this a DOW ELEF truck?", ["Yes", "No"])
            
        with lcl_col2:
            if is_dow_elef == "Yes":
                car_type = st.selectbox("Select Truck Type", ["HOWO", "FORD", "BENZ", "CANTER"])
            else:
                car_type = "OTHER"
                fuel_efficiency = st.number_input("Fuel Efficiency (km per liter)", min_value=1.0, value=5.0, step=0.5)
    
    # Calculate button
    calculate_btn = st.form_submit_button("🚀 Calculate Shipping Costs", type="primary")

# Display results
if calculate_btn:
    st.success("✅ Calculation Complete!")
    
    # Perform calculation
    prc, al, tot, su = calculate_shipping_cost(d, pr, t, tri, wt, pro, car_type, fuel_efficiency)
    
    if prc is not None:
        # Display results in a nice layout
        st.markdown("---")
        st.header("💰 Cost Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Fuel Cost", format_amount_in_currency(prc))
            st.metric("Driver Allowance", format_amount_in_currency(al))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Total Cost", format_amount_in_currency(tot))
            st.metric("**Selling Price**", f"**{format_amount_in_currency(su)}**", 
                     delta=f"{pro}% profit margin")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed breakdown
        with st.expander("📋 View Detailed Calculation"):
            st.write(f"**Calculation Details:**")
            st.write(f"- Delivery Distance: {d} km (round trip: {d*2} km)")
            st.write(f"- Fuel Price: {format_amount_in_currency(pr)} per liter")
            st.write(f"- Shipment Type: {t}")
            st.write(f"- Trip Duration: {tri} days")
            st.write(f"- Wear and Tear: {format_amount_in_currency(wt)}")
            st.write(f"- Profit Margin: {pro}%")
            
            if t == "LCL":
                if car_type != "OTHER":
                    st.write(f"- DOW ELEF Truck: {car_type}")
                else:
                    st.write(f"- Fuel Efficiency: {fuel_efficiency} km/liter")
    
    else:
        st.error("Please check your inputs and try again.")

# Instructions when no calculation
else:
    st.info("👆 Fill in the form above and click 'Calculate Shipping Costs' to see your results!")