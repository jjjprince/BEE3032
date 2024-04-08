import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import math
import opstrat as op

tab1, tab2, tab3 = st.tabs(["Options Strategies","Risk Neutral Probabilities and Cox-Rubenstein", "Binomial Trees"])
with tab1:
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
                ('Call Spread','Put Spread','Butterfly','Reverse Butterfly','Box Spread'))
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
        breakeven = s_t + p
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
        breakeven_l = s_t - p
        breakeven_h = s_t + p
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
        breakeven_l = s_t - p
        breakeven_h = s_t + p
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

with tab2:
    title = "Futures and Options Calculations"
    st.title("Risk Neutral Probabilities and Cox-Rubenstein")
    st.subheader("Risk Neutral Probabilities", divider="red")

    col1, col2, col3 = st.columns(3)
    with col1:
        r = st.number_input("Interest rate (%)$^*$", min_value=0.0001, key="<riskneutral1>") / 100
        s_u = st.number_input("Future Stock Price ($S_u$)", min_value=0.0001, key="<riskneutral4>")
    with col2:
        time = st.number_input("Number of Months Per Step", min_value=1, key="<riskneutral2>")
        t = time
        s_d = st.number_input("Future Stock Price ($S_d$)", min_value=0.0001, key="<riskneutral5>")
    with col3:
        s_t = st.number_input("Spot Price", min_value=0.0001, key="<riskneutral3>")
        u = round(s_u / s_t,4)
        d = round(s_d / s_t,4)
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

