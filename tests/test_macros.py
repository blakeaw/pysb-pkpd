from pysb.testing import *
from pysb.core import *
import numpy as np

from pysb.pkpd.macros import *

__all__ = [
    "drug_monomer",
    "one_compartment",
    "two_compartments",
    "three_compartments",
    "eliminate",
    "eliminate_mm",
    "clearance",
    "distribute",
    "transfer",
    "emax",
    "sigmoidal_emax",
    "linear_effect",
    "loglinear_effect",
    "fixed_effect",
    "dose_bolus",
    "dose_infusion",
    "dose_absorbed",
]

@with_model
def test_drug_monomer():
    drug_monomer()
    assert len(model.monomers) == 1
    assert model.monomers[0].name == 'Drug'
    drug_monomer("D2")
    assert len(model.monomers) == 2
    assert model.monomers[-1].name == 'D2'

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

if __name__ == "__main__":
    test_drug_monomer()
    test_one_compartment()
    test_two_compartments()