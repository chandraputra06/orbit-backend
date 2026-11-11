from fastapi import APIRouter
from app.api.v1.endpoints import (health, auth, upload, dashboard,
                                  analytics, fuzzy, customers, insights)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(upload.router, tags=["Upload"])
api_router.include_router(dashboard.router, tags=["Dashboard"])
api_router.include_router(analytics.router, tags=["Analyses"])
api_router.include_router(fuzzy.router, tags=["Fuzzy Mamdani"])
api_router.include_router(customers.router, tags=["Customers"])
api_router.include_router(insights.router, tags=["Insights"])
