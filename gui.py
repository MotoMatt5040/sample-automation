import traceback
import os
from typing import Callable, Optional
import logging
import sys

from dotenv import load_dotenv

load_dotenv()

import PyQt6.QtWidgets as qtw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
import pandas as pd
import json

from tkinter import filedialog
from vendor import Tarrance, Baselice, I360, RNC
from logging_format import CustomFormatter
from vendors_ import Vendor, read_file

v = Vendor()

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - Line: %(lineno)d - %(message)s",
# )
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

logger.debug('Enabled')
logger.info('Enabled')
logger.warning('Enabled')
logger.error('Enabled')
logger.critical('Enabled')

def create_button(
        text: str,
        function: Optional[Callable] = None,
        size: tuple[int, int] = None,
        checkable: bool = False,
        border_radius: int = 10,
        padding: int = 10
):
    button = qtw.QPushButton(text)
    if function is not None:
        button.clicked.connect(function)
    button.setCheckable(checkable)

    if size:
        button.setFixedSize(*size)

    button.setStyleSheet(
        "QPushButton {"
            "background-color: #333;  /* Background color */"
            "color: white;            /* Text color */"
            f"border-radius: {border_radius}px;     /* Rounded corners */"
            f"padding: {padding}px;           /* Padding */"
            "font-size: 12px;         /* Font size */"
        "}"
        "QPushButton:checked {"
            "background-color: #800080;     /* Background color when checked */"
        "}"
        "QPushButton:hover {"
            "background-color: #444;  /* Background color when hovered */"
        "}"
        "QPushButton:pressed {"
            "background-color: #555;  /* Background color when pressed */"
        "}"
        "QPushButton:disabled {"
            "background-color: #300; "
            "color: white;"
        "}"
    )
    return button


def create_combo_box(options: list[str], size: tuple[int, int] = None):
    combo_box = qtw.QComboBox()

    for option in options:
        combo_box.addItem(option)

    if size:
        combo_box.setFixedSize(*size)

    combo_box.setStyleSheet(
        """
        QComboBox {
            background-color: #333;  /* Background color */
            color: white;            /* Text color */
            border: 1px solid #555;  /* Border */
            border-radius: 5px;      /* Rounded corners */
            padding: 5px;            /* Padding */
            font-size: 12px;         /* Font size */
        }
        QComboBox::drop-down {
            subcontrol-position: right center;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #555;
            border-left-style: solid;
        }
        QComboBox::down-arrow {
            image: url(dropdown_arrow.png); /* Arrow icon */
            width: 12px;                        /* Width of the arrow icon */
            height: 12px;                       /* Height of the arrow icon */
        }
        QComboBox::drop-down:hover {
            background-color: #444;             /* Drop-down background color on hover */
        }
        QComboBox::item {
            padding: 5px;  /* Padding for each item */
        }
        QComboBox::item:selected {
            background-color: #666;             /* Background color of selected item */
        }
        QComboBox QAbstractItemView {
            background-color: #222;             /* Background color of the drop-down menu */
            color: white;                       /* Text color of items */
            selection-background-color: #555;   /* Background color of selected item */
            selection-color: white;             /* Text color of selected item */
            border: 1px solid #555;             /* Border of the drop-down menu */
            border-radius: 5px;                 /* Rounded corners */
            padding: 5px;                       /* Padding around items */
        }
        QComboBox QAbstractItemView::item {
            padding: 10px;                      /* Padding of items in the drop-down menu */
            font-size: 12px;                    /* Font size */
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #555;             /* Background color of selected item */
            color: white;                       /* Text color of selected item */
        }
        """
    )

    return combo_box


def create_radio_button(text: str, size: tuple[int, int] = None):
    radio_button = qtw.QRadioButton(text)

    if size:
        radio_button.setFixedSize(*size)

    radio_button.setStyleSheet(
        """
        QRadioButton {
            background-color: #333;  /* Background color */
            color: white;            /* Text color */
            border: 1px solid #555;  /* Border */
            border-radius: 5px;      /* Rounded corners */
            font-size: 12px;         /* Font size */
            text-align: center;      /* Center text */
        }
        QRadioButton::indicator {
            width: 0px;   /* Hide the default radio button indicator */
            height: 0px;
        }
        QRadioButton::checked {
            background-color: #800080; /* Background color when checked */
        }
        QRadioButton:hover {
            background-color: #444;  /* Background color when hovered */
        }
        QRadioButton:pressed {
            background-color: #555;  /* Background color when pressed */
        }
        """
    )

    return radio_button


def handle_button_clicked(button_group, button):
    logger.debug(f"Button clicked: {button.text()}")
    for btn in button_group.buttons():
        if btn != button:
            btn.setChecked(False)


