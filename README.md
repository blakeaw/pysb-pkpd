# pysb-pkpd

![Python version badge](https://img.shields.io/badge/python-3.11.3-blue.svg)
[![PySB version badge](https://img.shields.io/badge/PySB->%3D1.15.0-9cf.svg)](https://pysb.org/)
[![license](https://img.shields.io/github/license/blakeaw/pysb-pkpd.svg)](LICENSE)
![version](https://img.shields.io/badge/version-0.2.0-orange.svg)
[![release](https://img.shields.io/github/release-pre/blakeaw/pysb-pkpd.svg)](https://github.com/blakeaw/pysb-pkpd/releases/tag/v0.2.0)

`pysb-pkpd` is an add-on for the [PySB](https://pysb.org/) modeling framework that provides domain-specific macros and pre-constructed models for empirical and mechanistic PK/PD modeling. `pysb-pkpd` could also be used in conjuction with core PySB features to help build and execute quantitative systems pharmacology/toxicology (QSP/QST) models.

## Table of Contents

 1. [Install](#install)
     1. [Dependencies](#dependencies)
     2. [pip install](#pip-install)
     3. [Manual install](#manual-install)
 2. [License](#license)
 3. [Change Log](#change-log)
 4. [Documentation and Usage](#documentation-and-usage)
     1. [Quick Overview](#quick-overview)
     2. [Example](#example)
     3. [List of macros](#list-of-macros)
     4. [Preconstructed models](#preconstructed-models)
 5. [Contact](#contact)
 6. [Citing](#citing)  
 7. [Other Useful Tools](#other-useful-tools)

------

# Install

| **! Note** |
| :--- |
|  psyb-pkpd is still in version zero development so new versions may not be backwards compatible. |

**pysb-pkpd** installs as the `pysb.pkpd` Python (namespace) package. It is has been developed with Python 3.11.3 and PySB 1.15.0.

### Dependencies

Note that `pysb-pkpd` has the following core dependencies:
   * [PySB](https://pysb.org/) - developed using PySB version 1.15.0


### pip install

You can install `pysb-pkpd` version 0.2.0 with `pip` sourced from the GitHub repo:

##### with git installed:

Fresh install:
```
pip install git+https://github.com/blakeaw/pysb-pkpd@v0.2.0
```
Or to upgrade from an older version:
```
pip install --upgrade git+https://github.com/blakeaw/pysb-pkpd@v0.2.0
```
##### without git installed:

Fresh install:
```
pip install https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.2.0.zip
```
Or to upgrade from an older version:
```
pip install --upgrade https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.2.0.zip
```
### Manual install

First, download the repository. Then from the `pysb-pkpd` folder/directory run
```
pip install .
```

------

# License

This project is licensed under the BSD 2-Clause License - see the [LICENSE](LICENSE) file for details

------

# Change Log

See: [CHANGELOG](CHANGELOG.md)

------

# Documentation and Usage

## Quick Overview

The key feature of `pysb-pkpd` is a set of domain specific PySB macros for PK/PD modeling that can be used to programatically construct models in Python via the PySB framework: 

### Example

Building a two-compartment PK model with a sigmoidal Emax PD function:

```python
from pysb import Model
import pysb.pkpd as pkpd

# Initialize the PySB model:
Model()

# Add a Monomer for the drug:
pkpd.drug_monomer(name='Drug')

# Add the compartments for a two-compartment model:
pkpd.two_compartments(c1_name="CENTRAL",
                             c1_size=2.0,
                             c2_name="PERIPHERAL",
                             c2_size=1.0)


# Add a dose of the drug using an 
# instantaneous 'bolus' dose in the central
# compartment (initial amount of drug at time zero).
#   Note that dose is an amount such as weight, mass, or moles,
#     which will be converted automatically to an initial concentration
#     as: 
#         [Drug]_0 = dose / V_CENTRAL , 
#     where V_CENTRAL is the size (i.e., volume) of the central compartment.
pkpd.dose_bolus(Drug, CENTRAL, dose=100.)

# Add (1st order) distribution and re-distribution between the 
# central and peripheral compartments:
#    Note that klist is [k_distribute, k_redistribute]
pkpd.distribute(Drug, CENTRAL, PERIPHERAL, klist=[1.0, 1e-1])

# Include linear elimination of Drug from the central compartment 
# by processes like metabolism and renal excretion.
pkpd.eliminate(Drug, CENTRAL, kel=1e-2)

# Add the sigmoidal Emax PD function for Drug in the
# central compartment:
pkpd.sigmoidal_emax(Drug, CENTRAL, emax=1.,
                                   ec50=10.,
                                   n=1.7)
               
```

### PKRO Example

See [this notebook](example-notebooks/1_simple-PKRO.ipynb) for another example using PySB with the `psyb-pkpd` add-on to build a simple semi-mechanistic pharmacokinetic and receptor occupancy (PKRO) model. 

### List of macros

The `pysb.pkpd.macros` module currently defines the following macros encoding PK, PD, and dosing functions:

PK functions:

  * `drug_monomer` - adds a simple monomer species for the drug to the model. If the drug needs binding sites or other state variables then you should directly use the PySB `Monomer` class instead.
  * `one_compartment` - adds one compartment to the model for a one-comaprtment PK model. Alternatively, it could be used to add a new compartment to a multi-compartment model. 
  * `two_compartments` - adds two compartments to the model for a two-comaprtment PK model.
  * `three_compartments` - adds three compartments to the model for a three-compartment PK model.
  * `eliminate` - adds linear (1st-order) elimination of the specified drug/species from a compartment.
  * `eliminate_mm` - add non-linear, Michaelis-Menten, elimination of the specified drug/species from a compartment.
  * `clearance` - adds linear (1st-order) elimination of the specified drug/species from a compartment by systemic clearance.
  * `distribute` - adds distribution/redistribution of the specified drug/species between two compartments.
  * `transfer` - adds one-way transfer (distribution with no redistribution) of the specified drug/species from one compartment to another.

PD functions:

  * `emax` - Adds an Emax model expression for the specified drug/species in a given compartment. Generates a PySB Expression with name: 'Emax_expr_DrugName_CompartmentName'
  * `sigmoidal_emax` - Adds a sigmoidal Emax model expression for the specified drug/species in a given compartment. Generates a PySB Expression with name: 'Emax_expr_DrugName_CompartmentName'
  * `linear_effect` - Adds a linear effect model expression for the specified drug/specis in a given compartment. Generates a PySB Expression with name: 'LinearEffect_expr_DrugName_CompartmentName'

Dosing functions:

  * `dose_bolus` - adds an instantaneous bolus dose of the specified drug/species which defines the initial concentration at time zero; e.g., to model IV bolus.
  * `dose_infusion` - adds a continous (zero-order) infusion of the specified drug/species; e.g., to model continuous IV infusion. 
  * `dose_absorbed` - adds a dose of the specified drug which is absorbed into the specified compartment via first-order kinetics, including a bioavailibity factor; e.g., to model oral dosing or a subcutaneous depot. 

### Preconstructed models

Another feature of `pysb-pkpd` are a limited set of pre-constructed two-compartment and three-compartment models which can be used for empirical fitting of PK data or as base models for more complex semi-mechanistic PK/PD mdoels. 

#### PK/PD models

Two-compartment and three-compartment PK models with Emax PD function for the drug in the central compartment:
```python
from pysb.pkpd.models import twocomp_emax, threecomp_emax
```

#### PK-only models

Two-compartment and three-compartment PK models:
```python
from pysb.pkpd.pk_models import twocomp, threecomp
```


------

# Contact

Please open a [GitHub Issue](https://github.com/blakeaw/pysb-pkpd/issues) to
report any problems/bugs or make any comments, suggestions, or feature requests.

------

# Citing

If this package is useful in your work, please cite this GitHub repo: https://github.com/blakeaw/pysb-pkpd

-----

# Other Useful Tools

## Parameter estimation

Please see packages such as [simplePSO](https://github.com/LoLab-MSM/simplePSO), [PyDREAM](https://github.com/LoLab-MSM/PyDREAM), [Gleipnir](https://github.com/LoLab-MSM/Gleipnir), or [GAlibrate](https://github.com/blakeaw/GAlibrate) for tools to do PySB model parameter estimation using stochastic optimization or Bayesian Monte Carlo approaches.

## PD response models

If you want to separately fit response data independetly of PK data, then the [pharmacodynamic-response-models](https://github.com/NTBEL/pharmacodynamic-response-models) package may also be useful.  

## PySB model visualization

[pyvipr](https://github.com/LoLab-MSM/pyvipr) can be used for static and dynamic PySB model visualizations.

-----