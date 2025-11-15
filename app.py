from flask import Flask, render_template, request, send_file, jsonify, session
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import tempfile
import zipfile
from io import BytesIO
import base64
import json
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# --- CONFIG ---
UPLOAD_FOLDER = 'uploads'
TEMPLATES_FOLDER = 'templates'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_EXCEL_EXTENSIONS = {'xlsx', 'xls', 'csv'}

# Default font path (used as fallback)
FONT_PATH = r"C:/Windows/Fonts/arial.ttf"

# Supported fonts and styles on Windows (ttf names)
# If a font file is missing on the system, code falls back to default FONT_PATH
FONT_FILES = {
    'Arial': {
        'Regular': r"C:/Windows/Fonts/arial.ttf",
        'Bold': r"C:/Windows/Fonts/arialbd.ttf",
        'Italic': r"C:/Windows/Fonts/ariali.ttf",
        'Bold Italic': r"C:/Windows/Fonts/arialbi.ttf",
    },
    'Times New Roman': {
        'Regular': r"C:/Windows/Fonts/times.ttf",
        'Bold': r"C:/Windows/Fonts/timesbd.ttf",
        'Italic': r"C:/Windows/Fonts/timesi.ttf",
        'Bold Italic': r"C:/Windows/Fonts/timesbi.ttf",
    },
    'Calibri': {
        'Regular': r"C:/Windows/Fonts/calibri.ttf",
        'Bold': r"C:/Windows/Fonts/calibrib.ttf",
        'Italic': r"C:/Windows/Fonts/calibrii.ttf",
        'Bold Italic': r"C:/Windows/Fonts/calibriz.ttf",
    },
    'Verdana': {
        'Regular': r"C:/Windows/Fonts/verdana.ttf",
        'Bold': r"C:/Windows/Fonts/verdanab.ttf",
        'Italic': r"C:/Windows/Fonts/verdanai.ttf",
        'Bold Italic': r"C:/Windows/Fonts/verdanaz.ttf",
    },
    'Georgia': {
        'Regular': r"C:/Windows/Fonts/georgia.ttf",
        'Bold': r"C:/Windows/Fonts/georgiab.ttf",
        'Italic': r"C:/Windows/Fonts/georgiai.ttf",
        'Bold Italic': r"C:/Windows/Fonts/georgiaz.ttf",
    },
}

# --- CREATE FOLDERS ---
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMPLATES_FOLDER, exist_ok=True)
os.makedirs('certificates', exist_ok=True)

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/')
def index():
    # Get list of available templates
    templates = []
    if os.path.exists(TEMPLATES_FOLDER):
        for file in os.listdir(TEMPLATES_FOLDER):
            if allowed_file(file, ALLOWED_EXTENSIONS):
                templates.append(file)
    
    # Add default template if it exists
    default_template = "certificate_templates.png.png"
    if os.path.exists(default_template) and default_template not in templates:
        templates.insert(0, default_template)
    
    return render_template('index.html', templates=templates)

