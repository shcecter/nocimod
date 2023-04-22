from brian2 import Equations


basic_I = Equations("""
INa = gNa*m**3*h*(Ena-v) : amp
IK = gK*n**4*(Ek-v) : amp
I : amp
""")

base_master_eq = Equations("""
dv/dt = (gL * (El - v) + IK + INa + I) / Cm : volt""")
dmdt = Equations(
    """
dm/dt = a_m * (1 - m) - b_m * m : 1
a_m = 0.32*4*0.8 / exprel((13*mV - v + VT + 3*mV)/4/mV) / ms : Hz
b_m = 0.28 * 5 / exprel((v - VT - 40*mV + 3*mV)/5/mV) / ms : Hz
"""
)
dhdt = Equations(
    """
dh/dt = a_h * (1 - h) - b_h * h : 1
a_h = 0.128*0.2*exp((17*mV - v + VT + 15*mV)/18/mV) / ms : Hz
b_h = 4*0.2 / (1 + exp((40*mV - v + VT + 15*mV)/5/mV)) / ms : Hz
"""
)
dndt = Equations(
    """
dn/dt = a_n * (1 - n) - b_n * n : 1
a_n = 0.032/mV * 5*mV / exprel((15*mV - v + VT)/5/mV) / ms : Hz
b_n = 0.5 * exp((10*mV - v + VT)/40/mV) / ms : Hz
    """
)

Lnav_master_eq = Equations("""
dv/dt = (gL*(El-v) + INa + IK + INa18 + I) / Cm : volt
""")
gNa18_eq = Equations(
    """
INa18 = gNa18 * m**3 * h * (Ena - v) : ampere

alpha_m = 2.85/ms - 2.84 / (1 + exp((v/mV - 1.16)/13.95)) / ms : Hz
beta_m = 7.62 / (1 + exp((v/mV + 46.5)/8.83)) / ms : Hz
m_inf = alpha_m / (alpha_m + beta_m) : 1
tau_m = 1 / (alpha_m + beta_m) : second
dm/dt = (m_inf - m) / tau_m : 1

tau_h = 1.218*ms + 42. * exp(-((v/mV + 38.1)**2) / (2*15.2**2))*ms : second
h_inf = 1 / (1 + exp((v/mV + 32.2)/4)) : 1
dh/dt = (h_inf - h) / tau_h : 1
""",
    m="mNa18",
    h="hNa18",
    alpha_m="amNa18",
    beta_m="bmNa18",
    tau_m="tau_mNa18",
    m_inf="mNa18_inf",
    tau_h="tau_hNa18",
    h_inf="hNa18_inf",
)

base_eq = base_master_eq + basic_I + dndt + dmdt + dhdt
Lnav_eq = Lnav_master_eq + basic_I + dndt + dmdt + dhdt + gNa18_eq

gNa18_eq_new = Equations(
    """
INa18 = gNa18 * m * h * (Ena - v) : ampere

alpha_m = 2.85*1./ms - 2.85*1. / (1 + exp((v/mV - 1.16 + 12)/13.95/0.4)) / ms : Hz  # lowering activ time
beta_m = 7.62*1. / (1 + exp((v/mV + 46.5 + 15)/8.83)) / ms : Hz
m_inf = alpha_m / (alpha_m + beta_m) : 1
tau_m = 1 / (alpha_m + beta_m): second
dm/dt = (m_inf - m) / tau_m : 1

tau_h = 1.218*ms + 42. * 0.6 * exp(-((v/mV + 38.1 + 45)**2) / (2*15.2**2))*ms : second
h_inf = 1*1. / (1 + exp((v/mV + 32.2 + 5.)/4/0.8)) + 0.: 1
dh/dt = (h_inf - h) / tau_h : 1
""",
    m="mNa18",
    h="hNa18",
    alpha_m="amNa18",
    beta_m="bmNa18",
    tau_m="tau_mNa18",
    m_inf="mNa18_inf",
    tau_h="tau_hNa18",
    h_inf="hNa18_inf",
)

Lnav_eq_new = Lnav_master_eq + basic_I + dndt + dmdt + dhdt + gNa18_eq_new
