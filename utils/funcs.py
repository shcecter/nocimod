import brian2 as br


# Plot IF curve functions
def compIFcurve(group, max_cur=240, N=100):  # arg N is redundant
    mon = br.SpikeMonitor(group)
    group.v = -70 * br.mV
    group.I = f"i * {max_cur}*pA / N"  # noqa E741
    br.run(2000 * br.ms)
    return mon


def plotIFcurve(mon, group):
    br.plot(group.I / br.pA, mon.count / 2, "--o", lw=1, ms=4)
    br.xlabel("Входящий ток, пА")
    br.ylabel("Частота, Гц")
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


def max_conductances(voltages, neuron_group, neuron_group_statemon, network, restore_name):
    """
    Returns a list of max conductance values for given neuron group and list of voltages

    :param voltages: list of voltages to iterate over
    :param neuron_group: NeuronGroup to set voltage for each iteration
    :param neuron_group_statemon: StateMonitor to record current values
    :return: list of max conductance values
    """
    max_g = []
    for v in voltages:
        network.restore(restore_name)
        neuron_group.v = v
        network.run(200 * br.ms)
        max_g.append(abs(neuron_group_statemon.INa18[0]).max() / v)
    return max_g


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
