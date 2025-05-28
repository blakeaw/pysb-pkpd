from pysb import Model, Compartment, Monomer, Parameter, Expression, Observable, Initial
from . import macros

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

PD_MODEL_ARGS = {
    "emax": ["emax", "ec50"],
    "sigmoidal-emax": ["emax", "ec50", "n"],
    "linear": ["slope", "intercept"],
    "log-linear": ["slope", "intercept"],
    "fixed": ["e_fixed", "c_threshold"],
}


def one_compartment_model(
    dose_amount: float,
    dose_route: str = "iv-bolus",
    dose_parameters: dict | None = None,
    volume_distribution: float = 1.0,
    clearance: float = 0.5,
    pd_model: dict | None = None,
):
    """Generates a standard one-compartment PK/PD model.

    Parameters
    ----------
    dose_amount : float
        The amount of drug in the dose.
    dose_route : str, optional
        The route of drug adminstration. Default="iv-bolus".
        Options: 'iv-bolus', 'iv-infusion', 'oral'.
    dose_parameters : dict | None, optional
        Additional special dose/route parameters. Only
        required for the 'oral' route with parameters:
        'ka' - 1st-order absorption rate constant.
        'f' - bioavailibity fraction.
    volume_distribution : float, optional
        Volume of distribution; i.e., the volume of the central compartment.
        Default=1..
    clearance : float, optional
        Clearance rate of the drug (volume/time). Default=0.5.
    pd_model : dict | None, optional
        Set the PD model and its paramters. Default=None.
        Options:
            'emax' - parameters: 'emax', 'ec50'
            'sigmoidal-emax' - parameters: 'emax', 'ec50', 'n'
            'linear' - parameters: 'slope', 'intercept'
            'log-linear' - parameters: 'slope', 'intercept'
            'fixed' - parameters: 'e_fixed', 'c_threshold'

    Returns
    -------
    model: pysb.Model
        The generated model.

    Examples
    --------
    Oral administration with Emax PD::

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
    if dose_parameters is None:
        dose_parameters = {}
    DOSING_OPTIONS[dose_route](Drug, CENTRAL, dose, **dose_parameters)
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
    dose_parameters: dict | None = None,
    volume_central: float = 1.0,
    volume_peripheral: float = 1.0,
    k12: float = 1e-1,
    k21: float = 1e-2,
    clearance: float = 0.5,
    pd_model: dict | None = None,
):
    """Generates a standard two-compartment PK/PD model.

    Parameters
    ----------
    dose_amount : float
        The amount of drug in the dose.
    dose_route : str, optional
        The route of drug adminstration. Default="iv-bolus".
        Options: 'iv-bolus', 'iv-infusion', 'oral'.
    dose_parameters : dict | None, optional
        Additional special dose/route parameters. Only
        required for the 'oral' route with parameters:
            'ka' - 1st-order absorption rate constant.
            'f' - bioavailibity fraction.
    volume_central : float, optional
        Volume of the central compartment. Default=1..
    volume_peripheral : float, optional
        Volume of the peripheral compartment. Default=1..
    k12 : float, optional)
        The rate constant for distribution from the cental to peripheral
        compartment. Default=0.1.
    k21 : float, optional
        The rate constant for redistribution from the peripheral to central
        compartment. Default=0.01.
    clearance : float, optional
        Clearance rate of the drug (volume/time). Default=0.5.
    pd_model : dict | None, optional
        Set the PD model and its paramters. Default=None.
        Options:
            'emax' - parameters: 'emax', 'ec50'
            'sigmoidal-emax' - parameters: 'emax', 'ec50', 'n'
            'linear' - parameters: 'slope', 'intercept'
            'log-linear' - parameters: 'slope', 'intercept'
            'fixed' - parameters: 'e_fixed', 'c_threshold'

    Returns
    -------
    model : pysb.Model
        The generated model.

    Examples
    --------
    Oral administration with Emax PD::

        model = two_compartment_model(
            100.0,  # mg
            dose_route="oral",
            dose_parameters={
                'ka': 1e-1, # min^-1
                 'f': 0.95,
            },
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
    if dose_parameters is None:
        dose_parameters = {}
    DOSING_OPTIONS[dose_route](Drug, CENTRAL, dose, **dose_parameters)
    if clearance > 0:
        Parameter("CL", clearance)
        macros.clearance(Drug, CENTRAL, CL)
    if pd_model is not None:
        for key, value in pd_model.items():
            PD_MODELS[key](Drug, CENTRAL, **value)
    macros.distribute(Drug, CENTRAL, PERIPHERAL, klist=[k12, k21])
    return model


def three_compartment_model(
    dose_amount: float,
    dose_route: str = "iv-bolus",
    dose_parameters: dict | None = None,
    volume_central: float = 1.0,
    volume_peripheral: float = 1.0,
    volume_deep_peripheral: float = 1.0,
    k12: float = 1e-1,
    k21: float = 1e-2,
    k13: float = 1e-3,
    k31: float = 1e-4,
    clearance: float = 0.5,
    pd_model: dict | None = None,
):
    """Generates a standard three-compartment PK/PD model.

    Parameters
    ----------
    dose_amount : float
        The amount of drug in the dose.
    dose_route : str, optional
        The route of drug adminstration. Default="iv-bolus".
        Options: 'iv-bolus', 'iv-infusion', 'oral'.
    dose_parameters : dict | None, optional
        Additional special dose/route parameters. Only
        required for the 'oral' route with parameters:
            'ka' - 1st-order absorption rate constant.
            'f' - bioavailibity fraction.
    volume_central : float, optional
        Volume of the central compartment. Default=1..
    volume_peripheral : float, optional
        Volume of the peripheral compartment. Default=1..
    k12 : float, optional
        The rate constant for distribution from the cental to peripheral
        compartment. Default=0.1.
    k21 : float, optional
        The rate constant for redistribution from the peripheral to central
        compartment. Default=0.01.
    k13 : float, optional
        The rate constant for distribution from the cental to deep peripheral
        compartment. Default=0.001.
    k31 : float, optional
        The rate constant for redistribution from the deep peripheral to central
        compartment. Default=0.0001.
    clearance : float, optional
        Clearance rate of the drug (volume/time). Default=0.5.
    pd_model : dict | None, optional
        Set the PD model and its paramters. Default=None.
        Options:
            'emax' - parameters: 'emax', 'ec50'
            'sigmoidal-emax' - parameters: 'emax', 'ec50', 'n'
            'linear' - parameters: 'slope', 'intercept'
            'log-linear' - parameters: 'slope', 'intercept'
            'fixed' - parameters: 'e_fixed', 'c_threshold'

    Returns
    -------
    model : pysb.Model
        The generated model.

    Examples
    --------
    Oral administration with Emax PD::

        model = three_compartment_model(
            100.0,  # mg
            dose_route="oral",
            dose_parameters={
                'ka': 1e-1, # min^-1
                 'f': 0.95,
            },
            volume_central=10.0,  # L
            volume_peripheral=2.0, # L
            k12=1e-2, # min^-1
            k21=1e-4, # min^-1
            k13=1e-3, # min^-1
            k31=1e-5, # min^-1
            clearance=0.750,  # L/min
            pd_model={
                "emax": {
                    "emax": 2.2,
                    "ec50": 50.0,  # mg
                }
            },
        )

    I.V. infusion administration with linear PD::

        model = three_compartment_model(
            100.0,  # mg
            dose_route="iv-infusion",
            volume_central=10.0,  # L
            volume_peripheral=2.0, # L
            k12=1e-2, # min^-1
            k21=1e-4, # min^-1
            k13=1e-3, # min^-1
            k31=1e-5, # min^-1
            clearance=0.750,  # L/min
            pd_model={
                "linear": {
                    "slope": 0.2, # mg^-1
                    "intercept": 1.2,
                }
            },
        )
    """
    model = Model("three-compartment-model")
    macros.drug_monomer()
    Parameter("Vc", volume_central)
    Parameter("Vp", volume_peripheral)
    Parameter("Vdp", volume_deep_peripheral)
    macros.three_compartments(c1_size=Vc, c2_size=Vp, c3_size=Vdp)
    Parameter("dose", dose_amount)
    if dose_parameters is None:
        dose_parameters = {}
    DOSING_OPTIONS[dose_route](Drug, CENTRAL, dose, **dose_parameters)
    if clearance > 0:
        Parameter("CL", clearance)
        macros.clearance(Drug, CENTRAL, CL)
    if pd_model is not None:
        for key, value in pd_model.items():
            PD_MODELS[key](Drug, CENTRAL, **value)
    macros.distribute(Drug, CENTRAL, PERIPHERAL, klist=[k12, k21])
    macros.distribute(Drug, CENTRAL, DEEPPERIPHERAL, klist=[k13, k31])
    return model
