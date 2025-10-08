# Example from: docs\CLAUDE.md
# Index: 19
# Runnable: False
# Hash: fe388afc

# example-metadata:
# runnable: false

for i in range(10000):
    controller = AdaptiveSMC(gains=candidates[i], ...)
    fitness[i] = evaluate(controller)

    if i % 100 == 99:
        controller.cleanup()
        del controller
        gc.collect()