with tab3:
    title = "Futures and Options Calculations"
    st.title("Binomial Trees")

    st.subheader("Options Binomial Trees" ,divider="red")
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
        p = None
        if u != d:
            p = (math.exp(r*t/12)-d)/(u-d)
    
    # Define Step Spot Prices
    s_u = s_t * u
    s_uu = s_t * u**2
    s_uuu = s_t * u**3
    s_uud = s_udu = us_duu = s_t * u**2 * d
    s_ud = s_du = s_t * u * d
    s_ddu = s_dud = s_udd = s_t *d**2 * u
    s_d= s_t * d
    s_dd = s_t * d**2
    s_ddd = s_t * d**3
    
    if u!=d:
        try:
            if T == 1 and type == "Call" and style == "European":
                f_u = max(s_u - K, 0)
                f_d = max(s_d - K, 0)
                f = math.exp(-r*(t/12))*((p*f_u)+((1-p)*f_d))
            if T == 1 and type == "Put" and style == "European":
                f_u = max(K - s_u, 0)
                f_d = max(K - s_d, 0)
                f = math.exp(-r*(t/12))*((p*f_u)+((1-p)*f_d))
            if T == 2 and type == "Call" and style == "European":
                f_uu = max(s_uu - K, 0)
                f_ud = f_du = max(s_ud - K,0)
                f_dd = max(s_dd - K, 0)
                f_u = math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud))
                f_d = math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd))
                f = math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d))
            if T == 2 and type == "Put" and style == "European":
                f_uu = max(K - s_uu, 0)
                f_ud = f_du = max(K-s_ud,0)
                f_dd = max(K - s_dd, 0)
                f_u = math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud))
                f_d = math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd))
                f = math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d))
            if T == 2 and type == "Call" and style == "American":
                f_uu = max(s_uu - K, 0)
                f_ud = f_du = max(s_ud - K,0)
                f_dd = max(s_dd - K, 0)
                f_u = max(math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud)),s_u - K)
                f_d = max(math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd)),s_d-K)
                f = max(math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d)),s_t-K)
            if T == 2 and type == "Put" and style == "American":
                f_uu = max(K - s_uu, 0)
                f_ud = f_du = max(K-s_ud,0)
                f_dd = max(K - s_dd, 0)
                f_u = max(math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud)),K - s_u)
                f_d = max(math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd)),K - s_d)
                f = max(math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d)),K - s_t)
        except ValueError as ve:
            # Handle ValueError
            st.error(f"ValueError: {ve}")
        except ZeroDivisionError as zd:
            # Handle ZeroDivisionError
            st.error(f"ZeroDivisionError: {zd}")
        except Exception as e:
            # Handle other exceptions
            st.error(f"An error occurred during calculation: {e}") 
            
    with col3:
        st.write("Stock Decay Factor Auto-Calculated as")
        st.write("$d = \\frac{1}{u}=$",round(d_auto,4))
        st.write("Insert decay factor in box to the lft according to question or this figure.")
    if p  is not None:
        col1, col2 =st.columns(2)
        st.write("$^*$ Interest rate assuming continuous compounding")
        st.write("Stock Growth Factor",round(u,4))
        st.write("Stock Decay Factor",round(d,4))
        st.write("Risk Neutral Probability", round(p,4))
        st.write("Option Value:",round(f,4))

    st.subheader("Tree Visualisation")
    st.write("IMPORTANT: s denotes the underlying price with subscript denoting the number of up or down movs, f denotes options prices")
    if st.button ("RUN"):
        try:
            if T == 1 and type == "Call" and style == "European":
                f_u = max(s_u - K, 0)
                f_d = max(s_d - K, 0)
                f = math.exp(-r*(t/12))*((p*f_u)+((1-p)*f_d))
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"$s$: {round(s_t,4)}")
                with col2: 
                    st.write(f"$s_u$: {round(s_u,4)}")
                    st.write(f"$s_d$: {round(s_d,4)}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"$f$: {round(f,4)}")
                with col2: 
                    st.write(f"$f_u$: {round(f_u,4)}")
                    st.write(f"$f_d$: {round(f_d,4)}")

            if T == 1 and type == "Put" and style == "European":
                f_u = max(K - s_u, 0)
                f_d = max(K - s_d, 0)
                f = math.exp(-r*(t/12))*((p*f_u)+((1-p)*f_d))
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"$s$: {round(s_t,4)}")
                with col2: 
                    st.write(f"$s_u$: {round(s_u,4)}")
                    st.write(f"$s_d$: {round(s_d,4)}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"$f$: {round(f,4)}")
                with col2: 
                    st.write(f"$f_u$: {round(f_u,4)}")
                    st.write(f"$f_d$: {round(f_d,4)}")

            if T == 2 and type == "Call" and style == "European":
                f_uu = max(s_uu - K, 0)
                f_ud = f_du = max(s_ud - K,0)
                f_dd = max(s_dd - K, 0)
                f_u = math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud))
                f_d = math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd))
                f = math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d))
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

            if T == 2 and type == "Put" and style == "European":
                f_uu = max(K - s_uu, 0)
                f_ud = f_du = max(K-s_ud,0)
                f_dd = max(K - s_dd, 0)
                f_u = math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud))
                f_d = math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd))
                f = math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d))
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

            if T == 2 and type == "Call" and style == "American":
                f_uu = max(s_uu - K, 0)
                f_ud = f_du = max(s_ud - K,0)
                f_dd = max(s_dd - K, 0)
                f_u = max(math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud)),s_u - K)
                f_d = max(math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd)),s_d-K)
                f = max(math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d)),s_t-K)
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

            if T == 2 and type == "Put" and style == "American":
                f_uu = max(K - s_uu, 0)
                f_ud = f_du = max(K-s_ud,0)
                f_dd = max(K - s_dd, 0)
                f_u = max(math.exp(-r*(t/12))*((p*f_uu)+((1-p)*f_ud)),K - s_u)
                f_d = max(math.exp(-r*(t/12))*((p*f_ud)+((1-p)*f_dd)),K - s_d)
                f = max(math.exp(-r*(time/12))*((p*f_u)+((1-p)*f_d)),K - s_t)
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
        except ValueError as ve:
            # Handle ValueError
            st.error(f"ValueError: {ve}")
        except ZeroDivisionError as zd:
            # Handle ZeroDivisionError
            st.error(f"ZeroDivisionError: {zd}")
        except Exception as e:
            # Handle other exceptions
            st.error(f"An error occurred during calculation: {e}")
