import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QSplitter, QTextEdit
from PyQt5.QtCore import Qt
import pydicom

class DICOMViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        self.setWindowTitle('DICOM Viewer')
        self.setGeometry(300, 300, 800, 600)

        # Create layout
        layout = QVBoxLayout()

        # Instruction label
        self.label = QLabel("Drag and drop DICOM files or folders here")
        layout.addWidget(self.label)

        # Splitter for tree and details
        splitter = QSplitter(Qt.Horizontal)

        # Tree widget for studies/series
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("DICOM Structure")
        self.tree.itemSelectionChanged.connect(self.onItemSelected)
        splitter.addWidget(self.tree)

        # Text edit for DICOM tags
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        splitter.addWidget(self.details)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                if path.lower().endswith('.dcm') or path.lower().endswith('.dicom'):
                    files.append(path)
            elif os.path.isdir(path):
                for root, dirs, files_in_dir in os.walk(path):
                    for file in files_in_dir:
                        if file.lower().endswith('.dcm') or file.lower().endswith('.dicom'):
                            files.append(os.path.join(root, file))
        self.loadDICOM(files)

    def loadDICOM(self, files):
        studies = {}
        for file in files:
            try:
                ds = pydicom.dcmread(file)
                study_uid = ds.get('StudyInstanceUID', 'None')
                series_uid = ds.get('SeriesInstanceUID', 'None')
                if study_uid not in studies:
                    studies[study_uid] = {}
                if series_uid not in studies[study_uid]:
                    studies[study_uid][series_uid] = []
                studies[study_uid][series_uid].append((file, ds))
            except Exception as e:
                print(f"Error reading {file}: {e}")

        self.populateTree(studies)

    def populateTree(self, studies):
        self.tree.clear()
        for study_uid, series_dict in studies.items():
            study_item = QTreeWidgetItem([f"Study: {study_uid}"])
            self.tree.addTopLevelItem(study_item)
            for series_uid, file_list in series_dict.items():
                series_item = QTreeWidgetItem([f"Series: {series_uid}"])
                study_item.addChild(series_item)
                for file_path, ds in file_list:
                    file_item = QTreeWidgetItem([os.path.basename(file_path)])
                    file_item.setData(0, Qt.UserRole, (file_path, ds))
                    series_item.addChild(file_item)

    def onItemSelected(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            data = item.data(0, Qt.UserRole)
            if data:
                file_path, ds = data
                self.displayTags(ds)

    def displayTags(self, ds):
        tags = []
        for elem in ds:
            if elem.tag != (0x7fe0, 0x0010):  # Skip pixel data
                tags.append(f"{elem.name}: {str(elem.value)}")
        self.details.setText('\n'.join(tags))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DICOMViewer()
    window.show()
    sys.exit(app.exec_())