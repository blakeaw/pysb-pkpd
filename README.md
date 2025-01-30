# pysb-pkpd

![Python version badge](https://img.shields.io/badge/python-3.11.3-blue.svg)
[![PySB version badge](https://img.shields.io/badge/PySB->%3D1.15.0-9cf.svg)](https://pysb.org/)
[![license](https://img.shields.io/github/license/blakeaw/pysb-pkpd.svg)](LICENSE)
![version](https://img.shields.io/badge/version-0.3.3-orange.svg)
[![release](https://img.shields.io/github/release-pre/blakeaw/pysb-pkpd.svg)](https://github.com/blakeaw/pysb-pkpd/releases/tag/v0.3.3)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12775536.svg)](https://doi.org/10.5281/zenodo.12775536)

__`pysb-pkpd` enables you to efficiently program and simulate dynamic PK/PD and QSP models in Python using the PySB modeling framework.__ 

  :pill: :computer:

## What's new in

**version 0.3.0**

 * Macro encoding a Fixed-effect PD model: `fixed_effect`
 * Macro encoding a Log-linear Effect PD model: `loglinear_effect`
 * `simulate` function to simplify the process of simulating models.
 * The macro encoding the Linear-effect PD model, `linear_effect`, has an optional `intercept` argument to allow users to set the y-intercept of the linear model.

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
     4. [Simulating models](#simulating-models)
     5. [Preconstructed models](#preconstructed-models)
 5. [Contact](#contact)
 6. [Contributing](#contributing)
 7. [Supporting](#supporting)  
 8. [Other Useful Tools](#other-useful-tools)

------

# Install

| **! Note** |
| :--- |
|  psyb-pkpd is still in version zero development so new versions may not be backwards compatible. |

**pysb-pkpd** installs as the `pysb.pkpd` Python (namespace) package. It is has been developed with Python 3.11.3 and PySB 1.15.0.

### Dependencies

Note that `pysb-pkpd` has the following core dependencies:
   * [PySB](https://pysb.org/) - developed using PySB version 1.15.0, and recommended to install using conda/mamba.
```
conda install -c alubbock pysb
```

For automated testing and coverage analysis:
   * [pytest](https://docs.pytest.org/en/stable/getting-started.html)
   * [Coverage.py](https://coverage.readthedocs.io/en/7.6.10/install.html)
   * [nose](https://nose.readthedocs.io/en/latest/)
```
pip install pytest coverage nose
```

### pip install

You can install `pysb-pkpd` version 0.3.3 with `pip` sourced from the GitHub repo:

##### with git installed:

Fresh install:
```
pip install git+https://github.com/blakeaw/pysb-pkpd@v0.3.3
```
Or to upgrade from an older version:
```
pip install --upgrade git+https://github.com/blakeaw/pysb-pkpd@v0.3.3
```
##### without git installed:

Fresh install:
```
pip install https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.3.3.zip
```
Or to upgrade from an older version:
```
pip install --upgrade https://github.com/blakeaw/pysb-pkpd/archive/refs/tags/v0.3.3.zip
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

**pysb-pkpd** is an add-on for the [PySB](https://pysb.org/) modeling framework. Its key feature is a set of domain-specific PySB macros that facilitate the efficient and descriptive programmatic construction of PK/PD models in Python using the PySB framework. It also provides a limited set of pre-constructed one-, two-, and three-compartment PK and PK/PD models.

Additional details, such as examples and the list of available macros, can be found in the subsequent subsections of this README. 

You can also check out my blog post, [Modeling Drug Dynamics using Programmatic PK/PD Models in Python: An Introduction to PK/PD Modeling using PySB and pysb-pkpd](https://blakeaw.github.io/2023-10-23-pysb-pkpd/), for an introduction to PK/PD modeling concepts and additional illustrative case studies of building PK/PD models with `pysb` and `pysb-pkpd`. 

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
  * `loglinear_effect` - Adds a log-linear effect model expression for the specified drug/specis in a given compartment. Generates a PySB Expression with name: 'LogLinearEffect_expr_DrugName_CompartmentName'
  * `fixed_effect` - Adds a fixed-effect model expression for the specified drug/specis in a given compartment. Generates a PySB Expression with name: 'FixedEffect_expr_DrugName_CompartmentName'

Dosing functions:

  * `dose_bolus` - adds an instantaneous bolus dose of the specified drug/species which defines the initial concentration at time zero; e.g., to model IV bolus.
  * `dose_infusion` - adds a continous (zero-order) infusion of the specified drug/species; e.g., to model continuous IV infusion. 
  * `dose_absorbed` - adds a dose of the specified drug which is absorbed into the specified compartment via first-order kinetics, including a bioavailibity factor; e.g., to model oral dosing or a subcutaneous depot. 

### Simulating models

`pysb-pkpd` provides a `simulate` function that can be used to easily 
execute a simulation of your PK/PD model as below:

```python
import numpy as np
import pysb.pkpd as pkpd
from my_pkpd_model import model

# Simulate the PKPD/PySB model.
## Set the timespan for the simulation:
tspan = np.arange(241) # 0-240 seconds at 1 second intervals
## Execute the simulation:
simulation_trajectory = pkpd.simulate(model, tspan)
```


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

 * **Issues** :bug: : Please open a [GitHub Issue](https://github.com/blakeaw/pysb-pkpd/issues) to
report any problems/bugs with the code or its execution, or to make any feature requests.

 * **Discussions** :grey_question: : If you have questions, suggestions, or want to discuss anything else related to the project, feel free to use the [pysb-pkpd Discussions](https://github.com/blakeaw/pysb-pkpd/discussions) board.
* **Support** :question: : For any other support inquiries you can send an email to [blakeaw1102@gmail.com](mailto:blakeaw1102@gmail.com).

------

# Contributing

Interested in contributing to this project? See [CONTRIBUTING](./CONTRIBUTING.md) for details.

------

# Supporting

I'm very happy that you've chosen to use __pysb-pkpd__. This add-on is a project that I develop and maintain on my own time, independently of the core PySB library, and without external funding. If you've found it helpful, here are a few ways you can support its ongoing development:

* **Star** :star: : Show your support by starring the [pysb-pkpd GitHub repository](https://github.com/blakeaw/pysb-pkpd). It helps increase the project's visibility and lets others know it's useful. It also benefits my motivation to continue improving the package!
* **Share** :mega: : Sharing `pysb-pkpd` on your social media, forums, or with your network is another great way to support the project. It helps more people discover `pysb-pkpd`, which in turn motivates me to keep developing!
* **Cite** :books: : Citing or mentioning this software in your work, publications, or projects is another valuable way to support it. It helps spread the word and acknowledges the effort put into its development, which is greatly appreciated!
* **Sponsor** :dollar: : Even small financial contributions, such as spotting me the cost of a tea through Ko-fi so I can get my caffeine fix, can make a big difference! Every little bit can help me continue developing this and other open-source projects. 

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J4ZUCVU)

-----

# Other Useful Tools

## Parameter estimation

Please see packages such as [simplePSO](https://github.com/LoLab-MSM/simplePSO), [PyDREAM](https://github.com/LoLab-MSM/PyDREAM), [Gleipnir](https://github.com/LoLab-MSM/Gleipnir), or [GAlibrate](https://github.com/blakeaw/GAlibrate) for tools to do PySB model parameter estimation using stochastic optimization or Bayesian Monte Carlo approaches.

## PD response models

If you want to separately fit response data independetly of PK data, then the [pharmacodynamic-response-models](https://github.com/NTBEL/pharmacodynamic-response-models) package may also be useful.  

## PySB model visualization

[pyvipr](https://github.com/LoLab-MSM/pyvipr) can be used for static and dynamic PySB model visualizations.

-----