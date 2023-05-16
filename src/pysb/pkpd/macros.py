from pysb import Monomer, Parameter, Expression, Observable, Compartment, Initial
from pysb.core import ComponentSet, as_complex_pattern, MonomerPattern, ComplexPattern
import pysb.macros

__all__ = [
    "eliminate",
    "eliminate_mm",
    "clearance",
    "distribute",
    "transfer",
    "emax",
    "sigmoidal_emax",
    "single_dose"
]


def _check_for_monomer(species, compartment):
    if isinstance(species, Monomer):
        species = species() ** compartment
    else:
        species = species**compartment
    species = pysb.macros.as_complex_pattern(species)
    return species


def two_compartments(c1_name="CENTRAL", c1_size=1.0, c2_name="PERIPHERAL", c2_size=1.0):
    """
    Generate a reaction for linear elimination of a species from a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    kel : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """
    params_created = ComponentSet()
    C1_size = c1_size
    if not isinstance(C1_size, Parameter):
        C1_size = Parameter("V_{0}".format(c1_name), c1_size)
        params_created.add(C1_size)
    C2_size = c2_size
    if not isinstance(C2_size, Parameter):
        C2_size = Parameter("V_{0}".format(c2_name), c2_size)
        params_created.add(C2_size)
    C1 = Compartment(c1_name, size=C1_size)
    C2 = Compartment(c2_name, size=C2_size)
    compartments = ComponentSet([C1, C2])
    return compartments | params_created


def three_compartments(
    c1_name="CENTRAL",
    c1_size=1.0,
    c2_name="PERIPHERAL",
    c2_size=1.0,
    c3_name="DEEPPERIPHERAL",
    c3_size=1.0,
):
    """
    Generate a reaction for linear elimination of a species from a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    kel : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """
    params_created = ComponentSet()
    C1_size = c1_size
    if not isinstance(C1_size, Parameter):
        C1_size = Parameter("V_{0}".format(c1_name), c1_size)
        params_created.add(C1_size)
    C2_size = c2_size
    if not isinstance(C2_size, Parameter):
        C2_size = Parameter("V_{0}".format(c2_name), c2_size)
        params_created.add(C2_size)
    C3_size = c3_size
    if not isinstance(C3_size, Parameter):
        C3_size = Parameter("V_{0}".format(c3_name), c3_size)
        params_created.add(C3_size)
    C1 = Compartment(c1_name, size=C1_size)
    C2 = Compartment(c2_name, size=C2_size)
    C3 = Compartment(c3_name, size=C3_size)
    compartments = ComponentSet([C1, C2, C3])
    return compartments | params_created


def eliminate(species, compartment, kel):
    """
    Generate a reaction for linear elimination of a species from a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    kel : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """
    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    def eliminate_name_func(rule_expression):
        cps = rule_expression.reactant_pattern.complex_patterns
        # return '_'.join(pysb.macros._complex_pattern_label(cp) for cp in cps)
        return "_".join([monomer_name, comp_name])

    species = _check_for_monomer(species, compartment)

    return pysb.macros._macro_rule(
        "eliminate", species >> None, [kel], ["k"], name_func=eliminate_name_func
    )


