import numpy as np
from pysb.pkpd.pk_models import twocomp
from pysb.pkpd import simulate


def test_simulate():
    tspan = np.arange(10)
    sim_traj = simulate(twocomp, tspan)
    assert len(sim_traj) == 10
    assert len(sim_traj[0]) == 2


if __name__ == "__main__":
    test_simulate()
