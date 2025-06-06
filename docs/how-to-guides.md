# How-To Guides

## How to Simulate a Model

`pysb-pkpd` provides a `simulate` function that can be used to easily 
execute a dynamic ODE-based simulation of your PK/PD model as below:

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

## How to Incorporate and Manage Units in Models

PySB doesn't natively support incorporating and managing units in models, however, we've developed another extension package that adds these features: [pysb-units](https://github.com/Borealis-BioModeling/pysb-units).

You can install this add-on using pip:
```sh
pip install git+https://github.com/Borealis-BioModeling/pysb-units@v0.4.0
```

Then, we can define a pretty minimal example with a one-compartment PK model (`model.py`):

```py
# Import the pysb components:
from pysb import Model, Parameter, Monomer, Initial, Observable, Expression
# Import the pysb-pkpd macros module:
from pysb.pkpd import macros as pkpd
# Import pysb-units:
import pysb.units
# Import the pysb-units context manager:
from pysb.units import units

# Add the units features to the pkpd.macros module:
pysb.units.add_macro_units(pkpd)

# Activate units using the units context manager - 
# replaces core model components with the appropriate 
# versions from pysb.units (similar to unitize) and will 
# automatically call the check function when exiting the
# context:
with units():

    # Initialize the PySB model:
    Model()

    # The primary units needed for simulating the model are 
    # concentration (or amount) and time. We can define those
    # here with SimulationUnits:
    SimulationUnits(concentration='mg/L', time='h', volume='L')

    # Add a Monomer for the drug:
    pkpd.drug_monomer(name='Drug')

    # Add the compartment for a one-compartment model:
    Parameter('Vd', 10., unit='L') # Volume of Distribution
    pkpd.one_compartment(c1_name="CENTRAL",
                                c1_size=Vd)

    # Add a dose of the drug using an 
    # instantaneous 'bolus' dose in the central
    # compartment (initial amount of drug at time zero).
    #   Note that dose is an amount such as weight, mass, or moles,
    #     which will be converted automatically to an initial concentration
    #     as: 
    #         [Drug]_0 = dose / V_CENTRAL , 
    #     where V_CENTRAL is the size (i.e., volume) of the central compartment.
    Parameter('Dose', 100., unit='mg') # Dose amount
    pkpd.dose_bolus(Drug, CENTRAL, dose=Dose)

    # Include (linear) systemic clearance of Drug from the central compartment.
    Parameter('CL', 0.5, unit='L/h') # Clearance rate
    pkpd.clearance(Drug, CENTRAL, cl=CL)
```

Note that we define each model parameter and then pass that in to the `pkpd` macros. This allows us to specify the units of each parameter. 

## 🚧 Page Still Under Development 🚧

Thank you for your interest in our **How-To Guides** section! We’re actively working on expanding these pages to provide **step-by-step instructions** and **hands-on examples** for using `pysb-pkpd`.

Our goal is to make these resources **clear, practical, and easy to follow**—but we’re still in the process of gathering content and refining details.

Stay tuned! In the meantime:

- **Have a specific question?** Feel free to explore our existing documentation or reach out to the community.
- **Want to contribute?** If you have suggestions or example workflows, we'd love to hear from you!

Check back soon for updates as we continue to improve these guides!