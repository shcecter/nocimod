import brian2 as br


# Plot IF curve functions
def compIFcurve(group, max_cur=240, N=100):  # arg N is redundant
    mon = br.SpikeMonitor(group)
    group.v = -70*br.mV
    group.I = f"i * {max_cur}*pA / N"  # noqa E741
    br.run(2000*br.ms)
    return mon


def plotIFcurve(mon, group):
    br.plot(group.I/br.pA, mon.count/2, "--o", lw=1, ms=4)
    br.xlabel("Входящий ток, пА")
    br.ylabel("Частота, Гц")
    br.grid(True)
