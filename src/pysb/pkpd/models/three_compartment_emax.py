from pysb import Model
from ..macros import emax
from ..pk_models import threecomp

Model(base=threecomp)
# Add an Emax PD model for Drug in the 
# CENTRAL compartment
emax(Drug, CENTRAL, 1., 10.)