def eliminate_mm(species, compartment, vmax, km):
    """
    Generate a reaction for Michaelis-Menten elimination of a species from a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    kel : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    def eliminate_name_func(rule_expression):
        cps = rule_expression.reactant_pattern.complex_patterns
        # return '_'.join(pysb.macros._complex_pattern_label(cp) for cp in cps)
        return "_".join([monomer_name, comp_name])

    species = _check_for_monomer(species, compartment)
    params_created = ComponentSet()
    Vmax = vmax
    if not isinstance(Vmax, Parameter):
        Vmax = Parameter("Vmax_{0}_{1}".format(monomer_name, comp_name), vmax)
        params_created.add(Vmax)
    Km = km
    if not isinstance(Km, Parameter):
        Km = Parameter("Km_{0}_{1}".format(monomer_name, comp_name), km)
        params_created.add(Km)
    obs_expr = Observable("_obs_expr_{0}_{1}".format(monomer_name, comp_name), species)
    k_expr = Expression(
        "k_expr_{0}_{1}".format(monomer_name, comp_name), Vmax / (obs_expr + Km)
    )
    expr_components = ComponentSet([obs_expr, k_expr])
    components = pysb.macros._macro_rule(
        "eliminate_mm", species >> None, [k_expr], ["k"], name_func=eliminate_name_func
    )
    components |= params_created
    components |= expr_components

    return components


def clearance(species, compartment, cl):
    """
    Generate a reaction for the systemic clearance of a species from a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    kel : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """
    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    def clearance_name_func(rule_expression):
        cps = rule_expression.reactant_pattern.complex_patterns
        # return '_'.join(pysb.macros._complex_pattern_label(cp) for cp in cps)
        return "_".join([monomer_name, comp_name])

    species = _check_for_monomer(species, compartment)
    params_created = ComponentSet()
    CL = cl
    if not isinstance(CL, Parameter):
        CL = Parameter("CL_{0}_{1}".format(monomer_name, comp_name), cl)
        params_created.add(CL)
    Vcomp = compartment.size
    k_expr = Expression("k_CL_expr_{0}_{1}".format(monomer_name, comp_name), CL / Vcomp)
    expr_components = ComponentSet([k_expr])
    components = pysb.macros._macro_rule(
        "clearance", species >> None, [k_expr], ["k"], name_func=clearance_name_func
    )
    components |= expr_components
    return components | params_created


def distribute(species, c1, c2, klist):
    """
    Generate the unimolecular reversible equilibrium reaction species ** c1 <-> species ** c2.

    Parameters
    ----------
    species : Monomer or MonomerPattern
    c1 : Compartment
    c2 : Compartment
    klist : list of 2 Parameters or list of 2 numbers
        Forward (S1 -> S2) and reverse rate constants (in that order). If
        Parameters are passed, they will be used directly in the generated
        Rules. If numbers are passed, Parameters will be created with
        automatically generated names based on the names and states of S1 and S2
        and these parameters will be included at the end of the returned
        component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains one reversible Rule and optionally
        two Parameters if klist was given as plain numbers.

    Examples
    --------
    Simple two-state equilibrium between A and B::

        Model()
        Monomer('A')
        Monomer('B')
        equilibrate(A(), B(), [1, 1])

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('A')
        Monomer('A')
        >>> Monomer('B')
        Monomer('B')
        >>> equilibrate(A(), B(), [1, 1]) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('equilibrate_A_to_B', A() | B(), equilibrate_A_to_B_kf, equilibrate_A_to_B_kr),
         Parameter('equilibrate_A_to_B_kf', 1.0),
         Parameter('equilibrate_A_to_B_kr', 1.0),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name

    # turn any Monomers into MonomerPatterns
    def distribute_name_func(rule_expression):
        cps = rule_expression.reactant_pattern.complex_patterns
        # return '_'.join(pysb.macros._complex_pattern_label(cp) for cp in cps)
        return "_".join([monomer_name, c1.name, "to", c2.name])

    s1 = _check_for_monomer(species, c1)
    s2 = _check_for_monomer(species, c2)
    return pysb.macros._macro_rule(
        "distribute", s1 | s2, klist, ["kf", "kr"], name_func=distribute_name_func
    )


