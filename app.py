from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='template')

# Set the upload folder and allowed extensions for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'flv', 'wmv'}

# Check if a filename is allowed based on the file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    # Check if the POST request has a file part
    if 'video_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['video_file']
    # If the user does not select a file, browser also
    # submits an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Save the file to the upload folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Call your lane detection function here using the saved file path
        # ...
        return 'Video processing complete!'
    else:
        flash('Invalid file type')
        return redirect(request.url)
