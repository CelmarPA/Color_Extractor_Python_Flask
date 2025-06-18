from flask import Flask, render_template, request, url_for, redirect
from extract_colors import GetMostCommonColors
import os
import shutil

UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Clear the uploads folder on application start
if os.path.exists(UPLOAD_FOLDER):
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # delete file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # delete directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
else:
    os.makedirs(UPLOAD_FOLDER)

# Initialize Flask app and configure upload folder
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    """
    Home route that loads the default image and extracts colors.

    Returns:
        Rendered template 'index.html' with:
            - colors: dict of extracted colors and their percentages from the default image.
    """
    image_path = 'static/assets/images/test.jpg'  # Default image path

    extractor = GetMostCommonColors(10)  # Initialize extractor for 10 colors
    extractor.get_image(image_path)      # Load default image
    colors = extractor.get_colors()      # Extract colors and percentages

    return render_template('index.html', colors=colors)


@app.route('/get_image', methods=['GET', 'POST'])
def get_image():
    """
    Route to handle image upload via POST method.

    Validations:
        - Checks if the 'image' file part is in the request.
        - Redirects to home if no image is uploaded or filename is empty.

    Actions:
        - Saves the uploaded image to the upload folder.
        - Prepares relative path to image for template.
        - Renders 'index.html' with uploaded image and no colors (waiting for extraction).

    Returns:
        Redirects to home on invalid request or renders template with uploaded image info.
    """
    if request.method == 'POST':

        # Validate 'image' part in request files
        if 'image' not in request.files:
            return redirect(url_for('home'))

        image = request.files['image']

        # Validate image filename
        if image.filename == '':
            return redirect(url_for('home'))

        if image:
            # Save uploaded image to configured folder
            filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Create relative image path for template rendering
            image_file = f'uploads/{filename}'

            # Render template with uploaded image path, colors is None (extraction pending)
            return render_template('index.html', image_file=image_file, image_path=image_path, colors=None)

    # Redirect to home if method is GET or no valid image uploaded
    return redirect(url_for('home'))


@app.route("/extract", methods=["POST"])
def extract():
    """
    Route to extract colors from a given image with specified number of colors.

    Expects:
        - 'colors' parameter: number of colors to extract (default 10).
        - 'image_path' parameter: path to the image to process.

    Process:
        - Normalizes Windows-style backslashes to forward slashes.
        - Uses default image if no path provided.
        - Converts absolute/static path to relative path for HTML templates.
        - Extracts colors from the image using GetMostCommonColors.
        - Prints the percentages to console for debugging.

    Returns:
        Renders 'index.html' with:
            - image_path: path to the image processed
            - image_file: relative path for template image display
            - colors: dict of extracted colors and their percentages
    """
    num_colors = int(request.form.get("colors", 10))
    image_path = request.form.get("image_path")

    # Normalize path to use forward slashes (important on Windows)
    if image_path:
        image_path = image_path.replace("\\", "/")

    # Use default image if no path provided
    if not image_path:
        image_path = 'static/assets/images/test.jpg'  # Default fallback image

    # Extract relative path from static folder for templates
    if image_path.startswith('static/'):
        image_file = image_path[len('static/'):]
    else:
        image_file = image_path

    # Extract colors using the helper class
    extractor = GetMostCommonColors(num_colors)
    extractor.get_image(image_path)
    colors = extractor.get_colors()

    # Debug: print percentages to console
    # for color, percent in colors.items():
    #     print(percent)

    # Render template with all relevant info
    return render_template("index.html", image_path=image_path, image_file=image_file, colors=colors)


# --- Entry point ---
if __name__ == "__main__":
    # Start Flask app in debug mode
    app.run(debug=True)
