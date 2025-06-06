# Available PK/PD macros

The following PySB-style macro functions encoding key PK, PD, and dosing processes are available for model construction:

## PK functions

  * `drug_monomer` - adds a simple monomer species for the drug to the model. If the drug needs binding sites or other state variables then you should directly use the PySB `Monomer` class instead. [API Reference](reference.md#pkpd.macros.drug_monomer)
  * `one_compartment` - adds one compartment to the model for a one-comaprtment PK model. Alternatively, it could be used to add a new compartment to a multi-compartment model. [API Reference](reference.md#pkpd.macros.one_compartment)
  * `two_compartments` - adds two compartments to the model for a two-comaprtment PK model. [API Reference](reference.md#pkpd.macros.two_compartments)
  * `three_compartments` - adds three compartments to the model for a three-compartment PK model. [API Reference](reference.md#pkpd.macros.three_compartments)
  * `eliminate` - adds linear (1st-order) elimination of the specified drug/species from a compartment. [API Reference](reference.md#pkpd.macros.eliminate)
  * `eliminate_mm` - add non-linear, Michaelis-Menten, elimination of the specified drug/species from a compartment. [API Reference](reference.md#pkpd.macros.eliminate_mm)
  * `clearance` - adds linear (1st-order) elimination of the specified drug/species from a compartment by systemic clearance. [API Reference](reference.md#pkpd.macros.clearance)
  * `distribute` - adds distribution/redistribution of the specified drug/species between two compartments. [API Reference](reference.md#pkpd.macros.distribute)
  * `transfer` - adds one-way transfer (distribution with no redistribution) of the specified drug/species from one compartment to another. [API Reference](reference.md#pkpd.macros.transfer)

## PD functions

  * `emax` - Adds an Emax model expression for the specified drug/species in a given compartment. Generates a PySB Expression with name: 'Emax_expr_DrugName_CompartmentName'. [API Reference](reference.md#pkpd.macros.emax). 
Equation:
$$
E = E_{\textrm{max}} \frac{\left[\textrm{Drug}\right]}{\left[\textrm{Drug}\right] + EC_{\textrm{50}}}
$$
  * `sigmoidal_emax` - Adds a sigmoidal Emax model expression for the specified drug/species in a given compartment. Generates a PySB Expression with name: 'Emax_expr_DrugName_CompartmentName'. [API Reference](reference.md#pkpd.macros.sigmoidal_emax). Equation:
$$
E = E_{\textrm{max}} \frac{\left[\textrm{Drug}\right]^n}{\left[\textrm{Drug}\right]^n + EC_{\textrm{50}}^n}
$$
  * `linear_effect` - Adds a linear effect model expression for the specified drug/specis in a given compartment. Generates a PySB Expression with name: 'LinearEffect_expr_DrugName_CompartmentName'. [API Reference](reference.md#pkpd.macros.linear_effect). Equation:
$$
E = m \left[\textrm{Drug}\right] + b
$$
  * `loglinear_effect` - Adds a log-linear effect model expression for the specified drug/specis in a given compartment. Generates a PySB Expression with name: 'LogLinearEffect_expr_DrugName_CompartmentName'. [API Reference](reference.md#pkpd.macros.loglinear_effect). Equation:
$$
E = m \log(\left[\textrm{Drug}\right]) + b
$$
  * `fixed_effect` - Adds a fixed-effect model expression for the specified drug/species in a given compartment. Generates a PySB Expression with name: 'FixedEffect_expr_DrugName_CompartmentName'. [API Reference](reference.md#pkpd.macros.fixed_effect). Equation:
$$
E = E_{\textrm{fixed}} \, \, , \, \left[\textrm{Drug}\right] > C_{\textrm{threshold}}
$$
$$
E = 0  \, \, , \, \left[\textrm{Drug}\right] \leq C_{\textrm{threshold}}
$$
## Dosing functions

  * `dose_bolus` - adds an instantaneous bolus dose of the specified drug/species which defines the initial concentration at time zero; e.g., to model IV bolus.
  * `dose_infusion` - adds a continous (zero-order) infusion of the specified drug/species; e.g., to model continuous IV infusion. 
  * `dose_absorbed` - adds a dose of the specified drug which is absorbed into the specified compartment via first-order kinetics, including a bioavailibity factor; e.g., to model oral dosing or a subcutaneous depot. 

For additional details on each function see the [macros API Reference](reference.md#pkpd.macros).

## Example

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