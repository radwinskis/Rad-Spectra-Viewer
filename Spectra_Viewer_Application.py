import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QPushButton, QFileDialog, QSpinBox, QDoubleSpinBox,
                             QLabel, QWidget, QComboBox)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class SpectraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main widget and set it as central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Initialize instance variables
        self.df = None
        self.wavelength_column = "Wavelength"
        self.spectrum_index = 0
        # Add the label to the toolbar layout

        # Create the figure and canvas for the plot
        # self.figure = plt.figure() ###!!!
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.toolbar = CustomToolbar(self.canvas, self)

        # Create buttons and spin boxes
        self.load_button = QPushButton("Load CSV")
        self.load_button.setToolTip('Select .csv file to load, with data in columns and wavelength (nm) as first column')
        self.previous_button = QPushButton("Previous")
        self.previous_button.setToolTip('Go to previous spectrum')
        self.next_button = QPushButton("Next")
        self.next_button.setToolTip('Go to next spectrum')
        self.x_min_spinbox = QSpinBox()
        self.x_min_spinbox.setToolTip('Set minimum x-axis value wavelength (nm)')
        self.x_max_spinbox = QSpinBox()
        self.x_max_spinbox.setToolTip('Set maximum x-axis value wavelength (nm)')
        self.y_min_spinbox = QDoubleSpinBox()
        self.y_min_spinbox.setToolTip('Set minimum y-axis reflectance value')
        self.y_max_spinbox = QDoubleSpinBox()
        self.y_max_spinbox.setToolTip('Set maximum y-axis reflectance value')

        # Configure spin boxes
        self.x_min_spinbox.setRange(350, 2500)
        self.x_min_spinbox.setValue(350)
        self.x_min_spinbox.setSingleStep(10)
        self.x_max_spinbox.setRange(350, 2500)
        self.x_max_spinbox.setValue(2500)
        self.x_max_spinbox.setSingleStep(10)
        self.y_min_spinbox.setRange(0, 1)
        self.y_min_spinbox.setSingleStep(0.01)
        self.y_max_spinbox.setRange(0, 1)
        self.y_max_spinbox.setValue(1)
        self.y_max_spinbox.setSingleStep(0.01)

        # Create labels for spin boxes
        x_min_label = QLabel("X min:")
        x_max_label = QLabel("X max:")
        y_min_label = QLabel("Y min:")
        y_max_label = QLabel("Y max:")

        # Connect signals and slots
        self.load_button.clicked.connect(self.open_csv)
        self.previous_button.clicked.connect(self.on_previous_click)
        self.next_button.clicked.connect(self.on_next_click)
        self.x_min_spinbox.valueChanged.connect(self.on_x_min_change)
        self.x_max_spinbox.valueChanged.connect(self.on_x_max_change)
        self.y_min_spinbox.valueChanged.connect(self.on_y_min_change)
        self.y_max_spinbox.valueChanged.connect(self.on_y_max_change)

        # Create the combo box to select between single or multiple spectra
        self.spectra_mode_combo = QComboBox()
        self.spectra_mode_combo.addItem("Single")
        self.spectra_mode_combo.addItem("Multiple")

        # Create the combo box to select whether to use vertical reference bar
        self.reference_bar = QComboBox()
        self.reference_bar.addItem("OFF")
        self.reference_bar.addItem("ON")
        reference_bar_label = QLabel("Vertical Reference Line")
        font_vertical_line = QFont("Century Gothic", 8)
        reference_bar_label.setFont(font_vertical_line)
        self.reference_bar.currentTextChanged.connect(self.on_reference_bar_change)
        self.reference_bar_status = False
        self.reference_bar_wavelength = QSpinBox()
        self.reference_bar_wavelength.setRange(350, 2500)
        self.reference_bar_wavelength.setValue(1400)
        self.reference_bar_wavelength.setSingleStep(1)
        self.reference_bar_wavelength.valueChanged.connect(self.on_reference_bar_wavelength_change)
        self.reference_bar_wavelength_value = 1400

        # Create the spin box for the number of spectra to show at a time
        self.num_spectra_spinbox = QSpinBox()
        self.num_spectra_spinbox.setRange(1, 10)
        self.num_spectra_spinbox.setValue(5)
        self.num_spectra_spinbox.setSingleStep(1)
        self.num_spectra_spinbox.setDisabled(False)
        # Connect signals and slots
        self.spectra_mode_combo.currentTextChanged.connect(self.on_spectra_mode_change)
        self.num_spectra_spinbox.valueChanged.connect(self.on_num_spectra_change)

        #Create the combo box to select grid on or off
        self.grid_status = QComboBox()
        self.grid_status.addItem("ON")
        self.grid_status.addItem("OFF")
        grid_status_label = QLabel("Grid:")
        self.grid_status.currentTextChanged.connect(self.on_grid_status_change)
        self.grid_boolean_status = True

        #Widgets for adjusting tick parameters
        self.x_ticks_major_multiple = 200
        self.x_ticks_minor_multiple = 50
        self.y_ticks_major_multiple = 0.2
        self.y_ticks_minor_multiple = 0.05
        self.xt_maj_spinbox = QSpinBox()
        self.xt_maj_spinbox.setRange(50, 400)
        self.xt_maj_spinbox.setValue(200)
        self.xt_maj_spinbox.setSingleStep(1)
        self.xt_maj_spinbox.setDisabled(False)

        self.xt_min_spinbox = QSpinBox()
        self.xt_min_spinbox.setRange(1, 200)
        self.xt_min_spinbox.setValue(50)
        self.xt_min_spinbox.setSingleStep(1)
        self.xt_min_spinbox.setDisabled(False)

        # self.yt_maj_spinbox = QSpinBox()
        # self.yt_maj_spinbox.setRange(0.1, 0.5)
        # self.yt_maj_spinbox.setValue(0.2)
        # self.yt_maj_spinbox.setSingleStep(0.1)
        # self.yt_maj_spinbox.setDisabled(False)

        # self.yt_min_spinbox = QSpinBox()
        # self.yt_min_spinbox.setRange(0.01, 0.1)
        # self.yt_min_spinbox.setValue(0.05)
        # self.yt_min_spinbox.setSingleStep(0.01)
        # self.yt_min_spinbox.setDisabled(False)

        self.xt_maj_spinbox.valueChanged.connect(self.on_xt_maj_change)
        self.xt_min_spinbox.valueChanged.connect(self.on_xt_min_change)
        # self.yt_maj_spinbox.valueChanged.connect(self.on_yt_maj_change)
        # self.yt_min_spinbox.valueChanged.connect(self.on_yt_min_change)
        # Create layouts
        main_layout = QVBoxLayout()
        # Create the label with your custom text
        label = QLabel("Rad Spectra Viewer")
        font = QFont("Century Gothic", 8)
        label.setFont(font)
        # Create a horizontal layout for the label and toolbar
        toolbar_layout = QHBoxLayout()

        # Add the label and toolbar to the horizontal layout
        toolbar_layout.addWidget(label)
        toolbar_layout.addWidget(self.toolbar)
        toolbar_layout.addWidget(QLabel('X Ticks Major Multiple'))
        toolbar_layout.addWidget(self.xt_maj_spinbox)
        toolbar_layout.addWidget(QLabel('X Ticks Minor Multiple'))
        toolbar_layout.addWidget(self.xt_min_spinbox)
        toolbar_layout.addWidget(reference_bar_label)
        toolbar_layout.addWidget(self.reference_bar)
        toolbar_layout.addWidget(self.reference_bar_wavelength)
        self.reference_bar_wavelength.setHidden(True)
        # toolbar_layout.addWidget(QLabel('Y Ticks Major Multiple'))
        # toolbar_layout.addWidget(self.yt_maj_spinbox)
        # toolbar_layout.addWidget(QLabel('Y Ticks Minor Multiple'))
        # toolbar_layout.addWidget(self.yt_min_spinbox)

        # Add the toolbar layout to the main layout
        main_layout.addLayout(toolbar_layout)

        # # Add canvas to the main layout
        main_layout.addWidget(self.canvas)

        bottom_layout = QHBoxLayout()
        # bottom_layout.addStretch()
        bottom_layout.addWidget(self.load_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.previous_button)
        bottom_layout.addWidget(self.next_button)
        bottom_layout.addStretch()
        label2 = QLabel("# of Spectra Shown")
        font2 = QFont("Century Gothic", 6)
        label2.setFont(font2)
        bottom_layout.addWidget(label2)
        bottom_layout.addWidget(self.spectra_mode_combo)
        bottom_layout.addWidget(self.num_spectra_spinbox)
        self.num_spectra_spinbox.setHidden(True)


        main_layout.addLayout(bottom_layout)

        # top_right_layout = QHBoxLayout()
        # top_right_layout.addStretch()
        # top_right_layout.addWidget(self.spectra_mode_combo)
        # top_right_layout.addWidget(self.num_spectra_spinbox)

        right_layout = QGridLayout()
        right_layout.addWidget(x_min_label, 0, 0)
        right_layout.addWidget(self.x_min_spinbox, 0, 1)
        right_layout.addWidget(x_max_label, 1, 0)
        right_layout.addWidget(self.x_max_spinbox, 1, 1)
        right_layout.addWidget(y_min_label, 2, 0)
        right_layout.addWidget(self.y_min_spinbox, 2, 1)
        right_layout.addWidget(y_max_label, 3, 0)
        right_layout.addWidget(self.y_max_spinbox, 3, 1)
        right_layout.addWidget(grid_status_label, 4, 0)
        right_layout.addWidget(self.grid_status, 4, 1)
        # right_layout.addWidget(QLabel('X Ticks\nMajor Multiple'), 5, 0)
        # right_layout.addWidget(self.xt_maj_spinbox, 5, 1)

        main_right_layout = QVBoxLayout()
        main_right_layout.addStretch()
        main_right_layout.addLayout(right_layout)
        main_right_layout.addStretch()

        outer_layout = QHBoxLayout()
        outer_layout.addLayout(main_layout)
        outer_layout.addLayout(main_right_layout)

        main_widget.setLayout(outer_layout)

        self.setWindowTitle("Spectra Viewer")
        self.setGeometry(100, 100, 800, 600)

    def on_spectra_mode_change(self, mode):
        if mode == "Multiple":
            self.num_spectra_spinbox.setDisabled(False)
            self.num_spectra_spinbox.setHidden(False)
        else:
            self.num_spectra_spinbox.setDisabled(True)
            self.num_spectra_spinbox.setHidden(True)
        self.plot_spectrum()

    def on_num_spectra_change(self, value):
        self.plot_spectrum()

    def on_grid_status_change(self, status):
        if self.grid_status.currentText() == "ON":
            self.grid_boolean_status = True
        else: 
            self.grid_boolean_status = False
        self.plot_spectrum()
    
    def on_reference_bar_change(self, status):
        if self.reference_bar.currentText() == "ON":
            self.reference_bar_status = True
            self.reference_bar_wavelength.setHidden(False)
        else:
            self.reference_bar_status = False
            self.reference_bar_wavelength.setHidden(True)
        self.plot_spectrum()

    def on_reference_bar_wavelength_change(self, wavelength):
        self.reference_bar_wavelength_value = self.reference_bar_wavelength.value()
        self.plot_spectrum()

    def on_xt_maj_change(self, value):
        self.x_ticks_major_multiple = self.xt_maj_spinbox.value()
        self.plot_spectrum()
    def on_xt_min_change(self, value):
        self.x_ticks_minor_multiple = self.xt_min_spinbox.value()
        self.plot_spectrum()
    def on_yt_maj_change(self, value):
        self.y_ticks_major_multiple = self.yt_maj_spinbox.value()
        self.plot_spectrum()
    def on_yt_min_change(self, value):
        self.y_ticks_minor_multiple = self.yt_min_spinbox.value()
        self.plot_spectrum()

    def open_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.df = pd.read_csv(file_name)
            self.plot_spectrum()

    # def plot_spectrum(self):
    #     if self.df is None:
    #         return
    #     # fig, ax = plt.subplots(figsize=(7, 5))
    #     plt.clf()
    #     num_spectra = 1 if self.spectra_mode_combo.currentText() == "Single" else self.num_spectra_spinbox.value()

    #     for i in range(num_spectra):
    #         if self.spectrum_index + i < len(self.df.columns) - 1:
    #             plt.plot(self.df[self.wavelength_column], self.df.iloc[:, self.spectrum_index + i + 1],
    #                     label=self.df.columns[self.spectrum_index + 1 + i])
    #     plt.xlim(self.x_min_spinbox.value(), self.x_max_spinbox.value())
    #     plt.ylim(self.y_min_spinbox.value(), self.y_max_spinbox.value())
    #     plt.xlabel("Wavelength (nm)", fontsize=20)
    #     plt.ylabel("Reflectance", fontsize=20)
    #     plt.legend()
    #     plt.grid(True)
    #     self.canvas.draw()

    def plot_spectrum(self):
        if self.df is None:
            return
        # self.figure, self.ax = plt.subplots()
        self.ax.clear()
        num_spectra = self.num_spectra_spinbox.value() if self.spectra_mode_combo.currentText() == "Multiple" else 1
        for i in range(num_spectra):
            if self.spectrum_index + i < len(self.df.columns) - 1:
                self.ax.plot(self.df[self.wavelength_column], self.df.iloc[:, self.spectrum_index + i + 1],
                            label=self.df.columns[self.spectrum_index + 1 + i])
        if self.reference_bar_status == True:
            self.ax.axvline(self.reference_bar_wavelength_value, color='darkslategrey')
        else: None
        self.ax.set_xlim(self.x_min_spinbox.value(), self.x_max_spinbox.value())
        self.ax.set_ylim(self.y_min_spinbox.value(), self.y_max_spinbox.value())
        self.ax.set_xlabel("Wavelength (nm)", fontsize=20)
        self.ax.set_ylabel("Reflectance", fontsize=20)
        self.ax.legend()
        if self.grid_boolean_status == True:
            self.ax.grid(alpha=0.5)
        else: self.ax.grid(False)

        # Update the major and minor ticks
        self.ax.xaxis.set_major_locator(plt.MultipleLocator(self.x_ticks_major_multiple))
        self.ax.xaxis.set_minor_locator(plt.MultipleLocator(self.x_ticks_minor_multiple))
        self.ax.yaxis.set_major_locator(plt.MultipleLocator(self.y_ticks_major_multiple))
        self.ax.yaxis.set_minor_locator(plt.MultipleLocator(self.y_ticks_minor_multiple))

        self.canvas.draw()

    def on_previous_click(self):
        num_spectra = self.num_spectra_spinbox.value() if self.spectra_mode_combo.currentText() == "Multiple" else 1
        self.spectrum_index = max(0, self.spectrum_index - num_spectra)
        self.plot_spectrum()

    def on_next_click(self):
        num_spectra = self.num_spectra_spinbox.value() if self.spectra_mode_combo.currentText() == "Multiple" else 1
        self.spectrum_index = min(len(self.df.columns) - (num_spectra + 1), self.spectrum_index + num_spectra)
        self.plot_spectrum()

    def on_x_min_change(self, value):
        self.plot_spectrum()

    def on_x_max_change(self, value):
        self.plot_spectrum()

    def on_y_min_change(self, value):
        self.plot_spectrum()

    def on_y_max_change(self, value):
        self.plot_spectrum()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Set the stylesheet for a custom appearance
    style_sheet = """
    QWidget {
        font-size: 14pt;
        background-color: #FAFAFA;
        color: #272727;
    }
    QLabel {
        color: #272727;
    }
    QPushButton {
        color: #FAFAFA;
        background-color: #546E7A;
        border: 0.5px solid #004d40;
        border-radius: 3px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #B0BEC5;
    }
    QPushButton:pressed {
        background-color: #CFD8DC;
    }
    QSpinBox, QDoubleSpinBox {
        background-color: #FAFAFA;
        color: #272727;
        border: 0.5px solid #004d40;
        border-radius: 3px;
        padding: 0 5px;
    }
    QComboBox {
        background-color: #FAFAFA;
        color: #272727;       
    }
    """
    app.setStyleSheet(style_sheet)

    mainWin = SpectraApp()
    mainWin.show()
    sys.exit(app.exec_())

