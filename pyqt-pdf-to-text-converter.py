import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QLabel, QMessageBox, QAbstractItemView, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyPDF2 import PdfReader

class PdfListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith('.pdf') and os.path.isfile(path):
                    if not self.findItems(path, Qt.MatchExactly):
                        self.addItem(path)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

class ConverterThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(int)

    def __init__(self, files, output_folder):
        super().__init__()
        self.files = files
        self.output_folder = output_folder

    def run(self):
        count = 0
        for index, pdf_path in enumerate(self.files):
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            try:
                reader = PdfReader(pdf_path)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text() or "")
                txt_content = "\n".join(text)
                txt_path = os.path.join(self.output_folder, base_name + '.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
                count += 1
            except Exception as e:
                print(f"Failed to convert {pdf_path}: {e}")
            self.progress.emit(index + 1, base_name)
        self.finished.emit(count)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to TXT Converter")
        self.resize(600, 450)

        self.pdf_list = PdfListWidget()
        self.pdf_list.setSelectionMode(QListWidget.ExtendedSelection)

        self.folder_label = QLabel("Output Folder: Not selected")
        self.status_label = QLabel("")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        browse_btn = QPushButton("Select Output Folder")
        browse_btn.clicked.connect(self.select_folder)

        convert_btn = QPushButton("Convert PDFs to TXT")
        convert_btn.clicked.connect(self.convert_pdfs)

        clear_btn = QPushButton("Clear List")
        clear_btn.clicked.connect(self.pdf_list.clear)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Drag and drop PDF files below:"))
        layout.addWidget(self.pdf_list)
        layout.addWidget(self.folder_label)
        layout.addWidget(browse_btn)
        layout.addWidget(convert_btn)
        layout.addWidget(clear_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.output_folder = None
        self.thread = None

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.folder_label.setText(f"Output Folder: {folder}")

    def convert_pdfs(self):
        if not self.output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please select an output folder.")
            return

        total = self.pdf_list.count()
        if total == 0:
            QMessageBox.warning(self, "No Files", "Please add PDF files to convert.")
            return

        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Converting...")

        files = [self.pdf_list.item(i).text() for i in range(total)]
        self.thread = ConverterThread(files, self.output_folder)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_done)
        self.thread.start()

    def update_progress(self, value, filename):
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Processing '{filename}' ({value}/{self.progress_bar.maximum()})")

    def conversion_done(self, count):
        self.status_label.setText("Conversion complete.")
        QMessageBox.information(self, "Conversion Complete", f"Converted {count} file(s) successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())