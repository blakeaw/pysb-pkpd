# pysb-pkpd

PySB plugin package providing domain-specific macros and models for pharmacological PK/PD modeling.

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
 5. [Contact](#contact)
 6. [Citing](#citing)  

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

You can install `pysb-pkpd` version 0.1.0 with `pip` sourced from the GitHub repo:

##### with git installed:

Fresh install:
```
pip install git+https://github.com/blakeaw/pysb-pkpd@v0.1.0
```
Or to upgrade from an older version:
```
pip install --upgrade git+https://github.com/blakeaw/pysb-pkpd@v0.1.0
```
##### without git installed:

Fresh install:
```
pip install https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.1.0.zip
```
Or to upgrade from an older version:
```
pip install --upgrade https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.1.0.zip
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

### Quick Overview

`pysb-pkpd` defines a set of domain specific macros for PK/PD modeling using the PySB framework, as well as some pre-constructed versions of two and three-compartment PK and PK/PD models. As with PySB, `pysb-pkpd` is meant to be used to programatically construct models in Python. 

### Example

Building a two-compartment PK model with a sigmoidal Emax PD function:

```python
from pysb import Model, Monomer
import pysb.pkpd as pkpd

# Initialize the PySB model:
Model()

# Add a Monomer for the drug:
Monomer("Drug")

# Add the compartments for a two-compartment model:
pkpd.macros.two_compartments(c1_name="CENTRAL",
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
pkpd.macros.dose_bolus(Drug, CENTRAL, dose=100.)

# Add (1st order) distribution and re-distribution between the 
# central and peripheral compartments:
#    Note that klist is [k_distribute, k_redistribute]
pkpd.macros.distribute(Drug, CENTRAL, PERIPHERAL, klist=[1.0, 1e-1])

# Include linear elimination of Drug from the central compartment 
# by processes like metabolism and renal excretion.
pkpd.macros.eliminate(Drug, CENTRAL, kel=1e-2)

# Add the sigmoidal Emax PD function for Drug in the
# central compartment:
pkpd.macros.sigmoidal_emax(Drug, CENTRAL, emax=1.,
                                          ec50=10.,
                                          n=1.7)
               
```

### List of macros

The `pysb.pkpd.macros` module currently defines the following macros encoding PK, PD, and dosing functions:

PK functions:

  * `two_compartments` - adds two compartments to the model for a two-comaprtment PK model.
  * `three_compartments` - adds three compartments to the model for a three-compartment PK model.
  * `eliminate` - adds linear (1st-order) elimination of the specified drug/species from a compartment.
  * `eliminate_mm` - add non-linear, Michaelis-Menten, elimination of the specified drug/species from a compartment.
  * `clearance` - adds linear (1st-order) elimination of the specified drug/species from a compartment by systemic clearance.
  * `distribute` - adds distribution/redistribution of the specified drug/species between two compartments.
  * `transfer` - adds one-way transfer (distribution with no redistribution) of the specified drug/species from one compartment to another.

PD functions:

  * `emax` - Adds an Emax model expression for the specified drug/species in a given compartment.
  * `sigmoidal_emax` - Adds a sigmoidal Emax model expression for the specified drug/species in a given compartment.

Dosing functions:

  * `dose_bolus` - adds an instantaneous bolus dose of the specified drug/species, defining the initial concentration at time zero.
  * `dose_infusion` - adds a continous (zero-order) infusion of the specified drug/species. 

### Pre-constructed models

In addition to the macros module, `pysb-pkpd` includes some pre-constructed two-compartment and three-compartment models. 

#### PK/PD models

Two-compartment and three-compartment PK models with Emax PD function for the drug in the central compartment:
```python
from pysb.pkpd.pk_models import twocomp, threecomp
```

#### PK-only models

Two-compartment and three-compartment PK models:
```python
from pysb.pkpd.models import twocomp_emax, threecomp_emax
```


------

# Contact

Please open a [GitHub Issue](https://github.com/blakeaw/pysb-pkpd/issues) to
report any problems/bugs or make any comments, suggestions, or feature requests.

------

# Citing

If this package is useful in your work, please cite this GitHub repo: https://github.com/blakeaw/pysb-pkpd