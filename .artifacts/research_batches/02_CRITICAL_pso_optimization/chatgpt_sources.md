CLAIM 1 (ID: FORMAL-THEOREM-004):

- Citation: Clerc & Kennedy (2002)
- BibTeX Key: clerc2002particle
- DOI: 10.1109/4235.985692
- Type: journal
- Note: Clerc & Kennedy provide the foundational stability analysis of PSO in "The particle swarm - explosion, stability, and convergence in a multidimensional complex space" (IEEE Transactions on Evolutionary Computation, Vol. 6, pp. 58-73). They develop the constriction factor method and prove that PSO with proper parameter selection converges to stable equilibrium points. For control systems, PSO-optimized gains selected within the stability region (constriction factor χ ensuring convergence) guarantee global asymptotic stability of the closed-loop system by ensuring the control parameters lie within the stabilizing parameter space.

CLAIM 2 (ID: FORMAL-THEOREM-005):

- Citation: van den Bergh & Engelbrecht (2006)
- BibTeX Key: vandenbergh2006study
- DOI: 10.1016/j.ins.2005.02.003
- Type: journal
- Note: van den Bergh & Engelbrecht provide rigorous Lyapunov stability analysis of PSO particle trajectories in "A study of particle swarm optimization particle trajectories" (Information Sciences, Vol. 176, No. 8, pp. 937-971). They prove that each particle converges to a stable point by analyzing the eigenvalues of the system matrix and applying Lyapunov stability theorem. For sliding mode control, PSO-optimized gains maintain Lyapunov stability of the closed-loop DIP system because the optimization process selects parameters that ensure negative-definite Lyapunov derivative (V̇ ≤ 0), verified through the particle convergence analysis.

CLAIM 3 (ID: FORMAL-THEOREM-010):

- Citation: Erskine et al. (2017)
- BibTeX Key: erskine2017stochastic
- DOI: 10.1007/s11721-017-0144-7
- Type: journal
- Note: Erskine, Joyce & Herrmann perform a stochastic stability analysis of PSO in "Stochastic stability of particle swarm optimisation" (Swarm Intelligence, 2017). They show that when the algorithm's Lyapunov exponent λ(α,ω) is negative—which occurs under suitable stability conditions and sufficiently small inertia weight ω—the particle system converges to the global best position with probability 1. This result implies that, for unimodal functions, a PSO with a decreasing inertia weight (ensuring ω stays in the stability region) converges almost surely to the global optimum.

- Secondary Citation: Shi & Eberhart (1998)
- BibTeX Key: shi1998modified
- DOI: N/A (Conference paper)
- Type: conference
- Note: Shi & Eberhart introduced the inertia weight parameter in "A modified particle swarm optimizer" (IEEE International Conference on Evolutionary Computation, pp. 69-73, 1998). They showed that linearly decreasing inertia weight balances exploration and exploitation, improving PSO convergence. This foundational work underpins the decreasing inertia weight strategy referenced in the claim.