def transfer(species, c1, c2, k):
    """
    Generate the unimolecular reaction species ** c1 --> species ** c2.

    Parameters
    ----------
    species : Monomer or MonomerPattern
    c1 : Compartment
    c2 : Compartment
    k :  Parameter or number

    Returns
    -------
    components : ComponentSet
        The generated components. Contains one reversible Rule and optionally
        two Parameters if klist was given as plain numbers.

    Examples
    --------
    Simple two-state equilibrium between A and B::

        Model()
        Monomer('A')
        Monomer('B')
        equilibrate(A(), B(), [1, 1])

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('A')
        Monomer('A')
        >>> Monomer('B')
        Monomer('B')
        >>> equilibrate(A(), B(), [1, 1]) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('equilibrate_A_to_B', A() | B(), equilibrate_A_to_B_kf, equilibrate_A_to_B_kr),
         Parameter('equilibrate_A_to_B_kf', 1.0),
         Parameter('equilibrate_A_to_B_kr', 1.0),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name

    # turn any Monomers into MonomerPatterns
    def transfer_name_func(rule_expression):
        cps = rule_expression.reactant_pattern.complex_patterns
        # return '_'.join(pysb.macros._complex_pattern_label(cp) for cp in cps)
        return "_".join([monomer_name, c1.name, "to", c2.name])

    s1 = _check_for_monomer(species, c1)
    s2 = _check_for_monomer(species, c2)
    return pysb.macros._macro_rule(
        "transfer", s1 >> s2, [k], ["k"], name_func=transfer_name_func
    )


def emax(species, compartment, emax, ec50):
    """
    Generate an expression for Emax model for effect of species in a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    emax : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    ec50 : Parameter or number

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    species = _check_for_monomer(species, compartment)
    params_created = ComponentSet()
    Emax = emax
    if not isinstance(Emax, Parameter):
        Emax = Parameter("Emax_{0}_{1}".format(monomer_name, comp_name), emax)
        params_created.add(Emax)
    EC50 = ec50
    if not isinstance(EC50, Parameter):
        EC50 = Parameter("EC50_{0}_{1}".format(monomer_name, comp_name), ec50)
        params_created.add(EC50)
    obs_expr = Observable(
        "_obs_emax_expr_{0}_{1}".format(monomer_name, comp_name), species
    )
    expr = Expression(
        "Emax_expr_{0}_{1}".format(monomer_name, comp_name),
        (Emax * obs_expr) / (obs_expr + EC50),
    )
    expr_components = ComponentSet([obs_expr, expr])

    return expr_components | params_created


def sigmoidal_emax(species, compartment, emax, ec50, n):
    """
    Generate an expression for a sigmoidal Emax model for effect of species in a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    emax : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    ec50 : Parameter or number

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    species = _check_for_monomer(species, compartment)
    params_created = ComponentSet()
    Emax = emax
    if not isinstance(Emax, Parameter):
        Emax = Parameter("Emax_{0}_{1}".format(monomer_name, comp_name), emax)
        params_created.add(Emax)
    EC50 = ec50
    if not isinstance(EC50, Parameter):
        EC50 = Parameter("EC50_{0}_{1}".format(monomer_name, comp_name), ec50)
        params_created.add(ec50)
    hill_coeff = n
    if not isinstance(n, Parameter):
        hill_coeff = Parameter("n_{0}_{1}".format(monomer_name, comp_name), n)
        params_created.add(hill_coeff)
    obs_expr = Observable(
        "_obs_emax_expr_{0}_{1}".format(monomer_name, comp_name), species
    )
    expr = Expression(
        "Emax_expr_{0}_{1}".format(monomer_name, comp_name),
        (Emax * obs_expr**hill_coeff) / (obs_expr**hill_coeff + EC50**hill_coeff),
    )
    expr_components = ComponentSet([obs_expr, expr])

    return expr_components | params_created


def single_dose(species, compartment, dose):
    """
    Generate an expression for a sigmoidal Emax model for effect of species in a compartment.

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment from which the species is being lost.
    emax : Parameters or number
        Linear elimination rate. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    ec50 : Parameter or number

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally a Parameter if kel was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        elimination(Drug, Central, 1e-4)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> elimination(Drug, Central 1e-6) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('degrade_B', B() >> None, degrade_B_k),
         Parameter('degrade_B_k', 1e-06),
         ])

    """

    if isinstance(species, Monomer):
        monomer_name = species.name
    else:
        monomer_name = species.monomer.name
    comp_name = compartment.name

    species = _check_for_monomer(species, compartment)
    params_created = ComponentSet()
    Dose = dose
    Vcomp = compartment.size
    if not isinstance(Dose, Parameter):
        Dose = Parameter("dose_{0}_{1}".format(monomer_name, comp_name), dose)
        dose_expr = Expression("expr_{0}_{1}_0".format(monomer_name, comp_name), dose / Vcomp)
        params_created.add(Dose)
        params_created.add(dose_expr)
    else:
        dose_expr = Parameter("expr_{0}_{1}_0".format(monomer_name, comp_name), Dose / Vcomp)
        params_created.add(dose_expr) 

    initial = Initial(species, dose_expr)

    return params_created #| ComponentSet([initial])