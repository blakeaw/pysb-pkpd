from pysb import Monomer, Parameter, Expression, Observable, Compartment, Initial
from pysb.core import ComponentSet, as_complex_pattern, MonomerPattern, ComplexPattern
import pysb.macros

__all__ = [
    "two_compartments",
    "three_compartments",
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
    Generate compartments for a two-compartment model. 

    Parameters
    ----------
    c1_name : string
        The name of compartment 1. If a number is passed a Parameter will 
         be created and given as the size for Compartment 1. Default=CENTRAL.
    c1_size : Parameter or number
        The volume of compartment 1. If a number is passed a Parameter will 
         be created and given as the size for Compartment 1. Default=1.0
    c2_name : string
        The name of compartment 2.  Default=PERIPHERAL.
    c2_size : Parameter or number
        The volume of compartment 2. If a number is passed a Parameter will 
         be created and given as the size for Compartment 2. Default=1.0

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the two compartments
        and optionally two Parameters if c1_size and c2_size were 
        given as numbers.

    Examples
    --------
    Use the default compartment names but adjust the size::

        Model()
        two_comapartments(c1_size=30., c2_size=20.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> two_compartments() # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
        Compartment(name='CENTRAL', parent=None, dimension=3, size=V_CENTRAL),
        Compartment(name='PERIPHERAL', parent=None, dimension=3, size=V_PERIPHERAL),
        Parameter('V_CENTRAL', 1.0),
        Parameter('V_PERIPHERAL', 1.0),
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
    Generate compartments for a three-compartment model. 

    Parameters
    ----------
    c1_name : string
        The name of compartment 1. Default=CENTRAL.
    c1_size : Parameter or number
        The volume of compartment 1. If a number is passed a Parameter will 
         be created and given as the size for Compartment 1. Default=1.0
    c2_name : string
        The name of compartment 2. If a number is passed a Parameter will 
         be created and given as the size for Compartment 2. Default=PERIPHERAL.
    c2_size : Parameter or number
        The volume of compartment 2. Default=1.0
    c3_name : string
        The name of compartment 2. If a number is passed a Parameter will 
         be created and given as the size for Compartment 3. Default=DEEPPERIPHERAL.
    c3_size : Parameter or number
        The volume of compartment 3. Default=1.0
    Returns
    -------
    components : ComponentSet
        The generated components. Contains the three compartments
        and optionally three Parameters if c1_size, c2_size and
        c3_size were given as numbers.

    Examples
    --------
    Use the default compartments:

        Model()
        three_comapartments()

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> two_compartments() # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
        Compartment(name='CENTRAL', parent=None, dimension=3, size=V_CENTRAL),
        Compartment(name='PERIPHERAL', parent=None, dimension=3, size=V_PERIPHERAL),
        Compartment(name='DEEPPERIPHERAL', parent=None, dimension=3, size=V_DEEPPERIPHERAL),
        Parameter('V_CENTRAL', 1.0),
        Parameter('V_PERIPHERAL', 1.0),
        Parameter('V_DEEPPERIPHERAL', 1.0),
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
        >>> eliminate(Drug, CENTRAL, 1e-3) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
        Rule('eliminate_Drug_CENTRAL', Drug() ** CENTRAL >> None, eliminate_Drug_CENTRAL_k),
        Parameter('eliminate_Drug_CENTRAL_k', 0.001),
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
    vmax : Parameter or number
        The maximum velocity (or limiting rate) for the reaction. If a Parameter
        is passed, it will be used directly in the generated Rule. If a number
        is passed, a Parameter will be created with an automatically generated
        name based on the names and site states of the components of `species`
        and this parameter will be included at
        the end of the returned component list.
    km : Parameter or number
        The Michaelis constant  for the reaction. If a Parameter
        is passed, it will be used directly in the generated Rule. If a number
        is passed, a Parameter will be created with an automatically generated
        name based on the names and site states of the components of `species`
        and this parameter will be included at
        the end of the returned component list.
    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional elimination Rule
        and optionally two Parameters if vmax and km were given as numbers.

    Examples
    --------
    Non-linear elimination of Drug in the CENTRAL compartment::

        Model()
        Compartment('CENTRAL')
        Monomer('Drug')
        eliminate_mm(Drug, Central, 1., 15.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> eliminate_mm(Drug, CENTRAL, 1., 15.) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('eliminate_mm_Drug_CENTRAL', Drug() ** CENTRAL >> None, k_expr_Drug_CENTRAL),
         Parameter('Vmax_Drug_CENTRAL', 1.0),
         Parameter('Km_Drug_CENTRAL', 15.0),
         Observable('_obs_expr_Drug_CENTRAL', Drug() ** CENTRAL),
         Expression('k_expr_Drug_CENTRAL', Vmax_Drug_CENTRAL/(_obs_expr_Drug_CENTRAL + Km_Drug_CENTRAL)),
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
    cl : Parameters or number
        Clearance rate in volume/time. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the unidirectional clearance Rule,
        an Expression for the conversion of the clearance rate to a unidirectional 
        rate constant, and optionally a Parameter if cl was given as a number.

    Examples
    --------
    Linear elimination all Drug in the Central compartment::

        Model()
        Compartment('CENTRAL')
        Monomer('Drug')
        clearace(Drug, CENTRAL, 1.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> clearance(Drug, CENTRAL, 1.) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('clearance_Drug_CENTRAL', Drug() ** CENTRAL >> None, k_CL_expr_Drug_CENTRAL),
         Expression('k_CL_expr_Drug_CENTRAL', CL_Drug_CENTRAL/V_CENTRAL),
         Parameter('CL_Drug_CENTRAL', 1.0),
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
    Generate the unimolecular reversible equilibrium reaction
    to distribute/redistribute the species between the two compartments:
    species ** c1 <-> species ** c2.

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
    Distribution/redistribution of Drug between the CENTRAL and PERIPHERAL compartments::

        Model()
        Monomer('Drug')
        Compartment("CENTRAL")
        Compartment("PERIPHERAL")
        distribute(Drug, CENTRAL, PERIPHERAL, [1, 1])

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment("CENTRAL")
        Compartment(name='CENTRAL', parent=None, dimension=3, size=1.),
        >>> Compartment("PERIPERAL")
        Compartment(name='PERIPHERAL', parent=None, dimension=3, size=1.),        
        >>> distribute(Drug, CENTRAL, PERIPHERAL [1, 1]) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('distribute_Drug_CENTRAL_to_PERIPHERAL', Drug() ** CENTRAL | Drug() ** PERIPHERAL, distribute_Drug_CENTRAL_to_PERIPHERAL_kf, distribute_Drug_CENTRAL_to_PERIPHERAL_kr),
         Parameter('distribute_Drug_CENTRAL_to_PERIPHERAL_kf', 1.0),
         Parameter('distribute_Drug_CENTRAL_to_PERIPHERAL_kr', 1.0),
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
    Generate a unimolecular irreversible reaction to transfer a species from one
    compartment to another:  species ** c1 --> species ** c2.

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
    Transfer drug irreveribly from the Central to Peripheral compartment::

        Model()
        Monomer('Drug')
        Compartment("CENTRAL")
        Compartment("PERIPHERAL")
        transfer(Drug, CENTRAL, PERIPHERAL,  1.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment("CENTRAL")
        Compartment(name='CENTRAL', parent=None, dimension=3, size=1.),
        >>> Compartment("PERIPERAL")
        Compartment(name='PERIPHERAL', parent=None, dimension=3, size=1.),        
        >>> transfer(Drug, CENTRAL, PERIPHERAL, 1.) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Rule('transfer_Drug_CENTRAL_to_PERIPHERAL', Drug() ** CENTRAL >> Drug() ** PERIPHERAL, transfer_Drug_CENTRAL_to_PERIPHERAL_k),
         Parameter('transfer_Drug_CENTRAL_to_PERIPHERAL_k', 1.0),
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
    Generate an expression for Emax model for effect of species in a compartment:
        emax * [species ** compartment] / ( [species ** compartment] + ec50 )

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment for which the effect is being measured.
    emax : Parameter or number
        Maximum effect value. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    ec50 : Parameter or number
        The 50% effect concentration. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the Emax expression, a corresponding 
        observable for the species concentration, and optionally up to two
        Parameters if emax and ec50 were given as numbers.

    Examples
    --------
    Emax effect for Drug in the Central compartment::

        Model()
        Compartment('Central')
        Monomer('Drug')
        emax(Drug, Central, 2.4, 100.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> emax(Drug, Central 2.4, 100.) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Observable('_obs_emax_expr_Drug_CENTRAL', Drug() ** CENTRAL),
         Expression('Emax_expr_Drug_CENTRAL', _obs_emax_expr_Drug_CENTRAL*Emax_Drug_CENTRAL/(_obs_emax_expr_Drug_CENTRAL + EC50_Drug_CENTRAL)),
         Parameter('Emax_Drug_CENTRAL', 2.4),
         Parameter('EC50_Drug_CENTRAL', 100.0),
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
    Generate an expression for sigmoidal Emax model for effect of species in a compartment:
        emax * [species ** compartment] ** n / ( [species ** compartment] ** n + ec50 ** n)

    Note that `species` is not required to be "concrete".

    Parameters
    ----------
    species : Monomer, MonomerPattern or ComplexPattern
        The species undergoing linear elimination. If a Monomer, sites are considered
        as unbound and in their default state. If a pattern, must be
        concrete.
    compartment : Compartment
        The compartment for which the effect is being measured.
    emax : Parameter or number
        Maximum effect value. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    ec50 : Parameter or number
        The 50% effect concentration. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.
    n : Parameter or number
        The Hill coefficient. If a Parameter is passed, it will be used directly in
        the generated Rule. If a number is passed, a Parameter will be created
        with an automatically generated name based on the names and site states
        of the components of `species` and this parameter will be included at
        the end of the returned component list.        

    Returns
    -------
    components : ComponentSet
        The generated components. Contains the Emax expression, a corresponding 
        observable for the species concentration, and optionally up to three
        Parameters if emax, ec50, and n were given as numbers.

    Examples
    --------
    Emax effect for Drug in the Central compartment::

        Model()
        Compartment('Peripheral')
        Monomer('Drug')
        sigmoidal_emax(Drug, Peripheral, 4.4, 50.)

    Execution::

        >>> Model() # doctest:+ELLIPSIS
        <Model '_interactive_' ...>
        >>> Monomer('Drug')
        Monomer('Drug')
        >>> Compartment('CENTRAL', size=30.)
        Compartment(name='CENTRAL', parent=None, dimension=3, size=30.)
        >>> emax(Drug, Central 2.4, 100.) # doctest:+NORMALIZE_WHITESPACE
        ComponentSet([
         Observable('_obs_emax_expr_Drug_CENTRAL', Drug() ** CENTRAL),
         Expression('Emax_expr_Drug_CENTRAL', _obs_emax_expr_Drug_CENTRAL*Emax_Drug_CENTRAL/(_obs_emax_expr_Drug_CENTRAL + EC50_Drug_CENTRAL)),
         Parameter('Emax_Drug_CENTRAL', 2.4),
         Parameter('EC50_Drug_CENTRAL', 100.0),
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
        dose_expr = Expression("expr_{0}_{1}_0".format(monomer_name, comp_name), Dose / Vcomp)
        params_created.add(Dose)
        params_created.add(dose_expr)
    else:
        dose_expr = Parameter("expr_{0}_{1}_0".format(monomer_name, comp_name), Dose / Vcomp)
        params_created.add(dose_expr) 

    initial = Initial(species, dose_expr)

    return params_created #| ComponentSet([initial])