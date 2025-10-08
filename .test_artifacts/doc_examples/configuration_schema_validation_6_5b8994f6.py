# Example from: docs\configuration_schema_validation.md
# Index: 6
# Runnable: False
# Hash: 5b8994f6

class HILConfig(BaseModel):
    """Hardware-in-the-loop configuration schema."""
    enabled: bool = Field(False, description="Enable HIL communication")
    plant_address: str = Field(..., description="Plant server IP address")
    plant_port: int = Field(..., ge=1024, le=65535, description="Plant server port")
    controller_port: int = Field(..., ge=1024, le=65535, description="Controller client port")
    timeout: float = Field(..., gt=0.1, le=10.0, description="Communication timeout (s)")

    @validator('plant_address')
    def validate_ip_address(cls, v):
        """Validate IP address format."""
        import ipaddress
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValueError(f"Invalid IP address format: {v}")
        return v

    @validator('controller_port')
    def validate_port_conflict(cls, v, values):
        """Validate no port conflicts."""
        if 'plant_port' in values and v == values['plant_port']:
            raise ValueError("Controller and plant ports must be different")
        return v

    @validator('timeout')
    def validate_realtime_constraint(cls, v, values):
        """Validate real-time communication constraints."""
        if 'dt' in values:  # If simulation dt is available
            dt = values.get('dt', 0.01)
            if v > dt / 2:
                raise ValueError("Communication timeout too large for real-time operation")
        return v