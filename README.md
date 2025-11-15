# Certificate Generator Web Application

A beautiful web interface for generating personalized certificates with customizable templates, fonts, colors, and positioning.

## ✨ New Features

- 🎨 **Enhanced Font Color Picker**: Beautiful preset colors + custom color selection
- 📊 **Excel File Support**: Upload XLSX, XLS, and CSV files with names
- 📏 **Adjustable Font Size**: Range from 50 to 300 pixels
- 📍 **Flexible Positioning**: Control vertical position of the name text
- 👀 **Live Preview**: See how your certificate will look before generating
- 📁 **Template Management**: Upload, select, and manage multiple certificate templates
- 👥 **Dual Name Input**: Manual entry or file upload (no CSV required)
- 💾 **ZIP Download**: All certificates are packaged in a single ZIP file
- 🗑️ **Template Deletion**: Remove unwanted templates easily

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Files

Make sure you have:
- **Default Template**: `certificate_templates.png.png` in the root directory (optional)
- **Output Directory**: `certificates/` folder (will be created automatically)
- **Upload Folders**: `uploads/` and `templates/` folders (will be created automatically)

### 3. Run the Application

```bash
python app.py
```

The web application will start at `http://localhost:5000`

## 🎯 Usage

### **Template Management**
1. **Upload New Templates**: Click the upload area in the "Template Management" section
2. **Supported Formats**: PNG, JPG, JPEG, GIF, BMP
3. **Select Template**: Choose from available templates in the dropdown
4. **Delete Templates**: Remove unwanted templates (default template cannot be deleted)

