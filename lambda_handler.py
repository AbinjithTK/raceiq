"""
AWS Lambda handler for RaceIQ API
Serverless deployment using Mangum adapter
"""

from mangum import Mangum
from src.api.main import app

# Create Lambda handler
handler = Mangum(app, lifespan="off")
