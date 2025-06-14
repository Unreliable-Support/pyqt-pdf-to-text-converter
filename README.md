# PDF to TXT Converter GUI

A simple and efficient desktop application built with Python and PyQt5 for batch converting text-based PDF files into plain TXT files. The application features a clean user interface with drag-and-drop support for easy file handling.

This project demonstrates proficiency in building robust desktop applications with industry-standard GUI toolkits like PyQt5 and handling background tasks with `QThread` for a smooth user experience.

---

### Live Demo

A short video showcasing the application's features: dragging and dropping PDF files, selecting an output folder, running the conversion process, and viewing the resulting TXT files.

[![PDF to TXT Converter Demo](https://img.youtube.com/vi/CdTIBUgpRcU/0.jpg)](https://www.youtube.com/watch?v=CdTIBUgpRcU)

**[Click here to watch the full demo on YouTube](https://www.youtube.com/watch?v=CdTIBUgpRcU)**

---

### The Problem
Extracting plain text from multiple PDF files can be a tedious task, often requiring users to open each file, copy the content, and paste it into a text editor. This is inefficient for handling documents in bulk.

### The Solution
This application provides a straightforward tool to solve this problem. It allows users to:
1.  **Drag and drop** multiple PDF files directly into the application window.
2.  Select a destination folder for the output.
3.  Convert all added PDFs into TXT files with a single click.
4.  Monitor the progress in real-time with a progress bar and status updates.

### Key Technical Features
*   **Modern Desktop GUI:** Built using `PyQt5`, a powerful and widely-used framework for creating professional desktop applications.
*   **Intuitive User Experience:** Implements **drag-and-drop** functionality for adding files, making the application easy and fast to use.
*   **Asynchronous Processing:** Uses `QThread` and Qt's signal/slot mechanism to perform the file conversion in a background thread, ensuring the main application window remains responsive and never freezes.
*   **Real-Time Feedback:** A progress bar and status label keep the user informed about the conversion process.
*   **Efficient Text Extraction:** Leverages the `PyPDF2` library for reliable text extraction from standard, text-based PDF files.

### Technology Stack
*   **Python 3**
*   **PyQt5** (for the GUI and threading)
*   **PyPDF2** (for PDF text extraction)

### Installation & Usage

**1. Clone the Repository & Install Python Libraries:**
```bash
# Clone this repository
git clone https://github.com/Unreliable-Support/pyqt-pdf-to-text-converter.git

# Navigate to the project directory
cd pyqt-pdf-to-text-converter

# Install required Python libraries
pip install -r requirements.txt
