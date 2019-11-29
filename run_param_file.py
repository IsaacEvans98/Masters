"""
Parameter file for use in the Dedalus 2D anelastic convection script.
"""

import numpy as np

Lx, Lz = 2, 1                       # Domain size
Nx, Nz = 128, 64                    # Number of
Pr = 1.                             # Prandtl number
Pm = 1.                             # Magnetic Prandtl number
Ra = 8e5                       # Rayleigh number
Np = 0
Ta = 5e6
latitude = np.pi / 4                  # Number of density scale heights
m = 1.5                             # Polytropic index
theta = 1 - np.exp(-Np/m)           # Dimensionaless inverse T scale height
Roc = np.sqrt((Ra)/(Ta*Pr))


initial_timestep = 2e-5                 # Initial timestep
max_dt = 1e-4                         # max dt

snapshot_freq = 1.5e-4              # Frequency snapshot files are outputted
analysis_freq = 1.5e-5              # Frequency analysis files are outputted

end_sim_time = 2.                   # Stop time in simulations units
end_wall_time = np.inf              # Stop time in wall time
end_iterations = np.inf             # Stop time in iterations
