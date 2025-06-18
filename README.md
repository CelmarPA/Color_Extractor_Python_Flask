# 🖌️ Color Extractor - Image Color Palette with Flask

A web application built with Flask to extract and display the most common colors from an image using KMeans clustering. Users can upload an image, select the number of dominant colors, and get a palette with HEX codes and their percentages.

---

## 📌 Table of Contents

- [🖌️ Color Extractor - Image Color Palette with Flask](#️-color-extractor---image-color-palette-with-flask)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Features](#-features)
  - [⚙️ How It Works](#️-how-it-works)
  - [🧰 Technologies](#-technologies)
  - [🛠️ Getting Started](#️-getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Run the App](#3-run-the-app)
  - [📂 Project Structure](#-project-structure)
  - [📄 License](#-license)
  - [👤 Author](#-author)
  - [💬 Feedback](#-feedback)

---

## 🚀 Features

- Upload an image or use a default sample image
- Select the number of dominant colors to extract (default 10)
- Uses KMeans clustering to find dominant colors
- Displays extracted color palette with HEX codes and percentages
- Responsive UI with color preview and hover effects
- Copy HEX code to clipboard by clicking on a color box

---

## ⚙️ How It Works

- User uploads an image or the app uses a default image
- The backend resizes and processes the image using KMeans clustering
- Extracted colors and their percentages are sorted and sent to the frontend
- Colors are displayed as clickable boxes showing HEX and percentage on hover
- User can copy the HEX code by clicking a color box

---

## 🧰 Technologies

- **Python 3**
- **Flask** for web framework
- **scikit-learn** for KMeans clustering
- **Pillow (PIL)** for image processing
- **NumPy** for numerical operations
- **Bootstrap 4** for frontend styling
- **JavaScript** for interactivity (image preview and clipboard copy)

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/CelmarPA/Color_Extractor_Python_Flask
cd color_extractor_web_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000` to use the app.

---

## 📂 Project Structure

```
├── app.py               # Flask application
├── extract_colors.py    # Color extraction logic
├── requirements.txt     # Python dependencies
├── static/
│   ├── assets/
│   │   ├── css/
│   │   └── images/
│   └── uploads/         # Uploaded images stored here
└── templates/
    └── index.html       # Main HTML template
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Celmar Pereira**

- [GitHub](https://github.com/CelmarPA)
- [LinkedIn](https://linkedin.com/in/celmar-pereira-de-andrade-039830181)
- [Portfolio](https://yourportfolio.com)

---

## 💬 Feedback

Feel free to open issues or submit pull requests. Contributions are welcome!
