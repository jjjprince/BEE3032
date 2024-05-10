import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import math
import pandas as pd
import opstrat as op
from Calculations import OneStepBinomialTreePricingModel
from Calculations import TwoStepBinomialTreePricingModel
from Calculations import OptionsGreeks
from Calculations import NoArbitragePricing
from Calculations import FuturesAndForwardsValuation

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Futures and Forwards", "Hedging", "Options Strategies","Risk Neutral Probabilities and Cox-Rubenstein", "Binomial Trees"])
with tab1:
    st.title("Futures and Forwards Calculations")
    st.subheader("No Arbitrage Pricing", divider="red")
    st.write("Select from options below")
    type = st.selectbox("What type of futures contract are you pricing?",
                 ("Standard","Commodity with Storage Costs and Convenience Yield", "Stock Index", "Exchange Rate", "Known Income")
                 )
    
    # Initalise Variable
    s_0 = 0
    r = 0
    T = 0
    u = 0
    y = 0
    q = 0
    r_f = 0
    I = 0

    col1, col2 = st.columns(2)
    with col1:
        s_0 = st.number_input("Spot Price",min_value=0.001)
    with col2:
        T = st.number_input("Months to expiry", min_value=0.001)/12

    if type == "Standard":
        col1, col2 = st.columns(2)
        with col1:
            r  = st.number_input("Domestic Interest Rate (%)", min_value=0.001, key = "std")/100
    elif type == "Commodity with Storage Costs and Convenience Yield":
        col1, col2 = st.columns(2)
        with col1:
            r  = st.number_input("Domestic Interest Rate (%)", min_value=0.001, key = "commod")/100
            y = st.number_input("Convenience Yield Per Period",min_value=0.001)
        with col2:
            u = st.number_input("Storage Cost Per Period",min_value=0.001)
    elif type == "Stock Index":
        col1, col2 = st.columns(2)
        with col1:
            r  = st.number_input("Domestic Interest Rate (%)", min_value=0.001, key = "indx")/100
        with col2:
            q = st.number_input("Dividend Yield",min_value=0.001)
    elif type == "Exchange Rate":
        col1, col2 = st.columns(2)
        with col1:
            r  = st.number_input("Domestic Interest Rate (USDXXX) (%)", min_value=0.001, key = "exch")/100
        with col2:
            r_f = st.number_input("Foreign Interest Rate (XXXUSD) (%)",min_value=0.001)/100
        st.write("In a USD/GBP pair, GBP interest rate is domestic and foreign is the US interest rate")
    elif type == "Known Income":
        col1, col2 = st.columns(2)
        with col1:
            r  = st.number_input("Domestic Interest Rate (%)", min_value=0.001, key = "KI")/100
        with col2:
            I = st.number_input("PV of Future Income",min_value=0.001,)
            st.write("")
        st.write("PV of Future Income is determined by the formula:")
        st.latex(r'''
            I = i_1e^{-r}+i_2e^{-2r}+i_3e^{-3r}...
                 ''')
        st.write("where i denotes income in the given period")
    
    price_calculator = NoArbitragePricing(s_0,r,T,u,y,q,r_f,I)
    if type == "Standard":
        price = price_calculator.simple_price()
        st.write(s_0)
    elif type == "Commodity with Storage Costs and Convenience Yield":
        price = price_calculator.commodity_futures_price()
    elif type == "Stock Index":
        price = price_calculator.stock_index_price()
    elif type == "Exchange Rate":
        price = price_calculator.exchange_rate_price()
    elif type == "Known Income":
        price = price_calculator.KI_price()
    
    st.write("")
    st.write("Futures Price = ",round(price,4))

    st.subheader("Valuation of Futures/Forwards Position", divider ="red")
    K = price
    placehold = str(price)
    
    col1,col2 = st.columns(2)
    with col1:
        direction = st.selectbox("Long or Short Position?",("Long","Short"))
        f_0 = st.number_input("Current Forward Price", min_value = 0.001)
        r = st.number_input("Domestic Interest Rate (%)",min_value=0.001)/100
    with col2:
        N = st.number_input("Number of Contracts",min_value=0)
        K = st.number_input("Forward Price Agreed at Inception",min_value=0.001)
        T = st.number_input("Number of Months",  min_value=0.001)/12

    valuation_model = FuturesAndForwardsValuation (f_0,K,r,T)
    if direction == "Long":
        value = valuation_model.LongValue()
    elif direction == "Short":
        value = valuation_model.ShortValue()

    value = value * N
    st.write("")
    st.write("Position Value = ",round(value,4))

