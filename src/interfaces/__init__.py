#======================================================================================\\\
#============================= src/interfaces/__init__.py =============================\\\
#======================================================================================\\\

"""
Interfaces framework for control engineering applications.
This module provides interface systems for network communication, hardware abstraction,
HIL systems, data exchange, and monitoring capabilities designed for real-time
control systems and scientific computing applications.
"""

# Hardware-in-the-Loop (HIL) System - Complete and tested
from .hil import (
    # Enhanced HIL System
    EnhancedHILSystem, HILConfig, HILMode, TestScenario,
    # Real-time capabilities
    RealTimeScheduler, TimingConstraints, DeadlineMissHandler,
    # Fault injection
    FaultInjector, FaultType, FaultScenario,
    # Test automation
    HILTestFramework, TestSuite, TestCase,
    # Data logging
    HILDataLogger, LoggingConfig,
    # Simulation bridge
    SimulationBridge, ModelInterface,
    # Legacy compatibility
    HILControllerClient, PlantServer, run_client
)

# Data Exchange and Serialization - Complete framework
from .data_exchange import (
    # Core serialization
    SerializationFormat, SerializerInterface, SerializationError,
    JSONSerializer, MessagePackSerializer, PickleSerializer,
    BinarySerializer, CompressionSerializer,
    # Data types and schemas
    DataPacket,
    DataSchema, SchemaValidator, ValidationError,
    # Factory and performance
    SerializerFactory, StreamingSerializer
)

# Monitoring and Diagnostics - Complete system
from .monitoring import (
    # Health monitoring
    HealthStatus, HealthCheck, ComponentHealth,
    HealthMonitor, SystemHealthMonitor,
    # Metrics collection
    MetricType, Metric, MetricsCollector,
    PerformanceMonitor, SystemMetricsCollector,
    # Diagnostics and alerting
    DiagnosticEngine, DiagnosticResult,
    AlertManager, Alert, AlertRule, AlertLevel,
    EmailNotificationHandler, LogNotificationHandler,
    # Dashboard
    DashboardServer, MetricSeries, ChartConfig
)

# Hardware Abstraction - Basic hardware interfaces
from .hardware import (
    # Device management
    DeviceDriver, DeviceStatus, BaseDevice,
    DeviceManager, HardwareInterfaceFactory,
    # Drivers and interfaces
    SerialDevice, DAQInterface, SensorInterface,
    ActuatorInterface, AnalogSensor, DigitalSensor
)

# Network Interfaces - Basic networking
from .network import (
    # Core interfaces
    TCPInterface, UDPInterface, WebSocketInterface,
    HTTPInterface, NetworkInterfaceFactory,
    # Message handling
    MessageQueueInterface, ZeroMQInterface, RabbitMQInterface,
    # Servers and clients
    TCPServer, UDPServer, WebSocketServer
)

# Core interfaces and protocols
from .core import (
    CommunicationProtocol, MessageProtocol, ConnectionProtocol,
    InterfaceType, Message, ConnectionInfo, InterfaceConfig
)

__version__ = "1.0.0"

