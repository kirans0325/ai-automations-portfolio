from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    FEATURE_REQUEST = "feature_request"
    ACCOUNT_ACCESS = "account_access"
    OTHER = "other"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    FRUSTRATED = "frustrated"


class ActionItem(BaseModel):
    description: str = Field(description="Specific task or step required to address the ticket")
    assignee_role: str = Field(description="Role responsible for this action, e.g., Tier 2 Engineer, Finance Team")


class SupportTicketAnalysis(BaseModel):
    """Guaranteed structured output schema extracted from unstructured customer ticket text."""

    ticket_summary: str = Field(description="Concise 1-2 sentence summary of the core customer issue")
    category: TicketCategory = Field(description="Primary category of the issue")
    priority: PriorityLevel = Field(description="Urgency/priority assigned based on impact")
    customer_sentiment: Sentiment = Field(description="Detected emotional tone of the customer")
    customer_name: Optional[str] = Field(default=None, description="Name of customer if mentioned in text")
    account_id: Optional[str] = Field(default=None, description="Account/Invoice ID if referenced")
    affected_product: Optional[str] = Field(default=None, description="Product or service affected")
    action_items: List[ActionItem] = Field(default_factory=list, description="Recommended next actions for support staff")