### **Enhanced Font Color Selection**
1. **Preset Colors**: Choose from 12 beautiful preset colors including:
   - Professional: Copper (#B87333), Dark Blue (#2c3e50), Navy (#34495e)
   - Vibrant: Red (#e74c3c), Green (#27ae60), Orange (#f39c12)
   - Elegant: Purple (#9b59b6), Teal (#16a085), Gold (#f1c40f)
2. **Custom Colors**: Use the color picker for any specific color
3. **Visual Feedback**: Selected colors show checkmark and enhanced border
4. **Hover Effects**: Interactive color selection with smooth animations

### **Customization Options**
1. **Font Size**: Adjust using the slider (50-300px)
2. **Font Color**: Pick from presets or use custom color picker
3. **Text Position**: Set vertical placement (200-800px)
4. **Sample Name**: Enter a name to preview your settings

### **Recipient Names - Dual Input Methods**

#### **Method 1: Manual Input**
1. **Enter Names**: Type or paste names in the textarea (one per line)
2. **Example Format**:
   ```
   John Doe
   Jane Smith
   Michael Brown
   ```

#### **Method 2: File Upload**
1. **Supported Formats**: XLSX, XLS, CSV
2. **Column Detection**: Automatically detects columns named:
   - "Name", "name", "Names", "names"
   - Falls back to first column if no standard names found
3. **File Processing**: 
   - Upload your Excel/CSV file
   - View preview of extracted names
   - Names are automatically loaded into the manual input field
4. **Smart Parsing**: Handles various Excel formats and CSV delimiters

### **Generate Certificates**
1. **Preview**: Click "Preview" to see how your certificate will look
2. **Generate**: Click "Generate All" to create certificates for all names
3. **Download**: Certificates are automatically downloaded as a ZIP file

## 📁 File Structure

```
certificate.py/
├── app.py                 # Flask web application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── certificate_templates.png.png  # Default template (optional)
├── uploads/              # Temporary upload folder
├── templates/            # User-uploaded templates
└── certificates/         # Output directory for generated certificates
```

## 🔧 Customization Options

- **Font Size**: 50px to 300px (default: 150px)
- **Font Color**: 12 preset colors + unlimited custom colors
- **Vertical Position**: 200px to 800px (default: 600px)
- **Font Family**: Currently uses Arial (Windows) or system default
- **Template Formats**: PNG, JPG, JPEG, GIF, BMP
- **Names File Formats**: XLSX, XLS, CSV

## 🎨 Color Palette

The application includes a carefully curated selection of professional and attractive colors:

| Color | Hex Code | Use Case |
|-------|----------|----------|
| Copper | #B87333 | Classic, Professional |
| Dark Blue | #2c3e50 | Corporate, Trustworthy |
| Navy | #34495e | Elegant, Formal |
| Red | #e74c3c | Attention-grabbing, Important |
| Green | #27ae60 | Success, Growth |
| Orange | #f39c12 | Creative, Energetic |
| Purple | #9b59b6 | Royal, Creative |
| Teal | #16a085 | Modern, Balanced |
| Gold | #f1c40f | Premium, Achievement |
| Light Green | #2ecc71 | Fresh, Positive |
| Dark Purple | #8e44ad | Sophisticated, Mysterious |
| Dark Orange | #e67e22 | Warm, Inviting |

## 🆕 What's New vs. Previous Version

| Feature | Previous Version | New Version |
|---------|------------------|-------------|
| **Font Color Picker** | Basic color input | **12 preset colors + custom picker** |
| **Names Input** | Manual only | **Manual + Excel/CSV upload** |
| **File Support** | No file upload | **XLSX, XLS, CSV support** |
| **Color Selection** | Single color input | **Visual color palette with feedback** |
| **User Experience** | Basic controls | **Interactive color selection + tabs** |

## 🛠️ Troubleshooting

- **Template not found**: Upload a new template or check the templates folder
- **Upload fails**: Ensure file is in supported format (PNG/JPG for templates, XLSX/XLS/CSV for names)
- **Excel reading error**: Ensure Excel files are not password-protected and have readable data
- **Column not found**: The app will use the first column if no standard name columns are detected
- **Font issues**: The app will fall back to system default font if Arial is not available
- **Port already in use**: Change the port in `app.py` line 108: `app.run(debug=True, host='0.0.0.0', port=5001)`
- **File permissions**: Ensure the app has write permissions for the uploads and templates folders

## 🔒 Security Features

- **Secure Filenames**: Uploaded files are sanitized to prevent security issues
- **Unique Naming**: Files get unique identifiers to prevent conflicts
- **File Type Validation**: Only allowed file types are accepted
- **Session Management**: Secure session handling for file operations
- **Excel Security**: Safe Excel file parsing with pandas

## 💻 Technical Details

- **Backend**: Flask (Python web framework)
- **Image Processing**: Pillow (PIL) for certificate generation
- **File Handling**: Secure file uploads with Werkzeug
- **Excel Processing**: pandas with openpyxl and xlrd engines
- **Frontend**: Responsive HTML/CSS/JavaScript with interactive color picker
- **File Formats**: Generates PDF certificates from various image templates
- **Real-time Preview**: Base64 encoded images for instant preview
- **Batch Processing**: Generates multiple certificates simultaneously
- **ZIP Creation**: Automatic packaging of all generated certificates

## 📱 Responsive Design

- **Desktop**: 3-column layout for optimal organization
- **Tablet**: 2-column layout with preview spanning full width
- **Mobile**: Single-column layout with stacked controls
- **Touch-friendly**: Optimized for touch devices
- **Color Picker**: Responsive grid layout for preset colors

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradients
- **Interactive Controls**: Real-time updates and visual feedback
- **Enhanced Color Picker**: Visual color palette with hover effects and selection feedback
- **Tabbed Interface**: Organized input methods for names
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages and success notifications
- **Drag & Drop**: Intuitive file upload interface
- **Color Feedback**: Visual confirmation of selected colors

## 📊 Excel File Requirements

### **Supported Formats**
- **XLSX**: Modern Excel format (recommended)
- **XLS**: Legacy Excel format
- **CSV**: Comma-separated values

### **Column Naming**
The application automatically detects these column names:
- `Name`, `name`
- `Names`, `names`
- Falls back to first column if no standard names found

### **File Structure Example**
```
| Name        | Email           | Department |
|-------------|-----------------|------------|
| John Doe    | john@email.com  | IT         |
| Jane Smith  | jane@email.com  | HR         |
| Mike Brown  | mike@email.com  | Sales      |
```

## License

This project is open source and available under the MIT License.
