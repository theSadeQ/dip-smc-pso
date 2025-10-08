# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 19
# Runnable: True
# Hash: ea7c5fff

class TestHILIntegration:
    """Integration tests for Hardware-in-the-Loop."""

    @pytest.mark.slow
    def test_hil_plant_server_startup(self):
        """Test HIL plant server can start and accept connections."""
        from src.hil.plant_server import PlantServer
        import threading
        import time

        server = PlantServer(port=5555)

        # Start server in background thread
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()

        time.sleep(1.0)  # Allow server to start

        # Verify server is running
        assert server.is_running()

        # Cleanup
        server.shutdown()

    @pytest.mark.slow
    def test_hil_controller_client_connection(self):
        """Test HIL controller client can connect to plant server."""
        from src.hil.plant_server import PlantServer
        from src.hil.controller_client import ControllerClient
        import threading
        import time

        # Start server
        server = PlantServer(port=5556)
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()
        time.sleep(1.0)

        # Connect client
        client = ControllerClient(host='localhost', port=5556)
        connected = client.connect()

        assert connected

        # Cleanup
        client.disconnect()
        server.shutdown()