__all__ = [
    # Hardware-in-the-Loop (HIL) System
    'EnhancedHILSystem', 'HILConfig', 'HILMode', 'TestScenario',
    'RealTimeScheduler', 'TimingConstraints', 'DeadlineMissHandler',
    'FaultInjector', 'FaultType', 'FaultScenario',
    'HILTestFramework', 'TestSuite', 'TestCase',
    'HILDataLogger', 'LoggingConfig',
    'SimulationBridge', 'ModelInterface',
    'HILControllerClient', 'PlantServer', 'run_client',

    # Data Exchange and Serialization
    'SerializationFormat', 'SerializerInterface', 'SerializationError',
    'JSONSerializer', 'MessagePackSerializer', 'PickleSerializer',
    'BinarySerializer', 'CompressionSerializer',
    'DataPacket',
    'DataSchema', 'SchemaValidator', 'ValidationError',
    'SerializerFactory', 'StreamingSerializer',

    # Monitoring and Diagnostics
    'HealthStatus', 'HealthCheck', 'ComponentHealth',
    'HealthMonitor', 'SystemHealthMonitor',
    'MetricType', 'Metric', 'MetricsCollector',
    'PerformanceMonitor', 'SystemMetricsCollector',
    'DiagnosticEngine', 'DiagnosticResult', 'TroubleshootingAssistant',
    'AlertManager', 'Alert', 'AlertRule', 'AlertLevel',
    'EmailNotificationHandler', 'LogNotificationHandler',
    'DashboardServer', 'MetricSeries', 'ChartConfig',

    # Hardware Abstraction
    'DeviceDriver', 'DeviceStatus', 'BaseDevice',
    'DeviceManager', 'HardwareInterfaceFactory',
    'SerialDevice', 'DAQInterface', 'SensorInterface',
    'ActuatorInterface', 'AnalogSensor', 'DigitalSensor',

    # Network Interfaces
    'TCPInterface', 'UDPInterface', 'WebSocketInterface',
    'HTTPInterface', 'NetworkInterfaceFactory',
    'MessageQueueInterface', 'ZeroMQInterface', 'RabbitMQInterface',
    'TCPServer', 'UDPServer', 'WebSocketServer',

    # Core interfaces
    'CommunicationProtocol', 'MessageProtocol', 'ConnectionProtocol',
    'InterfaceType', 'Message', 'ConnectionInfo', 'InterfaceConfig',
]


def get_framework_info():
    """Get information about the available interfaces framework components."""
    return {
        "version": __version__,
        "modules": {
            "hil": "Hardware-in-the-Loop system with real-time capabilities",
            "data_exchange": "Data serialization and exchange framework",
            "monitoring": "System monitoring, diagnostics, and alerting",
            "hardware": "Hardware abstraction layer with device drivers",
            "network": "Network interfaces for TCP/UDP/WebSocket communication",
            "core": "Core interface protocols and data types"
        },
        "features": [
            "Hardware-in-the-Loop testing framework",
            "Multi-format data serialization",
            "Real-time system monitoring",
            "Hardware device abstraction",
            "Network communication interfaces",
            "Performance optimization",
            "Scientific computing integration"
        ],
        "total_components": len(__all__)
    }


def create_basic_interfaces_manager():
    """Create a basic manager for core interface components."""

    class BasicInterfacesManager:
        """Basic manager for interface framework components."""

        def __init__(self):
            self.hil_system = None
            self.monitoring_system = None
            self.hardware_manager = None

        def initialize_hil(self, config=None):
            """Initialize HIL system."""
            if config:
                self.hil_system = EnhancedHILSystem(config)
            return self.hil_system

        def initialize_monitoring(self):
            """Initialize monitoring system."""
            self.monitoring_system = SystemHealthMonitor()
            return self.monitoring_system

        def initialize_hardware(self):
            """Initialize hardware manager."""
            self.hardware_manager = HardwareManager()
            return self.hardware_manager

        def get_status(self):
            """Get status of initialized components."""
            return {
                "hil_active": self.hil_system is not None,
                "monitoring_active": self.monitoring_system is not None,
                "hardware_active": self.hardware_manager is not None
            }

    return BasicInterfacesManager()


# Convenience factory functions
def create_hil_system(config=None):
    """Create and configure a HIL system."""
    if config:
        return EnhancedHILSystem(config)
    return EnhancedHILSystem()


def create_data_serializer(format_type="json"):
    """Create a data serializer for the specified format."""
    return SerializerFactory.create_serializer(format_type)


def create_health_monitor():
    """Create a system health monitor."""
    return SystemHealthMonitor()


def create_hardware_manager():
    """Create a hardware device manager."""
    return HardwareManager()