@app.route('/upload_template', methods=['POST'])
def upload_template():
    try:
        if 'template' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['template']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            # Add unique identifier to avoid conflicts
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
            filepath = os.path.join(TEMPLATES_FOLDER, unique_filename)
            file.save(filepath)
            
            return jsonify({'success': True, 'filename': unique_filename})
        else:
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_names', methods=['POST'])
def upload_names():
    try:
        if 'names_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['names_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename, ALLOWED_EXCEL_EXTENSIONS):
            # Read the file based on its type
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                elif file.filename.endswith('.xls'):
                    df = pd.read_excel(file, engine='xlrd')
                else:
                    return jsonify({'error': 'Unsupported file format'}), 400
                
                # Extract names from the dataframe
                names = []
                if 'Name' in df.columns:
                    names = df['Name'].dropna().astype(str).tolist()
                elif 'name' in df.columns:
                    names = df['name'].dropna().astype(str).tolist()
                elif 'Names' in df.columns:
                    names = df['Names'].dropna().astype(str).tolist()
                elif 'names' in df.columns:
                    names = df['names'].dropna().astype(str).tolist()
                else:
                    # If no standard column names, use the first column
                    first_col = df.columns[0]
                    names = df[first_col].dropna().astype(str).tolist()
                
                # Clean names (remove extra whitespace)
                names = [name.strip() for name in names if name.strip()]
                
                if not names:
                    return jsonify({'error': 'No valid names found in the file'}), 400
                
                return jsonify({
                    'success': True, 
                    'names': names,
                    'count': len(names),
                    'filename': file.filename
                })
                
            except Exception as e:
                return jsonify({'error': f'Error reading file: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Invalid file type. Allowed: XLSX, XLS, CSV'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_template', methods=['POST'])
def delete_template():
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        filepath = os.path.join(TEMPLATES_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_certificates():
    try:
        # Get form data
        font_size = int(request.form.get('font_size', 150))
        font_color = request.form.get('font_color', '#B87333')
        text_y_position = int(request.form.get('text_y_position', 600))
        template_name = request.form.get('template_name', 'certificate_templates.png.png')
        names_input = request.form.get('names_input', '')
        font_family = request.form.get('font_family', 'Arial')
        font_style = request.form.get('font_style', 'Regular')
        
        # Parse names from input
        if names_input.strip():
            names = [name.strip() for name in names_input.split('\n') if name.strip()]
        else:
            return jsonify({'error': 'Please provide at least one name'}), 400
        
        # Determine template path
        if template_name == 'certificate_templates.png.png':
            template_path = template_name
        else:
            template_path = os.path.join(TEMPLATES_FOLDER, template_name)
        
        if not os.path.exists(template_path):
            return jsonify({'error': 'Template not found'}), 404
        
        # Create temporary directory for generated certificates
        temp_dir = tempfile.mkdtemp()
        generated_files = []
        
        for name in names:
            # Open template
            img = Image.open(template_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            # Resolve font path from mapping, fallback to default
            font_path = FONT_FILES.get(font_family, {}).get(font_style, FONT_PATH)
            try:
                font = ImageFont.truetype(font_path, font_size)
            except OSError:
                try:
                    font = ImageFont.truetype(FONT_PATH, font_size)
                except OSError:
                    font = ImageFont.load_default()
            
            # Center text horizontally
            text_width = draw.textlength(name, font=font)
            image_width = img.width
            x_position = (image_width - text_width) / 2
            
            # Draw name
            draw.text((x_position, text_y_position), name, font=font, fill=font_color)
            
            # Save to temporary directory
            output_path = os.path.join(temp_dir, f"{name}.pdf")
            img.save(output_path, "PDF")
            generated_files.append(output_path)
        
        # Create ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in generated_files:
                zip_file.write(file_path, os.path.basename(file_path))
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='certificates.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_certificate():
    try:
        # Get form data
        font_size = int(request.form.get('font_size', 150))
        font_color = request.form.get('font_color', '#B87333')
        text_y_position = int(request.form.get('text_y_position', 600))
        template_name = request.form.get('template_name', 'certificate_templates.png.png')
        sample_name = request.form.get('sample_name', 'Sample Name')
        font_family = request.form.get('font_family', 'Arial')
        font_style = request.form.get('font_style', 'Regular')
        
        # Determine template path
        if template_name == 'certificate_templates.png.png':
            template_path = template_name
        else:
            template_path = os.path.join(TEMPLATES_FOLDER, template_name)
        
        if not os.path.exists(template_path):
            return jsonify({'error': 'Template not found'}), 404
        
        # Open template
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        
        # Load font
        font_path = FONT_FILES.get(font_family, {}).get(font_style, FONT_PATH)
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            try:
                font = ImageFont.truetype(FONT_PATH, font_size)
            except OSError:
                font = ImageFont.load_default()
        
        # Center text horizontally
        text_width = draw.textlength(sample_name, font=font)
        image_width = img.width
        x_position = (image_width - text_width) / 2
        
        # Draw name
        draw.text((x_position, text_y_position), sample_name, font=font, fill=font_color)
        
        # Convert to base64 for preview
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({'preview': f'data:image/png;base64,{img_base64}'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_templates')
def get_templates():
    try:
        templates = []
        if os.path.exists(TEMPLATES_FOLDER):
            for file in os.listdir(TEMPLATES_FOLDER):
                if allowed_file(file, ALLOWED_EXTENSIONS):
                    templates.append(file)
        
        # Add default template if it exists
        default_template = "certificate_templates.png.png"
        if os.path.exists(default_template):
            templates.insert(0, default_template)
        
        return jsonify({'templates': templates})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_fonts')
def get_fonts():
    try:
        # Build a serializable list of available fonts and styles
        fonts = []
        for family, styles in FONT_FILES.items():
            fonts.append({
                'family': family,
                'styles': list(styles.keys())
            })
        return jsonify({'fonts': fonts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
