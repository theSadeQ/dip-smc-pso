# Example from: docs\factory\production_deployment_guide.md
# Index: 4
# Runnable: False
# Hash: 2a7d4c6c

def blue_green_deployment():
    """Blue-green deployment strategy."""

    print("Starting blue-green deployment")

    # Setup green environment
    green_env = setup_green_environment()

    # Deploy to green environment
    deploy_to_green(green_env)

    # Smoke test green environment
    if not smoke_test_green(green_env):
        cleanup_green(green_env)
        raise RuntimeError("Green environment smoke test failed")

    # Switch traffic to green
    switch_traffic_to_green(green_env)

    # Monitor for issues
    monitor_duration = 600  # 10 minutes
    if monitor_green_environment(monitor_duration):
        # Success - cleanup blue environment
        cleanup_blue_environment()
        print("✅ Blue-green deployment successful")
    else:
        # Issues detected - rollback to blue
        switch_traffic_to_blue()
        cleanup_green(green_env)
        raise RuntimeError("Green environment issues detected, rolled back")

# Run blue-green deployment
blue_green_deployment()