with tab2:
    st.title("Hedging Calculations")
    st.subheader("Average Price Paid", divider="red")
    col1, col2 = st.columns(2)
    with col1:
        s_0 = st.number_input("Current Spot Rate", min_value=0.001)
        R = st.number_input("% of total holdings hedged", min_value=0.001)/100
        K = st.number_input("Forward Price Agreed at Inception", min_value=0.001, key="imperf")
    with col2:
        q = st.number_input("Quantity", min_value=0.001)
        f_0 = st.number_input("Current Forward Price", min_value = 0.001,key="noarb")

    app  = R*(s_0-f_0+K) + (1-R)*s_0
    basis = s_0-f_0
    app_exp = R*K + (1-R)*s_0

    st.write("Average Price Paid (Now) = ",round(app,4))
    st.write("Basis Risk = ",round(basis,4))
    st.write("Average Price Paid (Expiry) = ",round(app_exp,4))

    st.subheader("Cross Hedging", divider="red")
    col1,col2=st.columns(2)
    with col1:
        rho = st.number_input("Correlation between assets",min_value=0.001)
        std_dev = st.number_input("Standard Deviation in Target Asset", min_value=0.001)
    with col2:
        std_dev_s = st.number_input("Standard Deviation in Hedging Asset", min_value=0.001)

    h_star = rho *  (std_dev/std_dev_s)
    st.write("Optimal Hedge Ratio = ",round(h_star,4))
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        Q_A = st.number_input("Size of position to be hedged", min_value=0.001)
        h_ = st.number_input("Optimal Hedge Ratio")
    with col2:
        Q_F = st.number_input("Size of substitute futures contract", min_value=0.001)
    
    n_star = h_ * (Q_A)/Q_F
    
    st.write("Number of futures needed to cross-hedge exposure = ",round(app,4))