def get_widgets_from_layout(layout):
    widgets = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item and item.widget():
            widgets.append(item.widget())
    return widgets


def get_widgets_from_grid(grid):
    rows = grid.rowCount()
    columns = grid.columnCount()

    for row in range(rows):
        for col in range(columns):
            item = grid.itemAtPosition(row, col)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    logger.debug(f"Widget in position ({row}, {col}): {widget}")
                else:
                    logger.debug(f"No widget in position ({row}, {col})")
            else:
                logger.debug(f"No item in position ({row}, {col})")


def blank_widget():
    bw = qtw.QWidget()
    bw.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Expanding)  # Expanding to take available space
    return bw


def delete_layout(layout):
    if layout is None:
        return

    # Remove all widgets and delete them
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            widget = item.widget()
            widget.deleteLater()
        elif item.layout():
            delete_layout(item.layout())

    # Delete the layout itself
    layout.deleteLater()


def create_candidate_names_text_box():
    candidate_names_text_box = qtw.QTextEdit()
    candidate_names_text_box.setLineWrapMode(qtw.QTextEdit.LineWrapMode.NoWrap)
    candidate_names_text_box.setPlaceholderText("Enter candidate names separated by new lines")
    candidate_names_text_box.setReadOnly(False)
    candidate_names_text_box.setFixedSize(200, 100)

    return candidate_names_text_box


def create_header_layout():
    ...


