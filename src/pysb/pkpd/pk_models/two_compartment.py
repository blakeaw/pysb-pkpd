from pysb import Model, Compartment, Monomer, Parameter, Expression, Observable, Initial

from ..macros import two_compartments, dose_bolus, eliminate, clearance, distribute

Model()

Monomer("Drug")

# Defines the compartments for the model:
#  CENTRAL
#  PERIPHERAL
two_compartments()

# The dose should be in units of weight, mass or moles and
# is converted into an initial concentration by dividing the
# amount by the compartment volume. 
dose_bolus(Drug, CENTRAL, 100.)
# Distribute drug between CENTRAL and PERIPHERAL compartments.
distribute(Drug, CENTRAL, PERIPHERAL, [1.0, 1e-1])
# Linear elimination of drug from the CENTRAL compartment 
# by processes like metabolism and renal excretion.
#eliminate(Drug, CENTRAL, 1e-2)
# Linear elimination of the drug from the CENTRAL compartment
# by systemic clearance. Not the clearance rate is in units of volume/time.
clearance(Drug, CENTRAL, 10.)
