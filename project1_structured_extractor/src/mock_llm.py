import re
from src.models import SupportTicketAnalysis, TicketCategory, PriorityLevel, Sentiment, ActionItem


def mock_extract_ticket_data(raw_text: str) -> SupportTicketAnalysis:
    """Offline rule-assisted parser that mimics LLM structured data extraction.
    Ensures keyless instant offline testing for learners.
    """
    text_lower = raw_text.lower()

    # Determine Category
    if any(k in text_lower for k in ["invoice", "charge", "refund", "billing", "payment", "$", "credit card"]):
        category = TicketCategory.BILLING
    elif any(k in text_lower for k in ["login", "password", "2fa", "access", "locked out"]):
        category = TicketCategory.ACCOUNT_ACCESS
    elif any(k in text_lower for k in ["crash", "error", "bug", "404", "500", "broken", "fail", "slow", "down"]):
        category = TicketCategory.TECHNICAL_SUPPORT
    elif any(k in text_lower for k in ["feature", "request", "add", "suggestion", "would be great"]):
        category = TicketCategory.FEATURE_REQUEST
    else:
        category = TicketCategory.OTHER

    # Determine Priority & Sentiment
    if any(k in text_lower for k in ["immediately", "urgent", "asap", "down", "production", "blocked"]):
        priority = PriorityLevel.URGENT
        sentiment = Sentiment.FRUSTRATED
    elif any(k in text_lower for k in ["unacceptable", "frustrated", "angry", "terrible", "issue"]):
        priority = PriorityLevel.HIGH
        sentiment = Sentiment.NEGATIVE
    elif any(k in text_lower for k in ["please help", "question", "assistance"]):
        priority = PriorityLevel.MEDIUM
        sentiment = Sentiment.NEUTRAL
    else:
        priority = PriorityLevel.LOW
        sentiment = Sentiment.POSITIVE

    # Extract Customer Name
    name_match = re.search(r"(?:thanks,|regards,|from:|name:)\s*([A-Z][a-z]+\s+[A-Z][a-z]+)", raw_text, re.IGNORECASE)
    customer_name = name_match.group(1) if name_match else "Jane Doe"

    # Extract Account or Invoice ID
    acc_match = re.search(r"(INV-\d+|ACC-\d+|#\d{4,})", raw_text)
    account_id = acc_match.group(1) if acc_match else "INV-98214"

    # Product match
    prod_match = re.search(r"(CloudSync|DataFlow|AuthPortal|Analytics Hub|API Service)", raw_text, re.IGNORECASE)
    affected_product = prod_match.group(1) if prod_match else "SaaS Platform"

    # Construct Action Items based on category
    if category == TicketCategory.BILLING:
        actions = [
            ActionItem(description="Verify billing ledger and check double-charge status", assignee_role="Billing Specialist"),
            ActionItem(description="Issue refund or credit if billing discrepancy is confirmed", assignee_role="Finance Lead")
        ]
    elif category == TicketCategory.TECHNICAL_SUPPORT:
        actions = [
            ActionItem(description="Inspect server error logs for affected product", assignee_role="DevOps / Backend Eng"),
            ActionItem(description="Contact customer with troubleshooting steps", assignee_role="Tier 2 Support")
        ]
    else:
        actions = [
            ActionItem(description="Triage support ticket and acknowledge customer request", assignee_role="Customer Success")
        ]

    # Summary
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    summary = lines[0] if lines else "Customer reported issue needing support triage."
    if len(summary) > 120:
        summary = summary[:117] + "..."

    return SupportTicketAnalysis(
        ticket_summary=summary,
        category=category,
        priority=priority,
        customer_sentiment=sentiment,
        customer_name=customer_name,
        account_id=account_id,
        affected_product=affected_product,
        action_items=actions
    )
