"""
Apoptosis-Necrosis Reaction Network Model: 

"""
import pickle
import numpy as np
import pylab as p
import calibratortools as ct
import simulator_1_0 as sim

from irvin_anrm_model import model
from pysb.integrate  import odesolve

#-----------Calibrated Parameters-----------------------
position = pickle.load(open('irvin_anrm_model_calibrated_params.pkl'))

#-----------Simulator Settings--------------------------
sims = sim.Settings()
sims.model = model
sims.tspan = np.linspace(0,20000,1000)
sims.estimate_params = model.parameters_rules()
sims.rtol = 1e-3
sims.atol = 1e-6

solve = sim.Solver(sims)
solve.run()

ic_params  = model.parameters_initial_conditions()

#-----------Apoptotic Conditions--------------------------
apoptotic_conditions = ct.initial_conditions(['Bak_0', 'Bax_0', 'Bid_0', 'zVad_0', 'TNFa_0'], [0.2e5, 40165, 12044, 0, 1500], ic_params)
y_apop = solve.simulate(position, observables=True, initial_conc = apoptotic_conditions)
yout1 = ct.extract_records(y_apop, ['Obs_cPARP', 'Obs_MLKL', 'ComplexI', 'ComplexI_ub', 'TRADD_RIP1', 'RIP1_FADD', 'RIP1_Trunc', 'RIP1_po4'])

#-----------Necroptotic Conditions--------------------------
necroptotic_conditions = ct.initial_conditions(['Bak_0', 'Bax_0', 'Bid_0', 'zVad_0'], [0.2e5, 40165, 12044, 9.6e6], ic_params)
#20uM zVad == 9.6e6 zVad per cell for a cell volume of 8e-13L
y_necr = solve.simulate(position, observables=True, initial_conc = necroptotic_conditions)
yout2 = ct.extract_records(y_necr, ['Obs_cPARP', 'Obs_MLKL'])

"""p.figure('Apoptosis')
p.ion()
p.plot(sims.tspan, (yout1[:,2]+yout1[:,3])/np.max((yout1[:,2]+yout1[:,3])), label = 'RIP1 in Complex I')
p.plot(sims.tspan, yout1[:,4]/np.max(yout1[:,4]), label = 'Complex IIa (TRADD)')
p.plot(sims.tspan, yout1[:,5]/np.max(yout1[:,5]), label = 'Complex IIb (FADD)')
p.plot(sims.tspan, yout1[:,6]/np.max(yout1[:,6]), label = 'tRIP1')
p.plot(sims.tspan, yout1[:,7]/np.max(yout1[:,7]), label = 'po4-RIP1')
#p.plot(sims.tspan, yout1[:,1], label = 'MLKL')"""

p.figure('Apoptosis')
p.ion()
p.plot(sims.tspan, (yout1[:,2]+yout1[:,3]), label = 'RIP1 in Complex I')
p.plot(sims.tspan, yout1[:,4], label = 'Complex IIa (TRADD)')
p.plot(sims.tspan, yout1[:,5], label = 'Complex IIb (FADD)')
p.plot(sims.tspan, yout1[:,6], label = 'tRIP1')
p.plot(sims.tspan, yout1[:,7], label = 'po4-RIP1')
#p.plot(sims.tspan, yout1[:,1], label = 'MLKL')

p.xlabel('time [sec]')
p.ylabel('PARP and MLKL concentration [molecules per cell]')
p.legend()
p.show()

p.figure('Necroptosis')
p.plot(sims.tspan, yout2[:,0], label = 'Cleaved Parp')
p.plot(sims.tspan, yout2[:,1], label = 'MLKL')

p.xlabel('time [sec]')
p.ylabel('PARP and MLKL concentration [molecules per cell]')
p.legend()
p.show()