`pysb-pkpd` includes functions to quickly generate standard one-, two-, and three-compartment PK/PD models.

## Model Generators

* `pkpd.standard.one_compartment_model` - Generate a standard one-compartment PK model with an optional PD model as a function of drug concentration in the model `CENTRAL` compartment. The PK model includes drug clearance from the `CENTRAL` compartment. [API Reference](reference.md#pkpd.standard.one_compartment_model)
* `pkpd.standard.two_compartment_model` - Generate a standard two-compartment PK model with an optional PD model as a function of drug concentration in the model `CENTRAL` compartment. The PK model includes two comparments (`CENTRAL` and `PERIPHERAL`), drug clearance from the `CENTRAL` compartment, and drug distribution/re-distribution between the `CENTRAL` and `PERIPHERAL` compartments. [API Reference](reference.md#pkpd.standard.two_compartment_model)
* `pkpd.standard.three_compartment_model` - Generate a standard three-compartment PK model with an optional PD model as a function of drug concentration in the model `CENTRAL` compartment. The PK model includes three comparments (`CENTRAL`, `PERIPHERAL`, and `DEEPPERIPHERAL`), drug clearance from the `CENTRAL` compartment, and drug distribution/re-distribution between the `CENTRAL` and `PERIPHERAL` compartments and the `CENTRAL` and `DEEPPERIPHERAL` compartments. [API Reference](reference.md#pkpd.standard.three_compartment_model)

### Dose routes and parameters

The dose route is specified with the `dose_route` input argument with optional parameters specified via the `dose_parameters` argument. The options are:

* `'iv-bolus'` with 

### Setting the PD model

PD models are specified with the optional `pd_model` input argument which takes a nested dictionary. The outer dictionary key specifies the model type while the inner dictionary specifies the model parameters and their values. The options are:

* `'emax'` model with parameters `'emax'` and `'ec50'`. Example input: `pd_model={'emax':{'emax': 2.0, 'ec50':52.4}}`
* `'sigmoidal-emax'` with parameters `'emax'`, `'ec50'`, and `'n'`. Example input: `pd_model={'sigmoidal-emax':{'emax': 2.0, 'ec50':52.4, 'n':1.1}}` 
* `'linear'` with parameters `'slope'` and `'intercept'`. Example input: `pd_model={'linear':{'slope': 1.4, 'intercept':0.43}}`
* `'log-linear'` with parameters `'slope'` and `'intercept'`. Example input: `pd_model={'log-linear':{'slope': 1.4, 'intercept':0.43}}`
* `'fixed'` with parameters `'e_fixed'` and `'c_threshold'`. Example input: `pd_model={'fixed':{'e_fixed': 4.7, 'c_threshold':100.0}}`

## Example

One-compartment model with oral administration and an Emax PD model:
```python
model = one_compartment_model(
    100.0,  # mg
    dose_route="oral",
    dose_parameters={
        'ka': 1e-1, # min^-1
         'f': 0.95,
    },
    volume_distribution=10.0,  # L
    clearance=0.750,  # L/min
    pd_model={
        "emax": {
            "emax": 2.2,
            "ec50": 50.0,  # mg
        }
    },
)
```