with tab3:
    st.title("Options Strategy Pricing and Payoffs")
    #Dfault Parameters
    T = 0
    S_t = 100
    K1 = 100
    K2 = 100
    K3 = 100
    K4 = 100

    st.subheader("Select Option Type and Provide Details", divider = "red")
    col1 , col2, col3 = st.columns(3)
    with col1:
        type = st.selectbox(
                "What type of options stucture?",
                ('Call Spread','Put Spread','Straddle','Strangle','Butterfly','Reverse Butterfly','Box Spread'))
    with col2:
            spot = st.number_input("Current spot", min_value=0.0001,key="<strategy1>")
            s_t = spot
    with col3:
        quantity = st.number_input("Quantity Bought", min_value=1,key="<strategy2>")
        q = quantity

    if type == "Call Spread":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Lower Strike", min_value=0.0001, key="csk1")
            K2 = st.number_input("Higher Strike", min_value=0.0001,key="csk2")
        with col2:
            p1 = st.number_input("Price of Lower Strike", min_value=0.0001,key="csp1")
            p2 = st.number_input("Price of Higher Strike", min_value=0.0001,key="csp2")

        st.text("")
        p = p1-p2
        breakeven = K1 + p
        st.write(f"Price of Strategy: {round(p,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven,4)}")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'c','strike':K2,'tr_type':'s','op_pr':p2}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

    if type == "Put Spread":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Higher Strike", min_value=0.0001, key="psk1")
            K2 = st.number_input("Lower Strike", min_value=0.0001,key="psk2")
        with col2:
            p1 = st.number_input("Price of Higher Strike", min_value=0.0001,key="psp1")
            p2 = st.number_input("Price of Lower Strike", min_value=0.0001,key="psp2")

        st.text("")
        p = p1-p2
        breakeven = K1 - p
        st.write(f"Price of Strategy: {round(p,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven,4)}")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'p','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'p','strike':K2,'tr_type':'s','op_pr':p2}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

    if type == "Straddle":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Strike", min_value=0.0001, key="stradk1")
        with col2:
            p1 = st.number_input("Price of Call", min_value=0.0001,key="stradp1")
            p2 = st.number_input("Price of Put", min_value=0.0001,key="stradp2")

        st.text("")
        p = p1+p2
        breakeven_l = K1 - p
        breakeven_h = K1 + p
        st.write(f"Price of Strategy: {round(p,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven_l,4)} and {round(breakeven_h,4)} ")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'p','strike':K1,'tr_type':'b','op_pr':p2}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)
    
    if type == "Strangle":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Call Strike", min_value=0.0001, key="strangk1")
            K2 = st.number_input("Put Strike", min_value=0.0001,key="strangk2")
        with col2:
            p1 = st.number_input("Price of Call", min_value=0.0001,key="strangp1")
            p2 = st.number_input("Price of Put", min_value=0.0001,key="strangp2")

        st.text("")
        p = p1+p2
        breakeven_l = K2 - p
        breakeven_h = K1 + p
        st.write(f"Price of Strategy: {round(p,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven_l,4)} and {round(breakeven_h,4)} ")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'p','strike':K2,'tr_type':'b','op_pr':p2}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

    if type == "Butterfly":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Lower Strike", min_value=0.0001, key="bflyk1")
            K2 = st.number_input("Middle Strike", min_value=0.0001, key="bflyk2")
            K3 = st.number_input("Upper Strike", min_value=0.0001, key="bflyk3")
        with col2:
            p1 = st.number_input("Price of Lower Strike", min_value=0.0001, key="bflyp1")
            p2 = st.number_input("Price of Middle Strike", min_value=0.0001, key="bflyp2")
            p3 = st.number_input("Price of Upper Strike", min_value=0.0001, key="bflyp3")

        st.text("")
        p = (p1 - 2*p2 + p3)
        pq = (p1 - 2*p2 + p3) * q
        breakeven_l = K1  + p
        breakeven_h = K3 - p
        max_payoff = (K3 - K2 - p) * q

        st.write(f"Price of Strategy: {round(pq,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven_l,4)} and {round(breakeven_h,4)} ")
        st.write(f"Maximum Payoff of \$ {round(max_payoff,4)} occurs when spot price is ${K2}")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'c','strike':K2,'tr_type':'s','op_pr':p2}
        op_3={'op_type':'c','strike':K2,'tr_type':'s','op_pr':p2}
        op_4={'op_type':'c','strike':K3,'tr_type':'b','op_pr':p3}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2,op_3,op_4])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

    if type == "Reverse Butterfly":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("Lower Strike", min_value=0.0001, key="rbflyk1")
            K2 = st.number_input("Middle Strike", min_value=0.0001, key="rbflyk2")
            K3 = st.number_input("Upper Strike", min_value=0.0001, key="rbflyk3")
        with col2:
            p1 = st.number_input("Price of Lower Strike", min_value=0.0001, key="rbflyp1")
            p2 = st.number_input("Price of Middle Strike", min_value=0.0001, key="rbflyp2")
            p3 = st.number_input("Price of Upper Strike", min_value=0.0001, key="rbflyp3")

        st.text("")
        p = (2*p2 - p1 - p3)
        pq = (-p1 +2*p2 - p3) * q
        breakeven_l = K1 - p
        breakeven_h = K3 + p
        max_payoff = (K3 - K2 - p) * q

        st.write(f"Price of Strategy: {round(pq,4)}")
        st.write(f"Breakeven Spot Price: {round(breakeven_l,4)} and {round(breakeven_h,4)} ")
        st.write(f"Maximum Payoff of \$ {round(max_payoff,4)} occurs when spot price is $\leq$ \${K1} or $\geq$ \${K3}")
        st.write("$^*$Breakeven price assumes no movement in underlying option value, prices shown below at expiry")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'s','op_pr':p1}
        op_2={'op_type':'c','strike':K2,'tr_type':'b','op_pr':p2}
        op_3={'op_type':'c','strike':K2,'tr_type':'b','op_pr':p2}
        op_4={'op_type':'c','strike':K3,'tr_type':'s','op_pr':p3}
        fig = op.multi_plotter(spot=s_t, spot_range=30, op_list=[op_1,op_2,op_3,op_4])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

    if type == "Box Spread":
        col1 , col2 = st.columns(2)
        with col1:
            K1 = st.number_input("ITM Call/ OTM Put Strike", min_value=0.0001, key="boxc1")
            K2 = st.number_input("OTM Call/ ITM Put Strike", min_value=0.0001, key="boxc2")
            st.write("REMINDER: ITM Call/OTM Put is the lower strike and OTM Call/ITM Put is the higher strike")

        with col2:
            p1 = st.number_input("Price of ITM Call", min_value=0.0001, key="cboxp1")
            p2 = st.number_input("Price of OTM Put", min_value=0.0001, key="pboxp1")
            p3 = st.number_input("Price of ITM Put", min_value=0.0001, key="pboxp2")
            p4 = st.number_input("Price of OTM Call", min_value=0.0001, key="cboxp2")

        st.text("")
        p = p1 - p2 + p3 - p4
        pq = (p1 - p2 + p3 - p4) * q
        payoff = (K2 - K1 - p) * q

        st.write(f"Price of Strategy: {round(pq,4)}")
        st.write(f"Guaranteed Payoff of \$ {round(payoff,4)}")
        st.text("")
        op_1={'op_type':'c','strike':K1,'tr_type':'b','op_pr':p1}
        op_2={'op_type':'p','strike':K1,'tr_type':'s','op_pr':p2}
        op_3={'op_type':'p','strike':K2,'tr_type':'b','op_pr':p3}
        op_4={'op_type':'c','strike':K2,'tr_type':'s','op_pr':p4}
        fig = op.multi_plotter(spot = s_t, spot_range = 30,op_list=[op_1,op_2,op_3,op_4])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)

