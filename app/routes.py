from flask import Blueprint, request, jsonify, send_file
import io
from app.utils import (
    upload_file_to_supabase, get_dashboard_data, create_dashboard,
    get_dashboards, get_dashboard, save_chart_config, get_charts, delete_chart
)
from supabase.config import supabase

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@bp.route('/dashboards', methods=['GET', 'POST'])
def dashboards():
    """List all dashboards or create a new one"""
    if request.method == 'GET':
        try:
            dashboards_list = get_dashboards()
            return jsonify(dashboards_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            
            if not name:
                return jsonify({'error': 'Dashboard name is required'}), 400
            
            dashboard = create_dashboard(name, description)
            return jsonify(dashboard), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/dashboards/<dashboard_id>', methods=['GET', 'PUT', 'DELETE'])
def dashboard(dashboard_id):
    """Get, update, or delete a specific dashboard"""
    if request.method == 'GET':
        try:
            dashboard = get_dashboard(dashboard_id)
            if not dashboard:
                return jsonify({'error': 'Dashboard not found'}), 404
            return jsonify(dashboard), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            result = supabase.table('dashboards').update({
                'name': data.get('name'),
                'description': data.get('description'),
                'updated_at': 'now()'
            }).eq('id', dashboard_id).execute()
            
            if not result.data:
                return jsonify({'error': 'Dashboard not found'}), 404
            return jsonify(result.data[0]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            supabase.table('dashboards').delete().eq('id', dashboard_id).execute()
            return jsonify({'message': 'Dashboard deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/dashboards/<dashboard_id>/upload', methods=['POST'])
def upload_file(dashboard_id):
    """Upload a data file for a dashboard"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Verify dashboard exists
        dashboard = get_dashboard(dashboard_id)
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        file_info = upload_file_to_supabase(file, dashboard_id)
        return jsonify(file_info), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboards/<dashboard_id>/data', methods=['GET'])
def get_data(dashboard_id):
    """Get data for a dashboard"""
    try:
        df = get_dashboard_data(dashboard_id)
        
        if df is None:
            return jsonify({'data': [], 'columns': []}), 200
        
        # Convert DataFrame to JSON
        data = df.to_dict('records')
        columns = list(df.columns)
        
        return jsonify({
            'data': data,
            'columns': columns,
            'row_count': len(df)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboards/<dashboard_id>/charts', methods=['GET', 'POST'])
def charts(dashboard_id):
    """Get all charts or create a new chart for a dashboard"""
    if request.method == 'GET':
        try:
            charts_list = get_charts(dashboard_id)
            return jsonify(charts_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            chart_config = request.get_json()
            chart = save_chart_config(dashboard_id, chart_config)
            return jsonify(chart), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/charts/<chart_id>', methods=['PUT', 'DELETE'])
def chart(chart_id):
    """Update or delete a specific chart"""
    if request.method == 'PUT':
        try:
            chart_config = request.get_json()
            chart_config['id'] = chart_id
            chart = save_chart_config(chart_config.get('dashboard_id'), chart_config)
            return jsonify(chart), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            delete_chart(chart_id)
            return jsonify({'message': 'Chart deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

