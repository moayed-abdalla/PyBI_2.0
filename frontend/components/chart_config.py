import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, Optional, List
import requests

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:5000/api")

# Color palettes for dark/light mode
LIGHT_COLORS = px.colors.qualitative.Set3
DARK_COLORS = px.colors.qualitative.Dark24

def get_color_palette():
    """Get color palette based on theme"""
    # Streamlit doesn't have direct theme access, so we'll use a default
    # In production, you might want to detect theme via CSS or user preference
    return LIGHT_COLORS

def create_chart(df: pd.DataFrame, chart_config: Dict[str, Any]) -> go.Figure:
    """Create a Plotly chart based on configuration"""
    chart_type = chart_config.get('chart_type', 'bar')
    x_column = chart_config.get('x_column')
    y_column = chart_config.get('y_column')
    metric_column = chart_config.get('metric_column')
    config = chart_config.get('config', {})
    
    # Get color palette
    colors = get_color_palette()
    
    try:
        if chart_type == 'metric':
            # Integer metric display
            if metric_column and metric_column in df.columns:
                value = df[metric_column].sum() if df[metric_column].dtype in ['int64', 'float64'] else len(df)
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="number",
                    value=value,
                    title={"text": chart_config.get('chart_title', metric_column)}
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                return fig
        
        elif chart_type == 'bar':
            if x_column and y_column and x_column in df.columns and y_column in df.columns:
                fig = px.bar(df, x=x_column, y=y_column, color=x_column, color_discrete_sequence=colors)
                fig.update_layout(
                    title=chart_config.get('chart_title', 'Bar Chart'),
                    xaxis_title=x_column,
                    yaxis_title=y_column
                )
                apply_chart_config(fig, config)
                return fig
        
        elif chart_type == 'line':
            if x_column and y_column and x_column in df.columns and y_column in df.columns:
                fig = px.line(df, x=x_column, y=y_column, color_discrete_sequence=colors)
                fig.update_layout(
                    title=chart_config.get('chart_title', 'Line Chart'),
                    xaxis_title=x_column,
                    yaxis_title=y_column
                )
                apply_chart_config(fig, config)
                return fig
        
        elif chart_type == 'scatter':
            if x_column and y_column and x_column in df.columns and y_column in df.columns:
                fig = px.scatter(df, x=x_column, y=y_column, color_discrete_sequence=colors)
                fig.update_layout(
                    title=chart_config.get('chart_title', 'Scatter Plot'),
                    xaxis_title=x_column,
                    yaxis_title=y_column
                )
                apply_chart_config(fig, config)
                return fig
        
        elif chart_type == 'pie':
            if x_column and y_column and x_column in df.columns and y_column in df.columns:
                fig = px.pie(df, names=x_column, values=y_column, color_discrete_sequence=colors)
                fig.update_layout(
                    title=chart_config.get('chart_title', 'Pie Chart')
                )
                apply_chart_config(fig, config)
                return fig
        
        # Default empty chart
        fig = go.Figure()
        fig.add_annotation(text="Please configure chart columns", showarrow=False)
        return fig
    
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error creating chart: {str(e)}", showarrow=False)
        return fig

def apply_chart_config(fig: go.Figure, config: Dict[str, Any]):
    """Apply configuration options to chart"""
    if config.get('flip_axes'):
        fig.update_layout(
            xaxis_title=fig.layout.yaxis.title.text,
            yaxis_title=fig.layout.xaxis.title.text
        )
        # Swap data
        for trace in fig.data:
            trace.x, trace.y = trace.y, trace.x
    
    if config.get('remove_labels'):
        fig.update_traces(textposition='none', texttemplate='')
        fig.update_layout(showlegend=False)
    
    if config.get('remove_lines') and hasattr(fig.data[0], 'line'):
        for trace in fig.data:
            trace.line = dict(width=0)

def chart_settings_popup(chart_id: str, chart_config: Dict[str, Any], dashboard_id: str):
    """Render chart settings popup"""
    with st.popover("⚙️ Settings"):
        st.write("**Chart Configuration**")
        
        # Flip axes
        flip_axes = st.checkbox(
            "Flip X/Y Axes",
            value=chart_config.get('config', {}).get('flip_axes', False),
            key=f"flip_{chart_id}"
        )
        
        # Remove labels
        remove_labels = st.checkbox(
            "Remove Labels",
            value=chart_config.get('config', {}).get('remove_labels', False),
            key=f"labels_{chart_id}"
        )
        
        # Remove lines
        remove_lines = st.checkbox(
            "Remove Lines",
            value=chart_config.get('config', {}).get('remove_lines', False),
            key=f"lines_{chart_id}"
        )
        
        # Update config
        if flip_axes != chart_config.get('config', {}).get('flip_axes') or \
           remove_labels != chart_config.get('config', {}).get('remove_labels') or \
           remove_lines != chart_config.get('config', {}).get('remove_lines'):
            
            chart_config['config'] = {
                'flip_axes': flip_axes,
                'remove_labels': remove_labels,
                'remove_lines': remove_lines
            }
            
            # Save to backend
            try:
                response = requests.put(
                    f"{API_BASE_URL}/charts/{chart_id}",
                    json=chart_config
                )
                if response.status_code == 200:
                    st.success("Settings updated!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error updating settings: {str(e)}")
        
        st.divider()
        
        # Delete chart
        if st.button("🗑️ Delete Chart", key=f"delete_{chart_id}", type="primary"):
            try:
                response = requests.delete(f"{API_BASE_URL}/charts/{chart_id}")
                if response.status_code == 200:
                    st.success("Chart deleted!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error deleting chart: {str(e)}")

def render_chart_editor(df: pd.DataFrame, chart_config: Dict[str, Any], dashboard_id: str):
    """Render chart with editor controls"""
    chart_id = chart_config.get('id')
    
    # Create columns for chart and settings
    col1, col2 = st.columns([10, 1])
    
    with col1:
        fig = create_chart(df, chart_config)
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{chart_id}")
    
    with col2:
        chart_settings_popup(chart_id, chart_config, dashboard_id)

