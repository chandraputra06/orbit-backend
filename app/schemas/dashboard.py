from pydantic import BaseModel

class MonthlySales(BaseModel):
    month: str
    sales: float

class DashboardSummary(BaseModel):
    total_customers: int
    total_orders: int
    total_sales: float
    average_order_value: float
    repeat_purchase_rate: float
    average_recency: float
    date_start: str
    date_end: str
    monthly_sales: list[MonthlySales]
