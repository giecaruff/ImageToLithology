import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QDoubleValidator
from collections import Counter
from PIL import Image
import pandas as pd
import math
import numpy as np

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Input fields
        self.top_depth_label = QLabel('Top Depth:')
        self.top_depth_input = QLineEdit(self)
        self.top_depth_input.setValidator(QDoubleValidator())
        
        self.bottom_depth_label = QLabel('Bottom Depth:')
        self.bottom_depth_input = QLineEdit(self)
        self.bottom_depth_input.setValidator(QDoubleValidator())
        
        self.step_label = QLabel('Step:')
        self.step_input = QLineEdit(self)
        self.step_input.setValidator(QDoubleValidator())
        
        self.path_color_label = QLabel('Path to Colors CSV:')
        self.path_color_input = QLineEdit(self)
        self.path_color_button = QPushButton('Browse', self)
        self.path_color_button.clicked.connect(self.browseColorCSV)
        
        self.image_path_label = QLabel('Image Path:')
        self.image_path_input = QLineEdit(self)
        self.image_path_button = QPushButton('Browse', self)
        self.image_path_button.clicked.connect(self.browseImage)
        
        self.output_path_label = QLabel('Output Path:')
        self.output_path_input = QLineEdit(self)
        self.output_path_button = QPushButton('Browse', self)
        self.output_path_button.clicked.connect(self.browseOutput)

        # Run button
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_processing)
        
        # Adding widgets to layout
        layout.addWidget(self.top_depth_label)
        layout.addWidget(self.top_depth_input)
        layout.addWidget(self.bottom_depth_label)
        layout.addWidget(self.bottom_depth_input)
        layout.addWidget(self.step_label)
        layout.addWidget(self.step_input)
        layout.addWidget(self.path_color_label)
        layout.addWidget(self.path_color_input)
        layout.addWidget(self.path_color_button)
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.image_path_input)
        layout.addWidget(self.image_path_button)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_input)
        layout.addWidget(self.output_path_button)
        layout.addWidget(self.run_button)
        
        self.setLayout(layout)
        self.setWindowTitle('Image Processor')
        self.show()
    
    def browseColorCSV(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Colors CSV', '', 'CSV Files (*.csv)', options=options)
        if file_path:
            self.path_color_input.setText(file_path)
    
    def browseImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'PNG Files (*.png);;All Files (*)', options=options)
        if file_path:
            self.image_path_input.setText(file_path)
    
    def browseOutput(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Output CSV', '', 'CSV Files (*.csv)', options=options)
        if file_path:
            self.output_path_input.setText(file_path)
    
    def run_processing(self):
        top_depth = float(self.top_depth_input.text())
        bottom_depth = float(self.bottom_depth_input.text())
        step_text = self.step_input.text()
        step = float(step_text) if step_text else False
        path_color = self.path_color_input.text()
        image_path = self.image_path_input.text()
        output_path = self.output_path_input.text()

        self.process_image(top_depth, bottom_depth, step, path_color, image_path, output_path)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def euclidean_distance(self, c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    def closest_color_code(self, rgb, color_data):
        min_dist = float('inf')
        closest_code = None
        
        for _, row in color_data.iterrows():
            color = self.hex_to_rgb(row['COR'])
            dist = self.euclidean_distance(rgb, color)
            if dist < min_dist:
                min_dist = dist
                closest_code = row['CODIGO']
                
        return closest_code

    def is_dark_color(self, rgba, threshold=50):
        r, g, b, a = rgba
        return a == 0 or (r < threshold and g < threshold and b < threshold)

    def most_common_color_in_row(self, image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            colors_per_row = []

            for y in range(height):
                row_colors = [img.getpixel((x, y)) for x in range(width)]
                row_colors = [color for color in row_colors if not self.is_dark_color(color)]
                counter = Counter(row_colors)
                most_common = counter.most_common(1)
                if most_common:
                    colors_per_row.append(most_common[0][0][:3])
                else:
                    colors_per_row.append(None)
            return colors_per_row

    def process_image(self, top_depth, bottom_depth, step, path_color, image_path, output_path):
        color_data = pd.read_csv(path_color)
        dominant_row_colors = self.most_common_color_in_row(image_path)

        last_valid_color = None
        codes_for_rows = []
        for color in dominant_row_colors:
            if color is None and last_valid_color:
                color = last_valid_color
            if color:
                last_valid_color = color
            code = self.closest_color_code(color, color_data) if color else None
            codes_for_rows.append(code)

        interval = (bottom_depth - top_depth) / len(codes_for_rows)
        depths = [top_depth + i * interval for i in range(len(codes_for_rows))]

        if step:
            new_depth = np.arange(top_depth, bottom_depth, step)
            new_code = np.interp(new_depth, depths, codes_for_rows)

            df = pd.DataFrame({
                'Depth': new_depth,
                'Code': new_code
            })
        else:
            df = pd.DataFrame({
                'Depth': depths,
                'Code': codes_for_rows
            })

        df.to_csv(output_path, index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    sys.exit(app.exec_())