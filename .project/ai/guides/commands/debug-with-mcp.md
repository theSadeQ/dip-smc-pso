---
description: Start integrated multi-server debugging session for control systems
tags: [debugging, mcp, workflow, control-systems, pso]
---

# MCP Integrated Debugging (DIP-SMC-PSO)

I'll help you debug control systems, optimization, and simulation issues using multiple MCP servers.

## What issue are you debugging?

Please describe the problem, and I'll create a systematic debugging plan using:

- **📁 Filesystem Server** for code and log analysis
- **🐙 GitHub Server** for issue tracking and history
- **🎭 Puppeteer Server** for Streamlit dashboard testing
- **🧠 Sequential Thinking** for methodical analysis

## Common Debugging Workflows

1. **PSO Optimization Issues**
   - Search GitHub issues for similar convergence problems
   - Analyze PSO logs with filesystem server
   - Review cost function implementation
   - Check parameter bounds validity
   - Examine swarm behavior patterns
   - Create detailed convergence report

2. **Controller Instability**
   - Review controller implementation (SMC/MPC/Adaptive)
   - Analyze Lyapunov function validity
   - Check gain bounds and tuning
   - Examine simulation logs for divergence
   - Test with reduced gains
   - Generate stability analysis report

3. **Numerical Errors (LinAlgError, Singular Matrix)**
   - Locate error in logs and stack trace
   - Review matrix operations in dynamics model
   - Check condition numbers and ill-conditioning
   - Analyze regularization strategies
   - Test with numerical stability fixes
   - Document solution approach

4. **Test Failures**
   - Search GitHub issues for test history
   - Analyze pytest logs with filesystem server
   - Review failing test implementation
   - Check for environment-specific issues
   - Run isolated test with debugging
   - Create bug report with reproduction steps

5. **Streamlit Dashboard Issues**
   - Test dashboard with Puppeteer server
   - Check console errors in browser
   - Verify plot rendering
   - Test simulation execution flow
   - Capture screenshots of errors
   - Document UI/UX issues

What would you like to debug?