with tab4:
    title = "Futures and Options Calculations"
    st.title("Risk Neutral Probabilities and Cox-Rubenstein")
    st.subheader("Risk Neutral Probabilities", divider="red")

    col1, col2, col3 = st.columns(3)
    with col1:
        r = st.number_input("Interest rate (%)$^*$", min_value=0.0001, key="<riskneutral1>") / 100
        s_u = st.number_input("Future Stock Price ($S_u$)", min_value=0.0001, key="<riskneutral4>")
    with col2:
        t = st.number_input("Number of Months Per Step", min_value=1, key="<riskneutral2>")
        s_d = st.number_input("Future Stock Price ($S_d$)", min_value=0.0001, key="<riskneutral5>")
    with col3:
        s_t = st.number_input("Spot Price", min_value=0.0001, key="<riskneutral3>")
        u = s_u / s_t
        d = s_d / s_t
        p = None
        if u != d:
            p = (math.exp(r*t/12)-d)/(u-d)
    if p  is not None:
        col1, col2 =st.columns(2)
        st.write("$^*$ Interest rate assuming continuous compounding")
        st.write("Stock Growth Factor",round(u,4))
        st.write("Stock Decay Factor",round(d,4))
        st.write("Risk Neutral Probability", round(p,4))

    st.text("")
    st.subheader("Cox-Rubenstein Cofficients", divider = "red")
    col1, col2, col3 = st.columns(3)
    with col1:
        sigma = st.number_input("Annualised Volatility (%)$^*$", min_value=0.0001) / 100
    with col2:
        time = st.number_input("Number of Months Per Step", min_value=1, key="<riskneutral2")
        t = time
   
    u = math.exp(sigma* math.sqrt(t/12))
    d = math.exp(-sigma* math.sqrt(t/12))

    col1, col2 =st.columns(2)
    st.write("$^*$ Interest rate assuming continuous compounding")
    st.write("Stock Growth Factor",round(u,4))
    st.write("Stock Decay Factor",round(d,4))   

