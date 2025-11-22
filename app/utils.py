import os
import pandas as pd
import uuid
from typing import Optional, Dict, Any, List
from werkzeug.utils import secure_filename
from supabase.config import supabase

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_supabase(file, dashboard_id: str) -> Dict[str, Any]:
    """
    Upload file to Supabase Storage and save metadata to database
    """
    if not allowed_file(file.filename):
        raise ValueError(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Secure filename and create unique path
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = f"uploads/{dashboard_id}/{unique_filename}"
    
    # Read file content
    file_content = file.read()
    file.seek(0)  # Reset file pointer
    
    # Upload to Supabase Storage
    try:
        # Ensure the path exists (create directory structure)
        storage = supabase.storage.from_("data-files")
        
        # Upload file
        storage_response = storage.upload(
            file_path, 
            file_content,
            file_options={"content-type": getattr(file, 'content_type', None) or "application/octet-stream", "upsert": "true"}
        )
        
        # Check for errors in response
        if hasattr(storage_response, 'error') and storage_response.error:
            raise Exception(f"Storage upload failed: {storage_response.error}")
        
        # Get public URL
        public_url_response = storage.get_public_url(file_path)
        public_url = public_url_response if isinstance(public_url_response, str) else public_url_response.get('publicUrl', '')
        
        # Save metadata to database
        file_record = {
            'dashboard_id': dashboard_id,
            'file_name': filename,
            'file_path': file_path,
            'file_type': file_ext
        }
        
        result = supabase.table('data_files').insert(file_record).execute()
        
        return {
            'id': result.data[0]['id'] if result.data else None,
            'file_name': filename,
            'file_path': file_path,
            'public_url': public_url,
            'file_type': file_ext
        }
    except Exception as e:
        raise Exception(f"Failed to upload file: {str(e)}")

def read_data_file(file_path: str, file_type: str) -> pd.DataFrame:
    """
    Read data file from Supabase Storage
    """
    try:
        # Download file from Supabase Storage
        file_data = supabase.storage.from_("data-files").download(file_path)
        
        # Read into pandas DataFrame
        if file_type == 'csv':
            import io
            df = pd.read_csv(io.BytesIO(file_data))
        elif file_type in ['xlsx', 'xls']:
            import io
            df = pd.read_excel(io.BytesIO(file_data))
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return df
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")

def get_dashboard_data(dashboard_id: str) -> Optional[pd.DataFrame]:
    """
    Retrieve and combine all data files for a dashboard
    """
    try:
        # Get all files for this dashboard
        files_response = supabase.table('data_files').select('*').eq('dashboard_id', dashboard_id).execute()
        
        if not files_response.data:
            return None
        
        # Read and combine all data files
        dataframes = []
        for file_record in files_response.data:
            df = read_data_file(file_record['file_path'], file_record['file_type'])
            dataframes.append(df)
        
        if not dataframes:
            return None
        
        # Combine all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
    
    except Exception as e:
        raise Exception(f"Failed to get dashboard data: {str(e)}")

def create_dashboard(name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new dashboard"""
    try:
        result = supabase.table('dashboards').insert({
            'name': name,
            'description': description
        }).execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        raise Exception(f"Failed to create dashboard: {str(e)}")

def get_dashboards() -> List[Dict[str, Any]]:
    """Get all dashboards"""
    try:
        result = supabase.table('dashboards').select('*').order('created_at', desc=True).execute()
        return result.data if result.data else []
    except Exception as e:
        raise Exception(f"Failed to get dashboards: {str(e)}")

def get_dashboard(dashboard_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific dashboard"""
    try:
        result = supabase.table('dashboards').select('*').eq('id', dashboard_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise Exception(f"Failed to get dashboard: {str(e)}")

def save_chart_config(dashboard_id: str, chart_config: Dict[str, Any]) -> Dict[str, Any]:
    """Save or update a chart configuration"""
    try:
        chart_id = chart_config.get('id')
        
        if chart_id:
            # Update existing chart
            result = supabase.table('kpi_charts').update({
                'chart_type': chart_config.get('chart_type'),
                'chart_title': chart_config.get('chart_title'),
                'x_column': chart_config.get('x_column'),
                'y_column': chart_config.get('y_column'),
                'metric_column': chart_config.get('metric_column'),
                'config': chart_config.get('config', {}),
                'position': chart_config.get('position')
            }).eq('id', chart_id).execute()
        else:
            # Create new chart
            result = supabase.table('kpi_charts').insert({
                'dashboard_id': dashboard_id,
                'chart_type': chart_config.get('chart_type'),
                'chart_title': chart_config.get('chart_title'),
                'x_column': chart_config.get('x_column'),
                'y_column': chart_config.get('y_column'),
                'metric_column': chart_config.get('metric_column'),
                'config': chart_config.get('config', {}),
                'position': chart_config.get('position')
            }).execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        raise Exception(f"Failed to save chart config: {str(e)}")

def get_charts(dashboard_id: str) -> List[Dict[str, Any]]:
    """Get all charts for a dashboard"""
    try:
        result = supabase.table('kpi_charts').select('*').eq('dashboard_id', dashboard_id).order('position').execute()
        return result.data if result.data else []
    except Exception as e:
        raise Exception(f"Failed to get charts: {str(e)}")

def delete_chart(chart_id: str) -> bool:
    """Delete a chart"""
    try:
        supabase.table('kpi_charts').delete().eq('id', chart_id).execute()
        return True
    except Exception as e:
        raise Exception(f"Failed to delete chart: {str(e)}")

