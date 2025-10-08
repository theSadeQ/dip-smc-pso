# Example from: docs\workflows\complete_integration_guide.md
# Index: 15
# Runnable: False
# Hash: 757cfe23

# scripts/deploy_production.py
import argparse
import logging
from src.production import ProductionManager

def deploy_production_system():
    """Deploy production-ready control system."""

    # Set up production logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('production.log'),
            logging.StreamHandler()
        ]
    )

    # Initialize production manager
    manager = ProductionManager(
        config_file='config/production.yaml',
        safety_mode=True,
        monitoring=True
    )

    # Pre-deployment checks
    if not manager.run_pre_deployment_checks():
        logging.error("Pre-deployment checks failed")
        return False

    # Deploy system
    try:
        manager.deploy_system()
        logging.info("Production system deployed successfully")

        # Start monitoring
        manager.start_monitoring()

        # Run production control loop
        manager.run_production_loop()

    except Exception as e:
        logging.error(f"Production deployment failed: {e}")
        manager.emergency_shutdown()
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy production control system')
    parser.add_argument('--config', default='config/production.yaml', help='Production config file')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without actual deployment')
    args = parser.parse_args()

    if args.dry_run:
        print("🧪 Performing dry run...")
        # Validate configuration and check dependencies
        validate_production_config(args.config)
    else:
        print("🚀 Deploying production system...")
        deploy_production_system()