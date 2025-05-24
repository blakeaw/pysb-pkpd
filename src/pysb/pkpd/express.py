from pysb import Model, Compartment, Monomer, Parameter, Expression, Observable, Initial
import macros

DOSING_OPTIONS = {
    "iv-bolus": macros.dose_bolus,
    "iv-infusion": macros.dose_infusion,
    "oral": macros.dose_absorbed,
}


PD_MODELS = {
    "emax": macros.emax,
    "sigmoidal-emax": macros.sigmoidal_emax,
    "linear": macros.linear_effect,
    "log-linear": macros.loglinear_effect,
    "fixed": macros.fixed_effect,
}


def one_compartment_model(
    dose_amount: float,
    dose_route: str = "iv-bolus",
    volume_distribution: float = 1.0,
    clearance: float = 0.5,
    pd_model: dict | None = None,
):
    """Generates a standard one-compartment PK/PD model.

    Args:
        dose_amount (float): The amount of drug in the dose.
        dose_route (str, optional): The route of drug adminstration. Defaults to "iv-bolus".
            Options: 'iv-bolus', 'iv-infusion', 'oral'.
        volume_distribution (float, optional): Volume of distribution; i.e., the volume of
            the central compartment. Defaults to 1..
        clearance (float, optional): Clearance rate of the drug (volume/time). Defaults to 0.5.
        pd_model (dict | None, optional): Set the PD model and its paramters. Defaults to None.
            Options: 
                'emax' - parameters: 'emax', 'ec50'
                'sigmoidal-emax' - parameters: 'emax', 'ec50', 'n'
                'linear' - parameters: 'slope', 'intercept'
                'log-linear' - parameters: 'slope', 'intercept'
                'fixed' - parameters: 'e_fixed', 'c_threshold'

    Returns:
        pysb.Model: The model.

    Examples
    --------
    Oral administration with Emax PD::

        model = one_compartment_model(
            100.0,  # mg
            dose_route="oral",
            volume_distribution=10.0,  # L
            clearance=0.750,  # L/min
            pd_model={
                "emax": {
                    "emax": 2.2,
                    "ec50": 50.0,  # mg
                }
            },
        )

    I.V. infusion administration with linear PD::

        model = one_compartment_model(
            100.0,  # mg
            dose_route="iv-infusion",
            volume_distribution=10.0,  # L
            clearance=0.750,  # L/min
            pd_model={
                "linear": {
                    "slope": 0.2, # mg^-1
                    "intercept": 1.2,
                }
            },
        )
    """
    model = Model("one-compartment-model")
    macros.drug_monomer()
    Parameter("Vd", volume_distribution)
    macros.one_compartment(c1_size=Vd)
    Parameter("dose", dose_amount)
    DOSING_OPTIONS[dose_route](Drug, CENTRAL, dose)
    if clearance > 0:
        Parameter("CL", clearance)
        macros.clearance(Drug, CENTRAL, CL)
    if pd_model is not None:
        for key, value in pd_model.items():
            PD_MODELS[key](Drug, CENTRAL, **value)
    return model

def two_compartment_model(
    dose_amount: float,
    dose_route: str = "iv-bolus",
    volume_central: float = 1.0,
    volume_peripheral: float = 1.0,
    k12: float = 1e-1,
    k21: float = 1e-2,
    clearance: float = 0.5,
    pd_model: dict | None = None,
):
    """Generates a standard two-compartment PK/PD model.

    Args:
        dose_amount (float): The amount of drug in the dose.
        dose_route (str, optional): The route of drug adminstration. Defaults to "iv-bolus".
            Options: 'iv-bolus', 'iv-infusion', 'oral'.
        volume_central (float, optional): Volume of the central compartment. Defaults to 1..
        volume_peripheral (float, optional): Volume of the peripheral compartment. Defaults to 1..
        k12 (float, optional): The rate constant for distribution from the cental to peripheral
            compartment. Defaults to 0.1.
        k21 (float, optional): The rate constant for redistribution from the peripheral to central
            compartment. Defaults to 0.01.
        clearance (float, optional): Clearance rate of the drug (volume/time). Defaults to 0.5.
        pd_model (dict | None, optional): Set the PD model and its paramters. Defaults to None.
            Options: 
                'emax' - parameters: 'emax', 'ec50'
                'sigmoidal-emax' - parameters: 'emax', 'ec50', 'n'
                'linear' - parameters: 'slope', 'intercept'
                'log-linear' - parameters: 'slope', 'intercept'
                'fixed' - parameters: 'e_fixed', 'c_threshold'

    Returns:
        pysb.Model: The model.

    Examples
    --------
    Oral administration with Emax PD::

        model = two_compartment_model(
            100.0,  # mg
            dose_route="oral",
            volume_central=10.0,  # L
            volume_peripheral=2.0, # L
            k12=1e-2, # min^-1
            k21=1e-4, # min^-1
            clearance=0.750,  # L/min
            pd_model={
                "emax": {
                    "emax": 2.2,
                    "ec50": 50.0,  # mg
                }
            },
        )

    I.V. infusion administration with linear PD::

        model = two_compartment_model(
            100.0,  # mg
            dose_route="iv-infusion",
            volume_central=10.0,  # L
            volume_peripheral=2.0, # L
            k12=1e-2, # min^-1
            k21=1e-4, # min^-1
            clearance=0.750,  # L/min
            pd_model={
                "linear": {
                    "slope": 0.2, # mg^-1
                    "intercept": 1.2,
                }
            },
        )
    """
    model = Model("two-compartment-model")
    macros.drug_monomer()
    Parameter("Vc", volume_central)
    Parameter("Vp", volume_peripheral)
    macros.two_compartments(c1_size=Vc, c2_size=Vp)
    Parameter("dose", dose_amount)
    DOSING_OPTIONS[dose_route](Drug, CENTRAL, dose)
    if clearance > 0:
        Parameter("CL", clearance)
        macros.clearance(Drug, CENTRAL, CL)
    if pd_model is not None:
        for key, value in pd_model.items():
            PD_MODELS[key](Drug, CENTRAL, **value)
    return model