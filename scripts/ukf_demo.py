# Example of an Unscented Kalman Filter
# applied to a nonlinear function
# For futher reference and examples see:
#   * Section on Kalman Filters in PML vol2 book
#   * Nonlinear Dynamics and Chaos - Steven Strogatz
# Author: Gerardo Durán-Martín (@gerdm)

import dynamical_systems_lib as ds
import matplotlib.pyplot as plt 
import pyprobml_utils as pml
import jax.numpy as jnp
from jax import random

plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False

def fz(x, dt):
    return x + dt * jnp.array([jnp.sin(x[1]), jnp.cos(x[0])])
def fx(x): return x


dt = 0.4
nsteps = 100
x0 = jnp.array([1.5, 0.0])

# State noise
Qt = jnp.eye(2) * 0.001
# Observed noise
Rt = jnp.eye(2) * 0.05
alpha, beta, kappa = 1, 0, 2

key = random.PRNGKey(314)
ukf = ds.UnscentedKalmanFilter(lambda x: fz(x, dt), fx, Qt, Rt, alpha, beta, kappa)
sample_state, sample_obs = ukf.sample(key, x0, nsteps)
mean_hist, Sigma_hist = ukf.filter(sample_obs)

fig, ax = plt.subplots()
ax.plot(*sample_state.T, label="state space")
ax.scatter(*sample_obs.T, s=60, c="tab:green", marker="+")
ax.scatter(*sample_state[0], c="black", zorder=3)
ax.legend()
ax.set_title("State Space")
plt.axis("equal")
pml.savefig("ukf-state-space.pdf")

fig, ax = plt.subplots()
ax.scatter(*sample_obs.T, marker="+", color="tab:green")
ax.plot(*mean_hist.T, c="tab:orange", label="filtered")
ax.scatter(*mean_hist[0], c="black", zorder=3)
for mut, Vt in zip(mean_hist[::4], Sigma_hist[::4]):
    pml.plot_ellipse(Vt, mut, ax, plot_center=False, alpha=0.9, zorder=3)
plt.legend()
ax.set_title("Approximate Space")
plt.axis("equal")
pml.savefig("ukf-filtered-space.pdf")

plt.show()