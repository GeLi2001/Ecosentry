from enum import Enum
from pydantic import BaseModel
from typing import Optional


class EnvironmentalIssueType(str, Enum):
    """Enumeration of environmental issues."""
    EMISSION = "emission"
    ILLEGAL_DUMPING = "illegal_dumping"
    DEFORESTATION = "deforestation" 
    WATER_POLLUTION = "water_pollution"
    NOT_QUALIFIED = "not_qualified"


class EnvironmentalIssue(BaseModel):
    """Pydantic model for environmental issues."""
    issue_type: EnvironmentalIssueType
    reasoning: str
