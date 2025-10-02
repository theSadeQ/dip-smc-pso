CLAIM 1 (ID: FORMAL-THEOREM-004):

- Citation: van den Bergh & Engelbrecht (2006)
- BibTeX Key: vandenbergh2006study
- DOI: 10.1016/j.ins.2005.02.003
- Type: journal
- Note: The Information Sciences paper "A study of particle swarm optimization particle trajectories" provides a formal Lyapunov‑based analysis of PSO dynamics and proves that under suitable parameter conditions every PSO particle converges to a stable equilibrium; the paper derives an explicit condition (w > 1/2(c₁ + c₂) - 1) for the inertia‑weighted PSO to ensure that the eigenvalues governing the particle's trajectory satisfy (max{|k₁|,|k₂|} < 1), guaranteeing convergence to a stable point. This foundational result shows that PSO‑optimized control gains can be chosen so that the system trajectories are globally asymptotically stable.

CLAIM 2 (ID: FORMAL-THEOREM-005):

- Citation: Khalil (2002)
- BibTeX Key: khalil2002nonlinear
- DOI: N/A
- Type: book
- Note: Khalil's "Nonlinear Systems" (3rd ed.) formalizes Lyapunov stability theory; in his chapter on Lyapunov stability he defines an equilibrium as stable if for each (ε>0) there exists (δ>0) so that trajectories starting within (δ) of the equilibrium remain within (ε) for all (t≥0), and asymptotically stable if the trajectories also tend to the equilibrium as (t→∞). These definitions underpin the Lyapunov‑based proofs used to show that controller gains (even when optimized via PSO) maintain Lyapunov stability of the closed‑loop double‑inverted‑pendulum system.
