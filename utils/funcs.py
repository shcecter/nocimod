import brian2 as br

from .equations import threshold_str, refractory_str


basic_namespace = {
    "Cm": 20 * br.pF,
    "Ena": 55 * br.mV,
    "Ek": -85 * br.mV,
    "El": -70 * br.mV,
    "gK": 40 * br.nS,
    "gL": 3 * br.nS,  # needed for IF_curve
    "gNa": 50 * br.nS,
    "gNa18": 100 * br.nS,
    "VT": -63 * br.mV,
}


# Plot IF curve functions
def compIFcurve(group, max_cur=240, N=100):
    mon = br.SpikeMonitor(group)
    group.v = -70 * br.mV
    group.I = f"i * {max_cur}*pA / N"  # noqa E741
    br.run(2000 * br.ms)
    return mon


def compIFcurve_by_equation(equation, name_space, max_cur=240, N=100):
    br.start_scope()
    neurons = br.NeuronGroup(N, equation, threshold=threshold_str, refractory=refractory_str,
                             method="exponential_euler", namespace=name_space)
    return compIFcurve(neurons, max_cur, N), neurons


def plotIFcurve(mon, group, ms=4):
    br.plot(group.I / br.pA, mon.count / 2, "--o", lw=1, ms=ms)
    br.xlabel("Входящий ток, пА")
    br.ylabel("Частота, Гц")
    br.grid(True)


def comp_statemon_by_equation(equation, name_space, I=100 * br.pA):
    br.start_scope()
    neurons = br.NeuronGroup(1, equation, method="exponential_euler", namespace=name_space)
    neurons.v = name_space["El"]
    stmon = br.StateMonitor(neurons, "v", record=True)
    br.run(10 * br.ms)
    neurons.I = I
    br.run(100 * br.ms)
    neurons.I = 0 * br.pA
    br.run(10 * br.ms)
    return stmon, neurons


def plot_v_by_equation(equation, name_space, I=100 * br.pA):
    stmon, _ = comp_statemon_by_equation(equation, name_space, I)
    br.plot(stmon.t / br.ms, stmon.v[0] / br.mV)
    br.xlabel("Время, мс")
    br.ylabel("мВ")
    br.grid(True)


# Z_eff functions
def max_currents(voltages, neuron_group, neuron_group_statemon):
    """
    Returns a list of max current values for given neuron group and list of voltages

    :param voltages: list of voltages to iterate over
    :param neuron_group: NeuronGroup to set voltage for each iteration
    :param neuron_group_statemon: StateMonitor to record current values
    :return: list of max current values
    """
    max_current_values = []
    for v in voltages:
        br.restore("patch_clamp_init")
        neuron_group.v = v
        br.run(200 * br.ms)
        max_current_values.append(abs(neuron_group_statemon.INa18[0] / br.pA).max())
    return max_current_values


def plot_max_g(voltages, neuron_group, neuron_group_statemon):
    """
    Plots the max conductance values for given neuron group and list of voltages

    :param voltages: list of voltages to iterate over
    :param neuron_group: NeuronGroup to set voltage for each iteration
    :param neuron_group_statemon: StateMonitor to record current values
    """
    for v in voltages:
        br.restore("patch_clamp_init")
        neuron_group.v = v
        br.run(200 * br.ms)
        br.plot(neuron_group_statemon.t / br.ms, neuron_group_statemon.INa18[0] / br.pA)
        br.grid()
        br.xlabel("Time (ms)")
        br.ylabel("Current (pA)")


def ln_G(max_gs, gNa_max):
    """
    Returns a list of log(max_g/(g_18nav - max_g)). Where max_g is the element of max_gs

    :param max_g: list of max conductance values
    :param g_18nav: maximum conductance value for Nav1.8
    :return: list of ln(max_g/(g_18nav - max_g))
    """
    max_gs = abs(br.array(max_gs / br.nS)) * br.nS
    return br.log(max_gs / (gNa_max - max_gs))


def plot_ln_G_vs_voltages(max_g, voltages, g_max, xlim=(-60, 15), ylim=(-15, 5)):
    """
    Plots ln(max_g/(g_18nav - max_g)) vs voltages for given max_g values and list of voltages

    :param max_g: list of max conductance values
    :param voltages: list of voltages
    :param g_18nav: maximum conductance value for Nav1.8
    """
    ln_G_vals = ln_G(max_g, g_max)
    br.plot(voltages / br.mV, ln_G_vals)
    br.xlabel("Voltage (mV)")
    br.ylabel("$ln\\frac{G_{Na}}{G^{max}_{Na}-G_{Na}}$")
    br.grid(True)
    br.xlim(*xlim)
    br.ylim(*ylim)


def comp_Zeff(max_gs, experimental_voltages, gna_max):
    k_boltzmann = 1.38
    T = 300
    eps_0 = 8.854
    e = 1.602
    lnG = ln_G(max_gs[:2], gna_max)
    d_lnG = lnG[1] - lnG[0]
    d_volt = experimental_voltages[1] - experimental_voltages[0]
    return (d_lnG / d_volt * br.mV) * k_boltzmann * T / eps_0 / e
