# Phase 3 Rollback Procedures

## Scenario 1 - Accessibility Score <95
1. Re-run Lighthouse locally to confirm failure.
2. Revert latest accessibility-related commit (`git revert <sha>`).
3. Restore previous CSS bundle from `docs/_static/custom.css.bak`.
4. Capture new axe/Lighthouse reports and update `validation/lighthouse/`.

## Scenario 2 - Token Regression
1. Reset token overrides to tag `phase3-wave0-complete`.
2. Replace `design_tokens_v2.json` with last known good version.
3. Rebuild Sphinx assets, verify via `tooling_validation.md` checklist.
4. Notify stakeholders in `DECISION_LOG.md` and enqueue fix for Wave 1.

## Scenario 3 - Streamlit Theme Breakage
1. Toggle `ENABLE_DIP_THEME=0` in Streamlit config.
2. Roll back `streamlit_theme` directory to prior commit.
3. Execute smoke tests documented in `VALIDATION_PROCEDURES.md`.
4. Capture screenshots for regression evidence in `validation/manual/`.

## Scenario 4 - Screenshot Automation Failure
1. Switch Playwright script to `--debug` mode and rerun.
2. If still failing, capture PNG manually via browser dev tools.
3. Update `baselines/INDEX.md` with manual capture status.
4. File decision entry noting deviation from automation.

## Scenario 5 - Percy/Lighthouse Infrastructure Outage
1. Pause current wave and inform PM (Slack + `DECISION_LOG.md`).
2. Run manual Lighthouse CLI and axe CLI, store results under `validation/`.
3. Resume automated runs once infrastructure restored, compare diffs.
4. Tag backlog tickets impacted and adjust Wave timeline if delay >4 hrs.

