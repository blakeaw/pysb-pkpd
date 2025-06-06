---
icon: material/home
---

# Welcome to `pysb-pkpd`'s Documentation

_**pysb-pkpd**: program and simulate dynamic PK/PD and QSP models in Python using the PySB modeling framework_

## Overview

`pysb-pkpd` is a domain-specific extension to the [PySB](https://pysb.org/) modeling framework that facilitates programming and simulating dynamic **pharmacokinetic/pharmacodynamic (PK/PD)** and **quantitative systems pharmacology (QSP)** models in [Python](https://www.python.org/). 

### Key Features

`pysb-pkpd` has the following key features:

- **Domain-specific PySB macros** - set of domain-specific PySB macros that facilitate the efficient and descriptive programmatic construction of compartmental PK/PD models.
- **Standard one-, two-, and three-compartment model generators** - functions to quickly and easily construct standard one-, two-, and three-compartment PK/PD models.

### Why Use `pysb-pkpd`?

Built on **[PySB](https://pysb.org/)**, a powerful programmatic and rule-based framework for biochemical modeling, `pysb-pkpd` offers a variety of benefits, including:

- **Programmatic Modeling** – Enables automated workflows, reproducibility (_e.g., version control and automated testing_), customization, and creation of reusable functions for pharmacological and biochemical processes.
- **Built-in Support for Mechanistic Modeling** – Leverage PySB's mechanistic modeling framework to incorporate additional biochemical mechanisms and build customized mechanistic PK/PD and QSP/QST models.
- **Rule-Based Approach** – Encode complex pharmacological and biochemical processes using intuitive [rule-based modeling](https://en.wikipedia.org/wiki/Rule-based_modeling). No need to enumerate all reactions/molecular species or manually encode the corresponding network of differential equations.
- **Python-Based** – Seamlessly integrates with Python’s scientific computing ecosystem, supporting advanced simulations, data analysis, and visualization.
- **Arbitrary Number of Compartments** – Specify any number of compartments to build custom multi-compartment models, including complex drug distribution and physiologically-based pharmacokinetic (PBPK) models.

------

## Installation
  1. Install **PySB** using [conda](https://docs.conda.io/en/latest/) or [mamba](https://github.com/mamba-org/mamba):
    ```bash
    conda install -c alubbock pysb
    ```
    **OR**
    ```bash
    mamba install -c alubbock pysb
    ```    
  2. Install **pysb-pkpd** with pip:
    ```bash
    pip install git+https://github.com/blakeaw/pysb-pkpd@v0.5.0
    ```
Ensure you have Python 3.11.3+ and PySB 1.15.0 installed.

## Quick-start Example

### 1. Using model generator function (quick and easy standard model construction)

Here’s a simple workflow to define and simulate a one-compartment PK model with an Emax PD function using the model generator functions:

```py
from pysb.pkpd import standard, util

# Define a simple one-compartment model
model = standard.one_compartment_model(dose_amount=100,
                                       dose_route='iv-bolus',
                                       volume_distribution=10.,
                                       clearance=0.5,
                                       pd_model={'emax':
                                           {'emax':2.2,
                                            'ec50': 225.8}
                                       }
                                       )
# Simulate concentration over time
simulation_results = util.simulate(model, 
                                   tspan=list(range(100)),
                                  )

```

### 2. Using PK/PD model macros (flexible and customizable programmatic model definition)

Here’s a simple workflow to define and simulate the same one-compartment PK model with an Emax PD function (same as above) using the PK/PD macros inside a model module file:

  1. Define `model.py` with the following code (the model is a Python module in this case):
```py
from pysb import Model
import pysb.pkpd as pkpd

# Initialize the PySB model:
Model()

# Add a Monomer for the drug:
pkpd.drug_monomer(name='Drug')

# Add the compartment for a one-compartment model:
pkpd.one_compartment(c1_name="CENTRAL",
                             c1_size=10.)

# Add a dose of the drug using an 
# instantaneous 'bolus' dose in the central
# compartment (initial amount of drug at time zero).
#   Note that dose is an amount such as weight, mass, or moles,
#     which will be converted automatically to an initial concentration
#     as: 
#         [Drug]_0 = dose / V_CENTRAL , 
#     where V_CENTRAL is the size (i.e., volume) of the central compartment.
pkpd.dose_bolus(Drug, CENTRAL, dose=100.)

# Include (linear) systemic clearance of Drug from the central compartment.
pkpd.clearance(Drug, CENTRAL, cl=0.5)

# Add the Emax PD function for Drug in the
# central compartment:
pkpd.emax(Drug, CENTRAL, emax=2.2,
                         ec50=225.8)
```
2. Import and simulate the model:
```py
from model import model
from pysb.pkpd import util

# Simulate concentration over time
simulation_results = util.simulate(model, 
                                   tspan=list(range(100)),
                                  )

```

## Acknowledgements

Special thanks for [Martin Breuss's MkDocs tuorial](https://realpython.com/python-project-documentation-with-mkdocs/#step-2-create-the-sample-python-package).