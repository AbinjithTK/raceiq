"""
AWS Elastic Beanstalk application entry point
"""

from src.api.main import app

# Elastic Beanstalk expects 'application' variable
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8080)
