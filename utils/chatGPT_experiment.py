from brian2 import *

"""
Doesn't work due to equation has inconsistent units.
"""
start_scope()
# Define model parameters
Cm = 1*uF/cm**2
g_L = 0.1*msiemens/cm**2
V_L = -70*mV
V_rest = -70*mV
V_Cl = -65*mV
g_Cl = 30*nS

# Define the neuron model
eqs = '''
dv/dt = (-g_L*(v - V_L) - g_Cl*(v - V_Cl))/Cm : volt
'''

# Set up the simulation
duration = 100*ms
voltage = -60*mV
stim_start = 10*ms
stim_end = 90*ms

# Create the neuron
neuron = NeuronGroup(1, eqs, threshold='v>-50*mV', reset='v=V_rest')

# Set the initial voltage
neuron.v = V_rest

# Define the patch clamp experiment
stimulus = TimedArray([voltage if stim_start <= t <= stim_end else V_rest for t in np.arange(0, duration, defaultclock.dt)], dt=defaultclock.dt)

# Run the simulation
trace = StateMonitor(neuron, 'v', record=True)
run(duration)

# Plot the results
plt.plot(trace.t/ms, trace.v[0]/mV)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
