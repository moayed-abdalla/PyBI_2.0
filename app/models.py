"""
Database models and data structures for PyBI
"""
from typing import Optional, Dict, Any
from datetime import datetime

class Dashboard:
    """Dashboard model"""
    def __init__(self, id: str, name: str, description: Optional[str] = None, 
                 created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class KPIChart:
    """KPI Chart configuration model"""
    def __init__(self, id: str, dashboard_id: str, chart_type: str, 
                 chart_title: Optional[str] = None, x_column: Optional[str] = None,
                 y_column: Optional[str] = None, metric_column: Optional[str] = None,
                 config: Optional[Dict] = None, position: Optional[int] = None):
        self.id = id
        self.dashboard_id = dashboard_id
        self.chart_type = chart_type
        self.chart_title = chart_title
        self.x_column = x_column
        self.y_column = y_column
        self.metric_column = metric_column
        self.config = config or {}
        self.position = position
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'dashboard_id': self.dashboard_id,
            'chart_type': self.chart_type,
            'chart_title': self.chart_title,
            'x_column': self.x_column,
            'y_column': self.y_column,
            'metric_column': self.metric_column,
            'config': self.config,
            'position': self.position
        }

