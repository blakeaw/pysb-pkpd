import pysb
from pysb.simulator import ScipyOdeSimulator
import numpy as np


def simulate(
    model: pysb.Model,
    tspan: np.ndarray,
    param_values: None | np.ndarray | list[np.ndarray] = None,
    initials: None | np.ndarray | list[np.ndarray] = None,
    nprocs: int = 1,
) -> np.ndarray:
    """Simulate the given model using the ScipyOdeSimulator.

    This function abstracts setting up and running a simulation of the model using
    the ScipyOdeSimulator with the lsoda integrator. It returns the corresponding model
    trajectory.

    Args:
        model: The input PySB model to simulate.
        tspan: The time span to simulate the model over.
        param_values: Optional specification of parameters to use when
            simulating the model. If None, the nominal/default model parameters
            will be used. The input can be None, a single parameter vector, or
            a list of parameter vectors that will each be simulated.
        initials: Optional specification of initial concentrations to use when
            simulating the model. If None, the nominal/default model values
            will be used. The input can be None, a single vector, or
            a list of vectors that will each be simulated.

    Returns:
        The PySB model simulation trajectory as a structured NumPy array.
    """

    simulator = ScipyOdeSimulator(
        model,
        tspan=tspan,
        integrator="lsoda",
    )
    simulation_result = simulator.run(
        param_values=param_values, initials=initials, num_processors=nprocs
    )
    simulation_trajectory = simulation_result.all
    return simulation_trajectory
