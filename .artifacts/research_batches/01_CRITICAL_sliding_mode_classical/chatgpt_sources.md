















CLAIM 1 (ID: FORMAL-THEOREM-016):

- Citation: Shtessel et al. (2013)
- BibTeX Key: shtessel2013sliding
- DOI: 10.1007/978-0-8176-4893-0_1
- Type: book
- Note: Chapter 1 of Shtessel’s textbook introduces the sliding variable (σ=x_2+c,x_1) with (c>0).  The authors derive the desired dynamics ( \dot{x}_1 + c x_1 =0) and solve it to get (x_1(t)=x_1(0)e^{-ct}) and (x_2(t)=-c,x_1(0)e^{-ct}), noting that both states converge exponentially at a rate (c).  They explain that driving (σ) to zero in finite time produces these exponential dynamics with convergence rates determined by the positive parameter (c).

CLAIM 2 (ID: FORMAL-THEOREM-019):

- Citation: Slotine & Li (1991)
- BibTeX Key: slotine1991applied
- DOI: N/A
- Type: book
- Note: In the sliding‑mode chapter of *Applied Nonlinear Control*, Slotine and Li derive the reaching condition ( \tfrac{\mathrm{d}}{\mathrm{d}t}\tfrac{1}{2}s^2 \le -\eta ) with (\eta>0).  Integrating this inequality shows that the trajectory reaches the sliding surface in finite time bounded by (t_{\mathrm{reach}} \le |s(0)|/\eta).  This provides a formal bound on the time required to reach the sliding surface under the reaching condition.

CLAIM 3 (ID: FORMAL-THEOREM-020):

- Citation: Shtessel et al. (2013)
- BibTeX Key: shtessel2013sliding
- DOI: 10.1007/978-0-8176-4893-0_1
- Type: book
- Note: Same source as Claim 1. In the same chapter, Shtessel and co‑authors propose a sliding‑mode control law (u=-c,x_2-\varphi,\mathrm{sign}(σ)) and show that the control gain (\varphi) must exceed the disturbance bound (L) by choosing (\varphi = L + \alpha\sqrt{2}).  They remark that the first term (L) compensates for the bounded uncertainty while the additional term (\alpha\sqrt{2}) determines the reaching time; a larger (\alpha) yields a shorter finite‑time convergence to the sliding surface.  This classical result demonstrates that choosing the switching gain greater than the uncertainty bound guarantees finite‑time convergence.

CLAIM 4 (ID: FORMAL-THEOREM-023):

- Citation: Slotine & Li (1991)
- BibTeX Key: slotine1991applied
- DOI: N/A
- Type: book
- Note: Same source as Claim 2. To mitigate chattering, Slotine and Li introduce a boundary layer of thickness (\phi) around the sliding surface and replace the discontinuous sign function with (s/\phi) within this layer.  They prove that this boundary‑layer method makes the layer attractive and ensures that the tracking error components satisfy (|x_i(t)| \le 2\lambda,\varepsilon) for (i=0,\dots,n-1), where (\varepsilon) is proportional to (\phi).  Thus, the tracking error is ultimately bounded by a constant determined by the boundary‑layer width, providing a practical bound on the steady‑state error.



# Sources Used for Sliding Mode Control Claims

This file lists the primary documents used to support the sliding‑mode control claims and provides accessible addresses for each source.  Because some of the books are copyrighted, only the specific sections referenced in the research are reproduced here.  For full context, refer to the original documents at the provided links.

## 1. Slotine & Li (1991) – *Applied Nonlinear Control*

- **Accessible address:** [https://vtechworks.lib.vt.edu/bitstream/handle/10919/30598/CHAP4_DOC.pdf](https://vtechworks.lib.vt.edu/bitstream/handle/10919/30598/CHAP4_DOC.pdf)
- **Context:** Chapter 5 introduces sliding‑mode control for robust tracking.  The authors derive the reaching condition and show that the reaching time is bounded by \(t_{\text{reach}} \le |s(0)|/\eta\).  They also discuss the use of a boundary layer to mitigate chattering, which leads to a guaranteed bound on the tracking error.
- **Excerpt:**
  - Finite‑time reachability: “Integrating (5.4) between \(t=0\) and \(t_{\text{reach}}\) leads to \(t_{\text{reach}} \le s(t=0)/\eta\) … The state trajectory reaches the surface in a finite time and then slides along the surface towards the desired state exponentially”【617493263938330†L268-L284】.
  - Gain condition: “By choosing \(k(x,t)\) large enough, such as \(k(x,t)=F(x,t)+\eta\), we ensure the sliding condition”【617493263938330†L439-L470】.
  - Boundary layer: “Inside the boundary layer the sign function is replaced by \(s/\phi\).  This leads to tracking within a guaranteed precision; for all trajectories starting in the layer, \(|x_i(t)| \le 2\lambda\varepsilon\) for \(i=0,\dots,n-1\)”【617493263938330†L618-L649】.

## 2. Shtessel et al. (2013) – *Sliding Mode Control and Observation*

- **Accessible address:** DOI link [https://doi.org/10.1007/978-0-8176-4893-0_1](https://doi.org/10.1007/978-0-8176-4893-0_1)
- **Context:** The introductory chapter provides an intuitive overview of sliding‑mode control using a second‑order system example.  It derives the sliding surface \(\sigma = x_2 + c x_1\) with \(c>0\) and shows that the closed‑loop dynamics \(\dot{x}_1 + c x_1 =0\) have exponential solutions with rate \(c\).  A Lyapunov analysis yields a finite‑time bound on the reaching phase and a control gain that compensates the disturbance bound.
- **Excerpt:**
  - Exponential dynamics: “The homogeneous equation \(\dot{x}_1 + c x_1 = 0\) with \(c>0\) has the solution \(x_1(t)=x_1(0)e^{-c t}\) and \(x_2(t)=-c x_1(0)e^{-c t}\); both converge to zero”【213856928523750†L96-L105】.
  - Sliding variable: “Define \(\sigma=x_2 + c x_1\) with \(c>0\). Driving \(\sigma\) to zero in finite time gives asymptotic convergence of \(x_1\) and \(x_2\) at the exponential rate dictated by \(c\)”【213856928523750†L112-L121】.
  - Finite‑time bound: “Under the Lyapunov inequality \(\dot{V} \le -\alpha V^{1/2}\), the reaching time satisfies \(t_r \le 2 V^{1/2}(0)/\alpha\)”【213856928523750†L155-L163】.
  - Gain selection: “The control gain is \(\varphi = L + \alpha\sqrt{2}\); the first term cancels the disturbance bound and the second term determines the reaching time”【213856928523750†L193-L226】.