def get_data():
    ...


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.header_layout = None
        self.index_of_main_layout = None
        self.index_of_vendor_layout = None
        self.radio_widgets = None
        self.vendor = 'TAR'
        self.path_text_box = None
        self.join_path_text_box = None
        self.headers = None
        self.header_widget_container = None
        self.header_text_boxes = None
        self.header_checkboxes = None
        self.setWindowTitle("Sample Automation")
        self.setLayout(qtw.QHBoxLayout())
        # self.resize(1080, 720)
        self.set_background_color("black")

        # self.vendor_side_panel()
        self.main_panel()

        self.show()

    def adjust_stretch(self, target: str, stretch: int):
        targets = {'vendor': self.index_of_vendor_layout, 'main': self.index_of_main_layout}
        self.layout().setStretch(targets[target], stretch)

    def get_data(self):
        logger.debug("Getting data")
        if not self.path_text_box.text():
            logger.warning("No file path selected")
            return
        if not self.join_path_text_box.text():
            v.df = read_file(self.path_text_box.text())
        else:
            v.merge_df((self.path_text_box.text(), self.join_path_text_box.text()))
        logger.debug('Data read, creating headers widget')
        self.create_headers_widget()
        logger.debug('Headers widget created, adding blank widget to layout')
        self.layout().addWidget(blank_widget())
        logger.debug('Blank widget added to layout')
        logger.debug(v.headers)

    def clear_layout(self):
        if self.header_layout is None:
            return

        while self.layout().count():
            item = self.layout().takeAt(2)
            logger.debug(f"deleting: {item}")
            if item is not None:
                if item.widget():
                    widget = item.widget()
                    widget.deleteLater()
                elif item.layout():
                    delete_layout(item.layout())
            else:
                break

        self.adjust_stretch('main', 1)

    def handle_radio_click(self, radio_button: qtw.QRadioButton, items_to_modify: tuple[qtw.QPushButton, qtw.QLineEdit]):

        logger.debug(f"Radio button clicked: {radio_button.text()}")
        self.clear_layout()

        if not radio_button.text() == 'MIXED':
            logger.debug('Join pathing disabled')
            items_to_modify[0].setDisabled(True)
            items_to_modify[1].setDisabled(True)
            items_to_modify[1].setPlaceholderText("Disabled for single mode")
            items_to_modify[1].clear()
            return

        logger.debug('Join pathing enabled')
        items_to_modify[0].setDisabled(False)
        items_to_modify[1].setDisabled(False)
        items_to_modify[1].setPlaceholderText("Select a file to join")

    def handle_check_headers(self):
        logger.debug(f"Checking headers for {self.vendor} at {self.path_text_box.text()}")
        self.get_data()

    def handle_process_data(self):
        logger.debug(f"Processing data for {self.vendor}")

    def create_headers_widget(self):
        # Create a new layout for column headers
        grid_layout = qtw.QGridLayout()

        # Create a container widget for column headers
        header_container = qtw.QWidget()
        header_container.setMaximumWidth(500)
        header_container.setLayout(grid_layout)

        # Create a scroll area
        scroll_area = qtw.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(header_container)

        # Clear any existing column header widgets
        # logger.debug(f"self.header_widget_contianer: {self.header_widget_container}")
        # if self.header_layout is not None:
        #     logger.debug(f"self.header_widget_container: {self.header_widget_container}")
        #     logger.debug('Removing existing header layout')
        #
        #     # Remove widgets from the existing layout
        #     while self.header_layout.count():
        #         item = self.header_layout.takeAt(0)  # Take the item at index 0
        #         if item.widget():
        #             item.widget().deleteLater()  # Delete widget
        #         elif item.layout():
        #             delete_layout(item.layout())  # Recursively delete nested layouts
        #
        #     # Remove the layout from the parent widget
        #     self.layout().removeItem(self.header_layout)
        #     logger.debug('Removed existing header layout from parent widget')
        #
        #     # Delete the layout itself
        #     self.header_layout.deleteLater()
        #     self.header_layout = None  # Reset the layout reference
        #     logger.debug('Existing header layout deleted')

        # Add the scroll area to the main layout
        self.header_layout = qtw.QHBoxLayout()
        self.header_widget_container = scroll_area
        self.header_widget_container.setMinimumWidth(500)
        self.header_widget_container.setMaximumWidth(1000)
        # self.layout().addWidget(self.header_widget_container)
        logger.debug('Adding header widget container to layout')
        self.add_to_layout(self.header_widget_container, layout=self.header_layout, anchor='left')
        self.header_layout.addWidget(blank_widget())
        self.layout().addLayout(self.header_layout, stretch=1)

        # Create and add the "Sample Frame Headers" label
        title_label = qtw.QLabel("Sample Headers")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        grid_layout.addWidget(title_label, 0, 0, 1, 3)  # Span across the first three columns

        # Add labels, checkboxes, and text boxes for each column header in the DataFrame
        self.header_text_boxes = {}  # Dictionary to keep track of text boxes
        # self.header_checkboxes = {}  # Dictionary to keep track of checkboxes

        for index, column in enumerate(v.headers):
            checkbox = qtw.QCheckBox()
            label = qtw.QLabel(column)
            text_box = qtw.QLineEdit()
            text_box.setText(column)  # Set the initial text to the column name
            label.setStyleSheet("color: white;")
            text_box.setStyleSheet("background-color: #333; color: white; border: 1px solid #555;")

            grid_layout.addWidget(checkbox, index + 1, 0)  # Add checkbox to the first column
            grid_layout.addWidget(label, index + 1, 1)  # Add label to the second column
            grid_layout.addWidget(text_box, index + 1, 2)  # Add text box to the third column

            # Store the text box and checkbox in dictionaries
            self.header_text_boxes[column] = {'text': text_box, 'state': checkbox}
            # self.header_checkboxes[column] = checkbox
        self.adjust_stretch('main', 0)

    def handle_vendor_button_clicked(self, button):
        self.vendor = button.text()
        logger.debug(f"Vendor selected: {self.vendor}")
        self.clear_layout()

    def create_vendor_button_handler(self, vendor_button):
        def handler():
            self.handle_vendor_button_clicked(vendor_button)

        return handler

    def create_path_grid(self):
        path_grid = qtw.QGridLayout()

        path_button = create_button(
            "Select File", lambda: self.handle_file_dialog('path'), size=(75, 25), padding=0)
        self.path_text_box = qtw.QLineEdit()
        self.path_text_box.setPlaceholderText("Select a file to process")

        self.join_path_button = create_button(
            "Join Path", lambda: self.handle_file_dialog('join'), size=(75, 25), padding=0)
        self.join_path_text_box = qtw.QLineEdit("")
        self.join_path_text_box.setPlaceholderText("Select a file to join")

        self.add_to_layout(path_button, layout=path_grid, row=0, column=0, anchor='left')
        self.add_to_layout(self.path_text_box, layout=path_grid, row=0, column=1, anchor='left')
        self.add_to_layout(self.join_path_button, layout=path_grid, row=1, column=0, anchor='left')
        self.add_to_layout(self.join_path_text_box, layout=path_grid, row=1, column=1, anchor='left')

        return path_grid

    def create_radio_button_layout(self):
        radio_layout = qtw.QHBoxLayout()
        mixed_radio = create_radio_button("MIXED", size=(75, 25))
        landline_radio = create_radio_button("LANDLINE", size=(75, 25))
        cell_radio = create_radio_button("CELL", size=(75, 25))

        self.radio_widgets = [mixed_radio, landline_radio, cell_radio]
        for widget in self.radio_widgets:
            widget.clicked.connect(
                lambda _, w=widget: self.handle_radio_click(w, (self.join_path_button, self.join_path_text_box))
            )

        mixed_radio.setChecked(True)

        self.add_to_layout(mixed_radio, layout=radio_layout, anchor='left')
        self.add_to_layout(landline_radio, layout=radio_layout, anchor='left')
        self.add_to_layout(cell_radio, layout=radio_layout, anchor='left')

        return radio_layout

    def create_button_layout(self):
        button_layout = qtw.QGridLayout()
        self.check_button = create_button(
            "Check Headers", lambda: self.handle_check_headers(), size=(100, 50), checkable=True)
        self.process_button = create_button(
            "Process Data", lambda: self.handle_process_data(), size=(100, 50), checkable=True)

        button_group = qtw.QButtonGroup()
        button_group.setExclusive(True)
        button_group.addButton(self.check_button)
        button_group.addButton(self.process_button)
        button_group.buttonClicked.connect(lambda button: handle_button_clicked(button_group, button))

        self.add_to_layout(self.check_button, layout=button_layout, row=0, column=0, anchor='left')
        self.add_to_layout(self.process_button, layout=button_layout, row=1, column=0, anchor='left')

        return button_layout

    def main_panel(self):

        # Vendor selection buttons do not work properly when put in their own function.
        # The issue seems to be intermittent with no clear cause.
        self.vendor_layout = qtw.QVBoxLayout()
        self.vendor_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vendor_layout.setContentsMargins(0, 0, 5, 0)
        vendors = ['TAR', 'BAS', 'I360', 'DT', 'L2', 'RNC']

        button_group = qtw.QButtonGroup()
        button_group.setExclusive(True)
        for vendor in vendors:
            vendor_button = create_button(vendor, size=(50, 50), border_radius=25, checkable=True)
            vendor_button.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
            # vendor_button.clicked.connect(lambda checked, btn=vendor_button: self.handle_vendor_button_clicked(btn))
            vendor_button.clicked.connect(self.create_vendor_button_handler(vendor_button))
            self.add_to_layout(vendor_button, layout=self.vendor_layout, anchor='top')
            button_group.addButton(vendor_button)

        button_group.buttons()[0].setChecked(True)
        button_group.buttonClicked.connect(lambda button: handle_button_clicked(button_group, button))

        self.vendor_layout.addWidget(blank_widget())

        self.main_layout = qtw.QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addLayout(self.create_path_grid())

        self.layout().addLayout(self.vendor_layout, stretch=0)
        self.add_to_layout(create_candidate_names_text_box(), layout=self.main_layout, anchor='left')
        self.main_layout.addLayout(self.create_radio_button_layout())
        self.main_layout.addLayout(self.create_button_layout())

        widgets = get_widgets_from_layout(self.main_layout)
        for widget in widgets:
            widget.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)

        self.main_layout.addWidget(blank_widget())

        self.layout().addLayout(self.main_layout, stretch=1)

        self.index_of_vendor_layout = self.layout().indexOf(self.vendor_layout)
        self.index_of_main_layout = self.layout().indexOf(self.main_layout)
        logger.debug(f"Vendor layout index: {self.index_of_vendor_layout}")
        logger.debug(f"Main layout index: {self.index_of_main_layout}")

    def set_background_color(self, color: str):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

    def add_to_layout(
            self,
            item, anchor: str = "center",
            layout: Optional[qtw.QLayout] = None,
            row: Optional[int] = None,
            column: Optional[int] = None
    ):
        alignment = {
            "left": Qt.AlignmentFlag.AlignLeft,
            "right": Qt.AlignmentFlag.AlignRight,
            "top": Qt.AlignmentFlag.AlignTop,
            "bottom": Qt.AlignmentFlag.AlignBottom,
            "center": Qt.AlignmentFlag.AlignCenter,
        }.get(anchor, Qt.AlignmentFlag.AlignCenter)

        if layout is not None:
            if isinstance(layout, qtw.QGridLayout) and row is None:
                raise ValueError("Row must be specified for QGridLayout")
            elif isinstance(layout, qtw.QGridLayout) and column is None:
                raise ValueError("Column must be specified for QGridLayout")
            if row is not None and column is not None:
                layout.addWidget(item, row, column, alignment=alignment)
            else:
                layout.addWidget(item, alignment=alignment)
        else:
            self.layout().addWidget(item, alignment=alignment)

    def handle_file_dialog(self, path_type: str):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All files", "*.*"),
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("TXT files", "*.txt")
            ]
        )
        if path_type == 'path':
            self.path_text_box.setText(file_path)
        elif path_type == 'join':
            self.join_path_text_box.setText(file_path)


app = qtw.QApplication([])
mw = MainWindow()
app.exec()

sys.exit()

