from pysb.testing import *
from pysb.core import *
import numpy as np

from pysb.pkpd.macros import *


@with_model
def test_drug_monomer():
    drug_monomer()
    assert len(model.monomers) == 1
    assert model.monomers[0].name == "Drug"
    drug_monomer("D2")
    assert len(model.monomers) == 2
    assert model.monomers[-1].name == "D2"


@with_model
def test_one_compartment():
    one_compartment()
    assert len(model.compartments) == 1
    assert model.compartments[0].name == "CENTRAL"
    assert np.isclose(model.compartments[0].size.value, 1.0)
    assert len(model.parameters) == 1
    one_compartment("C2", 2.0)
    assert len(model.compartments) == 2
    assert model.compartments[-1].name == "C2"
    assert np.isclose(model.compartments[-1].size.value, 2.0)
    assert len(model.parameters) == 2


@with_model
def test_two_compartments():
    two_compartments()
    assert len(model.compartments) == 2
    assert model.compartments[0].name == "CENTRAL"
    assert model.compartments[1].name == "PERIPHERAL"
    assert np.isclose(model.compartments[0].size.value, 1.0)
    assert np.isclose(model.compartments[1].size.value, 1.0)
    assert len(model.parameters) == 2
    two_compartments("C2", 2.0, "P2", 0.1)
    assert len(model.compartments) == 4
    assert model.compartments[2].name == "C2"
    assert model.compartments[3].name == "P2"
    assert np.isclose(model.compartments[2].size.value, 2.0)
    assert np.isclose(model.compartments[3].size.value, 0.1)
    assert len(model.parameters) == 4


@with_model
def test_three_compartments():
    three_compartments()
    assert len(model.compartments) == 3
    assert model.compartments[0].name == "CENTRAL"
    assert model.compartments[1].name == "PERIPHERAL"
    assert model.compartments[2].name == "DEEPPERIPHERAL"
    assert np.isclose(model.compartments[0].size.value, 1.0)
    assert np.isclose(model.compartments[1].size.value, 1.0)
    assert np.isclose(model.compartments[2].size.value, 1.0)
    assert len(model.parameters) == 3
    three_compartments("C2", 2.0, "P2", 0.1, "DP2", 0.4)
    assert len(model.compartments) == 6
    assert model.compartments[3].name == "C2"
    assert model.compartments[4].name == "P2"
    assert model.compartments[5].name == "DP2"
    assert np.isclose(model.compartments[3].size.value, 2.0)
    assert np.isclose(model.compartments[4].size.value, 0.1)
    assert np.isclose(model.compartments[5].size.value, 0.4)
    assert len(model.parameters) == 6


def base_components():
    one_compartment()
    drug_monomer()
    return


# ---- PK Macros ----


@with_model
def test_eliminate():
    base_components()
    eliminate(Drug, CENTRAL, kel=0.1)
    assert len(model.parameters) == 2
    assert len(model.rules) == 1


@with_model
def test_eliminate_mm():
    base_components()
    eliminate_mm(Drug, CENTRAL, vmax=0.1, km=100.0)
    assert len(model.parameters) == 3
    assert len(model.rules) == 1
    assert len(model.expressions) == 1


@with_model
def test_clearance():
    base_components()
    clearance(Drug, CENTRAL, cl=10.0)
    assert len(model.parameters) == 2
    assert len(model.rules) == 1
    assert len(model.expressions) == 1


@with_model
def test_distribute():
    base_components()
    one_compartment("PERIPHERAL")
    distribute(Drug, CENTRAL, PERIPHERAL, klist=[0.1, 0.05])
    assert len(model.parameters) == 4
    assert len(model.rules) == 1
    assert len(model.expressions) == 0


@with_model
def test_transfer():
    base_components()
    one_compartment("PERIPHERAL")
    transfer(Drug, CENTRAL, PERIPHERAL, k=0.01)
    assert len(model.parameters) == 3
    assert len(model.rules) == 1
    assert len(model.expressions) == 0


# ---- PD Macros ----


@with_model
def test_emax():
    base_components()
    emax(Drug, CENTRAL, emax=10.0, ec50=100.0)
    assert len(model.parameters) == 3
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.observables) == 1


@with_model
def test_sigmoidal_emax():
    base_components()
    sigmoidal_emax(Drug, CENTRAL, emax=10.0, ec50=100.0, n=2.0)
    assert len(model.parameters) == 4
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.observables) == 1


@with_model
def test_linear_effect():
    base_components()
    linear_effect(Drug, CENTRAL, slope=0.1, intercept=1.0)
    assert len(model.parameters) == 3
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.observables) == 1


@with_model
def test_loglinear_effect():
    base_components()
    loglinear_effect(Drug, CENTRAL, slope=0.1, intercept=1.0, base=2)
    assert len(model.parameters) == 3
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.observables) == 1


@with_model
def test_fixed_effect():
    base_components()
    fixed_effect(Drug, CENTRAL, e_fixed=1.0, c_threshold=24.6)
    assert len(model.parameters) == 3
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.observables) == 1


# ---- Dose Macros ----


@with_model
def test_dose_bolus():
    base_components()
    dose_bolus(Drug, CENTRAL, dose=100.0)
    assert len(model.parameters) == 2
    assert len(model.rules) == 0
    assert len(model.expressions) == 1
    assert len(model.initials) == 1


@with_model
def test_dose_infusion():
    base_components()
    dose_infusion(Drug, CENTRAL, dose=2.0)
    assert len(model.parameters) == 2
    assert len(model.rules) == 1
    assert len(model.expressions) == 1
    assert len(model.initials) == 0


@with_model
def test_dose_absorbed():
    base_components()
    dose_absorbed(Drug, CENTRAL, dose=10.0, ka=1e-1, f=0.78)
    assert len(model.parameters) == 4
    assert len(model.rules) == 1
    assert len(model.expressions) == 2
    assert len(model.initials) == 1
    assert len(model.monomers) == 2


if __name__ == "__main__":
    test_drug_monomer()
    test_one_compartment()
    test_two_compartments()
    test_three_compartments()
    test_eliminate()
    test_eliminate_mm()
    test_clearance()
    test_distribute()
    test_transfer()
    test_emax()
    test_sigmoidal_emax()
    test_linear_effect()
    test_loglinear_effect()
    test_fixed_effect()
    test_dose_bolus()
    test_dose_infusion()
    test_dose_absorbed()
