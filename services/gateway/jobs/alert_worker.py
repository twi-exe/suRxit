"""
alert_worker.py — background job for alerts

Responsibilities:
    - Subscribe to Kafka/Redis for RISK_ALERT events
    - Store alerts in DB
    - Send notifications (email/SMS/FCM)
"""
import asyncio

async def alert_worker():
        """Background job: handle RISK_ALERT events and dispatch notifications."""
        # TODO: Subscribe to Kafka/Redis for RISK_ALERT events
        # TODO: Store in alerts table
        # TODO: Send notifications
        pass
