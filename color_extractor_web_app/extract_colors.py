# Import libraries
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import filedialog


class GetMostCommonColors:
    """
    Class to extract the most common colors from an image using KMeans clustering.

    Attributes:
        width (int): Width to resize the image for processing.
        height (int): Height to resize the image for processing.
        k (int): Number of colors (clusters) to extract.
        hex_format (str): Format string to convert RGB to HEX.
        image (PIL.Image): Loaded image object.
        rgb_colors (list): List of RGB colors from cluster centers.
        hex_colors (list): List of HEX color strings corresponding to cluster centers.
        percentages (np.array): Percentage representation of each color cluster.
    """

    def __init__(self, quant_colors=10):
        """
        Initialize the GetMostCommonColors class.

        Args:
            quant_colors (int): Number of colors (clusters) to extract from the image.
        """
        self.width = 150
        self.height = 150
        self.k = quant_colors

        self.hex_format = "#{:02x}{:02x}{:02x}"

        self.image = None
        self.rgb_colors = None
        self.hex_colors = None
        self.percentages = None

    def rgb_to_hex(self, rgb):
        """
        Convert an RGB color tuple/list to a HEX color string.

        Args:
            rgb (tuple/list): RGB color with three integer values (0-255).

        Returns:
            str: HEX color string in the format "#rrggbb".
        """
        return self.hex_format.format(*rgb)

    def get_image(self, image_file=None):
        """
        Load an image either from a file path or by opening a file dialog.

        Args:
            image_file (str or None): Path to the image file. If None, a file dialog will open.

        Side Effects:
            Sets self.image to the loaded PIL.Image object.
            If no file is selected in the dialog, the program exits.
        """
        if not image_file:
            # Open file dialog to select image
            file_path = filedialog.askopenfilename(
                title="Select an image file",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
            )

            if file_path:
                self.image = Image.open(file_path)
            else:
                print("No file selected. Exiting.")
                exit()

        else:
            # Load image from given path
            self.image = Image.open(image_file)

    def get_colors(self):
        """
        Process the loaded image to extract dominant colors and their percentages.

        Steps:
            1. Resize and convert image to RGB.
            2. Flatten pixels into a 2D array.
            3. Use KMeans to cluster pixels into 'k' colors.
            4. Calculate the percentage of pixels for each color.
            5. Sort colors by percentage in descending order.

        Returns:
            dict: Dictionary where keys are HEX color strings and values are percentages.
        """
        # Resize image for faster processing and ensure RGB mode
        resized_image = self.image.resize((self.width, self.height)).convert("RGB")

        # Convert image to numpy array of pixels, reshaped as (num_pixels, 3)
        pixels = np.array(resized_image).reshape(-1, 3)

        # Apply KMeans clustering to pixel colors
        kmeans = KMeans(n_clusters=self.k, random_state=0, n_init=10).fit(pixels)

        labels = kmeans.labels_  # Cluster labels for each pixel
        self.rgb_colors = kmeans.cluster_centers_.astype(int)  # Cluster center RGB colors

        counts = np.bincount(labels)  # Count pixels per cluster
        total_pixels = len(labels)

        # Convert cluster RGB colors to HEX strings
        self.hex_colors = [self.rgb_to_hex(color) for color in self.rgb_colors]

        # Calculate percentage of each color cluster and round to 2 decimals
        self.percentages = np.round((counts / total_pixels) * 100, 2)

        # Return dictionary of sorted colors and percentages
        colors_perc = self.sort_percentages()
        return colors_perc

    def sort_percentages(self):
        """
        Sort colors and percentages in descending order of percentage.

        Side Effects:
            Updates self.rgb_colors to be sorted accordingly.

        Returns:
            dict: Sorted dictionary of HEX colors to percentages.
        """
        # Get indices to sort percentages descending
        sorted_indices = np.argsort(-self.percentages)

        # Sort the RGB colors based on sorted indices
        self.rgb_colors = [self.rgb_colors[i] for i in sorted_indices]

        # Sort HEX colors and percentages
        sorted_hex = [self.hex_colors[i] for i in sorted_indices]
        sorted_perc = self.percentages[sorted_indices]

        # Create dictionary {HEX color: percentage}
        return {hex_color: perc for hex_color, perc in zip(sorted_hex, sorted_perc)}

    def display_palette(self):
        """
        Display the extracted color palette visually and print colors with percentages.

        This method uses matplotlib to show a row of color blocks.

        Side Effects:
            Prints color HEX and percentage to console.
            Shows a matplotlib window with color swatches.
        """
        plt.figure(figsize=(8, 4))

        # Ensure colors are sorted
        sorted_colors = self.sort_percentages()

        # Print colors and their percentages
        print("\nPalette (sorted by percentage):")
        for hex_color, perc in sorted_colors.items():
            print(f"{hex_color} - {perc:.2f}%")

        # Plot color blocks using RGB values
        for i, color in enumerate(self.rgb_colors):
            plt.subplot(1, self.k, i + 1)
            plt.axis("off")
            plt.imshow(np.ones((100, 100, 3), dtype=int) * color)

        plt.show()