with tab5:
    title = "Futures and Options Calculations"
    st.title("Binomial Trees")

    st.subheader("Calculation Inputs" ,divider="red")
    col1, col2, col3 = st.columns(3)
    with col1:
        type = st.radio(
            "What type of option?",
            ('Call','Put'))
    with col2:
        style = st.radio(
            "What style of option?",
            ('European','American'))

    col1, col2, col3 = st.columns(3)
    with col1:
        spot = st.number_input("Current spot", min_value=0.0001)
        s_t = spot
    with col2:
        K = st.number_input("Excercise Price", min_value=0.001)
    with col3:
        r = st.number_input("Interest rate (%)$^*$", min_value=0.0001) / 100

    col1, col2, col3 = st.columns(3)
    with col1:
        time = st.number_input("Number of Months Per Step", min_value=1)
        t = time
        u = st.number_input("Stock Growth Factor", min_value=0.0001)
    with col2:
        T = st.number_input("Number of Steps", min_value=1, max_value=3)
        d = st.number_input("Stock Decay Factor", min_value=0.0001)
        d_auto = 1/u
        p = 0
        if u != d:
            p = (math.exp(r*t/12)-d)/(u-d)
    with col3:
        st.write("Stock Decay Factor Auto-Calculated as")
        st.write("$d = \\frac{1}{u}=$",round(d_auto,4))
 
    # Define Step Spot Prices
    s_u = s_t * u
    s_uu = s_t * u**2
    s_ud = s_du = s_t * u * d
    s_d= s_t * d
    s_dd = s_t * d**2
    
    if u != d:
        try:
            if T == 1 and style == "European":
                if type == "Call":
                    pricing_model = OneStepBinomialTreePricingModel(s_u,s_d,K,t,p,r)  # Initialize the model
                    f_u, f_d, f = pricing_model.one_step_call()  # Call the method
                elif type == "Put":
                    pricing_model = OneStepBinomialTreePricingModel(s_u,s_d,K,t,p,r)  # Initialize the model
                    f_u, f_d, f = pricing_model.one_step_put()  # Call the method
            elif T == 2:
                if style == "European":
                    if type == "Call":
                        pricing_model = TwoStepBinomialTreePricingModel(s_t,s_u,s_uu,s_ud,s_d,s_dd,K,t,p,r)  # Initialize the model
                        f_uu, f_ud, f_dd, f_u, f_d, f = pricing_model.two_step_call_EU()  # Call the method
                    elif type == "Put":
                        pricing_model = TwoStepBinomialTreePricingModel(s_t,s_u,s_uu,s_ud,s_d,s_dd,K,t,p,r)  # Initialize the model
                        f_uu, f_ud, f_dd, f_u, f_d, f = pricing_model.two_step_put_EU()  # Call the method
                elif style == "American":
                    if type == "Call":
                        pricing_model = TwoStepBinomialTreePricingModel(s_t,s_u,s_uu,s_ud,s_d,s_dd,K,t,p,r)  # Initialize the model
                        f_uu, f_ud, f_dd, f_u, f_d, f = pricing_model.two_step_call_US()  # Call the method
                    elif type == "Put":
                        pricing_model = TwoStepBinomialTreePricingModel(s_t,s_u,s_uu,s_ud,s_d,s_dd,K,t,p,r)  # Initialize the model
                        f_uu, f_ud, f_dd, f_u, f_d, f = pricing_model.two_step_put_US()  # Call the method
        except ValueError as ve:
            # Handle ValueError
            st.error(f"ValueError: {ve}")
        except ZeroDivisionError as zd:
            # Handle ZeroDivisionError
            st.error(f"ZeroDivisionError: {zd}")
        except Exception as e:
            # Handle other exceptions
            st.error(f"An error occurred during calculation: {e}") 
            
    if p != 0:
        st.subheader('Pricing', divider = 'red')
        st.write("$^*$ Interest rate assuming continuous compounding")
        col1, col2 =st.columns(2)
        with col1:
            st.write("Stock Growth Factor",round(u,4))
            st.write("Stock Decay Factor",round(d,4))
        with col2:
            st.write("Risk Neutral Probability", round(p,4))
            st.write("Option Value:",round(f,4))
        st.write("")
        st.subheader('Binomial Tree Visualisation', divider = 'red')
        st.write("s denotes the underlying price with subscript denoting the number of up or down moves, f denotes options prices")
        st.write("")
        if T == 1:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"$s$: {round(s_t,4)}")
            with col2: 
                st.write(f"$s_u$: {round(s_u,4)}")
                st.write(f"$s_d$: {round(s_d,4)}")
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"$f$: {round(f,4)}")
            with col2: 
                st.write(f"$f_u$: {round(f_u,4)}")
                st.write(f"$f_d$: {round(f_d,4)}")
        elif T == 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"$s_0$: {round(s_t,4)}")
            with col2:
                st.write(f"$s_u$: {round(s_u,4)}")
                st.write(f"$s_d$: {round(s_d,4)}")
            with col3:
                st.write(f"$s_{{uu}}$: {round(s_uu,4)}")
                st.write(f"$s_{{ud}}$: {round(s_ud,4)}")
                st.write(f"$s_{{dd}}$: {round(s_dd,4)}")
            st.write("")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"$f$: {round(f,4)}")
            with col2:
                st.write(f"$f_u$: {round(f_u,4)}")
                st.write(f"$f_d$: {round(f_d,4)}")
            with col3:
                st.write(f"$f_{{uu}}$: {round(f_uu,4)}")
                st.write(f"$f_{{ud}}$: {round(f_ud,4)}")
                st.write(f"$f_{{dd}}$: {round(f_dd,4)}")

        st.subheader('Greeks', divider = 'red')
        greeks = OptionsGreeks(f,f_u,f_d,f_ud,f_uu,f_dd,s_u,s_d,s_uu,s_ud,s_dd,t)
        if T == 1:
            delta = greeks.ones_step_delta()
            df = pd.DataFrame(
                [
                    {"Greek": "Spot-Delta (Δ)", "Value": delta}
                ]
            )  
        elif T == 2:
            delta, delta_u, delta_d = greeks.two_step_delta()
            gamma = greeks.two_step_gamma()
            theta = greeks.two_step_theta()
            df = pd.DataFrame(
                [
                    {"Greek": "Spot-Delta (Δ)", "Value": delta},
                    {"Greek": "Up Delta (Δ_u)", "Value": delta_u},
                    {"Greek": "Down-Delta (Δ_d)", "Value": delta_d},
                    {"Greek": "Gamma (Γ)", "Value": gamma},
                    {"Greek": "Theta (θ)", "Value": theta},
                ]
            )
        st.markdown(
            f"""
            <style>
            .reportview-container .main .dataframe .col1 {{ width: 300px !important; }}
            .reportview-container .main .dataframe .col2 {{ width: 300px !important; }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df, use_container_width = True)
