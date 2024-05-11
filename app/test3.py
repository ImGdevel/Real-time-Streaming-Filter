import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt

def edit_image(input_image_path, output_image_path, width, height, x_offset=0, y_offset=0, scale=1):
    # Load input image
    original_image = QPixmap(input_image_path)

    # Scale the image
    scaled_image = original_image.scaled(original_image.width() * scale, original_image.height() * scale, Qt.KeepAspectRatio)

    # Create a new image with transparent background
    new_image = QImage(width, height, QImage.Format_ARGB32)
    new_image.fill(Qt.transparent)

    # Calculate the position to paste the scaled image
    paste_x = (width - scaled_image.width()) // 2 + x_offset
    paste_y = (height - scaled_image.height()) // 2 + y_offset

    # Create a QPainter object for the new image
    painter = QPainter(new_image)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(paste_x, paste_y, scaled_image)
    painter.end()

    # Save the edited image
    new_image.save(output_image_path, "PNG")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Open file dialog to select an image
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
    file_dialog.setViewMode(QFileDialog.Detail)
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    if file_dialog.exec_():
        selected_files = file_dialog.selectedFiles()
        input_image_path = selected_files[0]

        # Define output path
        output_image_path = "output_image.png"

        # Define the desired width and height
        desired_width = 400
        desired_height = 400

        # Define the offsets for image positioning (default: 0, 0)
        x_offset = 100
        y_offset = -100

        # Define the scale factor (default: 1)
        scale = 4

        # Edit the image
        edit_image(input_image_path, output_image_path, desired_width, desired_height, x_offset, y_offset, scale)

    sys.exit(app.exec_())
