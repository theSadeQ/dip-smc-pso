# Example from: docs\configuration_schema_validation.md
# Index: 1
# Runnable: False
# Hash: 6abd46ef

# example-metadata:
# runnable: false

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
import numpy as np

class SystemConfig(BaseModel):
    """System-level configuration schema."""
    version: str = Field(..., regex=r"^\d+\.\d+\.\d+$", description="Semantic version")
    environment: str = Field(..., regex=r"^(development|testing|staging|production)$")
    logging_level: str = Field("INFO", regex=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    @validator('version')
    def validate_version_compatibility(cls, v):
        """Validate version compatibility."""
        major, minor, patch = map(int, v.split('.'))
        if major < 2:
            raise ValueError("Version 2.0+ required for production deployment")
        return v