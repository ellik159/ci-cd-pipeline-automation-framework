"""
Optional web dashboard for viewing pipeline configurations and security reports

This is pretty basic right now - just serves static reports
TODO: Make it more interactive with real-time updates
"""

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

REPORTS_DIR = Path('./security_reports')


@app.route('/')
def index():
    """Main dashboard page"""
    # TODO: create actual HTML template
    return '''
    <html>
    <head>
        <title>Pipeline Dashboard</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            h1 { color: #333; }
            .report { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>CI/CD Pipeline Dashboard</h1>
        <p>Security Reports:</p>
        <div id="reports"></div>
        
        <script>
            // TODO: fetch actual reports and display them
            document.getElementById('reports').innerHTML = 
                '<p>No reports available. Run security scans first.</p>';
        </script>
    </body>
    </html>
    '''


@app.route('/api/reports')
def get_reports():
    """Get list of available security reports"""
    if not REPORTS_DIR.exists():
        return jsonify({'reports': []})
    
    reports = []
    for report_file in REPORTS_DIR.glob('*.json'):
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
                reports.append({
                    'name': report_file.stem,
                    'file': report_file.name,
                    'data': data
                })
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # skip invalid files
    
    return jsonify({'reports': reports})


@app.route('/api/reports/<filename>')
def get_report(filename):
    """Get specific security report"""
    # Validate filename to prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    report_path = REPORTS_DIR / filename
    
    if not report_path.exists():
        return jsonify({'error': 'Report not found'}), 404
    
    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'error': 'Could not read report'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("🚀 Starting dashboard on http://localhost:5000")
    print("   Note: This is very basic and mostly for demo purposes")
    # Only bind to 0.0.0.0 and enable debug if explicitly set
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    app.run(debug=debug_mode, host=host, port=5000)
