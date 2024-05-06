import math
from datetime import datetime

class NoArbitragePricing:
    def __init__(self,s_0,r,T,u,y,q,r_f,I):
        self.s_0 = s_0
        self.r  = r
        self.T = T
        self.u = u
        self.y = y
        self.q = q
        self.r_f = r_f
        self.I = I

    def simple_price(self):
        price = self.s_0 * math.exp(self.r*self.T)
        return price

    def commodity_futures_price(self):
        price = self.s_0 * math.exp((self.r+self.u-self.y)*self.T)
        return price
    
    def stock_index_price(self):
        price = self.s_0 * math.exp((self.r-self.q)*self.T)
        return price
    
    def exchange_rate_price(self):
        price = self.s_0 * math.exp((self.r-self.r_f)*self.T)
        return price
    
    def KI_price(self):
        price = (self.s_0-self.I) * math.exp(self.r*self.T)
        return price

class FuturesAndForwardsValuation:
    def __init__(self,f_0,K,r,T):
        self.f_0 = f_0
        self.K = K
        self.r = r
        self.T = T
    def LongValue (self):
        value = (self.f_0 - self.K)*math.exp(-self.r*self.T)
        return value
    
    def ShortValue (self):
        value = (self.K - self.f_0)*math.exp(-self.r*self.T)
        return value

class OneStepBinomialTreePricingModel:
    def __init__(self,s_u,s_d,K,t,p,r):
        self.s_u = s_u
        self.p = p
        self.s_d = s_d
        self.K = K
        self.t = t
        self.r = r
        self.f_u = 1
        self.f_d = 1
        self.f = 1

    def one_step_call(self):
        self.f_u = max(self.s_u - self.K, 0)
        self.f_d = max(self.s_d - self.K, 0)
        self.f = math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d))
        return self.f_u, self.f_d, self.f

    def one_step_put(self):
        self.f_u = max(self.K - self.s_u, 0)
        self.f_d = max(self.K - self.s_d, 0)
        self.f = math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d))
        return self.f_u, self.f_d, self.f
 
class TwoStepBinomialTreePricingModel:
    def __init__(self,s_u,s_uu,s_ud,s_d,s_dd,K,t,p,r):
        self.s_u = s_u
        self.p = p
        self.s_uu = s_uu
        self.s_ud = s_ud
        self.s_d = s_d
        self.s_dd = s_dd
        self.K = K
        self.t = t
        self.r = r
        self.f_uu = 1
        self.f_uu = 1
        self.f_u = 1
        self.f_d = 1
        self.f = 1

    def two_step_call_EU(self):
        self.f_uu = max(self.s_uu - self.K, 0)
        self.f_ud = max(self.s_ud - self.K,0)
        self.f_dd = max(self.s_dd - self.K, 0)
        self.f_u = math.exp(-self.r*(self.t/12))*((self.p*self.f_uu)+(1-self.p)*self.f_ud)
        self.f_d = math.exp(-self.r*(self.t/12))*((self.p*self.f_ud)+((1-self.p)*self.f_dd))
        self.f = math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d))
        return self.f_uu, self.f_ud, self.f_dd, self.f_u, self.f_d, self.f

    def two_step_put_EU(self):
        self.f_uu = max(self.K - self.s_uu, 0)
        self.f_ud = f_du = max(self.K-self.s_ud,0)
        self.f_dd = max(self.K - self.s_dd, 0)
        self.f_u = math.exp(-self.r*(self.t/12))*((self.p*self.f_uu)+((1-self.p)*self.f_ud))
        self.f_d = math.exp(-self.r*(self.t/12))*((self.p*self.f_ud)+((1-self.p)*self.f_dd))
        self.f = math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d))
        return self.f_uu, self.f_ud, self.f_dd, self.f_u, self.f_d, self.f
    
    def two_step_call_US(self):
        self.f_uu = max(self.s_uu - self.K, 0)
        self.f_ud = f_du = max(self.s_ud - self.K,0)
        self.f_dd = max(self.s_dd - self.K, 0)
        self.f_u = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_uu)+((1-self.p)*self.f_ud)),self.s_u - self.K)
        self.f_d = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_ud)+((1-self.p)*self.f_dd)),self.s_d-self.K)
        self.f = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d)),self.s_t-self.K)
        return self.f_uu, self.f_ud, self.f_dd, self.f_u, self.f_d, self.f
        
    def two_step_put_US(self):
        self.f_uu = max(self.K - self.s_uu, 0)
        self.f_ud = f_du = max(self.K-self.s_ud,0)
        self.f_dd = max(self.K - self.s_dd, 0)
        self.f_u = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_uu)+((1-self.p)*self.f_ud)),self.K - self.s_u)
        self.f_d = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_ud)+((1-self.p)*self.f_dd)),self.K - self.s_d)
        self.f = max(math.exp(-self.r*(self.t/12))*((self.p*self.f_u)+((1-self.p)*self.f_d)),self.K - self.s_t)
        return self.f_uu, self.f_ud, self.f_dd, self.f_u, self.f_d, self.f
    
class OptionsGreeks:
    def __init__(self,f,f_u,f_d,f_ud,f_uu,f_dd,s_u,s_d,s_uu,s_ud,s_dd,t):
        self.f = f
        self.f_u = f_u
        self.f_d = f_d
        self.f_ud = f_ud
        self.f_uu = f_uu
        self.f_dd = f_dd
        self.s_u = s_u
        self.s_d = s_d
        self.s_uu = s_uu
        self.s_ud = s_ud
        self.s_dd = s_dd
        self.t = t

    def one_step_delta(self):
        self.delta = (self.f_u-self.f_d)/(self.s_u-self.s_d)
        return self.delta
    
    def two_step_delta(self):
        self.delta = (self.f_u-self.f_d)/(self.s_u-self.s_d)
        self.delta_u = (self.f_uu-self.f_ud)/(self.s_uu-self.s_ud)
        self.delta_d = (self.f_ud-self.f_dd)/(self.s_ud-self.s_dd)
        return self.delta, self.delta_u, self.delta_d
    
    def two_step_gamma(self):
        self.delta_u = (self.f_uu-self.f_ud)/(self.s_uu-self.s_ud)
        self.delta_d = (self.f_ud-self.f_dd)/(self.s_ud-self.s_dd)
        self.gamma = (self.delta_u-self.delta_d)/((self.s_uu-self.s_dd)/2)
        return self.gamma

    def two_step_theta(self):
        self.theta = (self.f_ud-self.f)/(2*self.t)
        return self.theta
