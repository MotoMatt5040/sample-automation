import traceback
import os

from dotenv import load_dotenv
load_dotenv()

import PyQt5.QtWidgets as qtw
import pandas as pd
from tkinter import filedialog
from clients import Tarrance, Baselice


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.df_initialized = False
        self.df = pd.DataFrame()
        self.setWindowTitle("Sample Automation")
        self.setLayout(qtw.QHBoxLayout())

        self._file_path = None
        self.init_ui()
        self.show()

    def init_ui(self):
        initial_layout = qtw.QVBoxLayout()
        self.client_label = qtw.QLabel("Select Client")
        initial_layout.addWidget(self.client_label)

        self.client_combo_box = qtw.QComboBox(self)
        self.client_combo_box.addItem("Tarrance")
        self.client_combo_box.addItem("I360")
        self.client_combo_box.addItem("Other")
        self.client_combo_box.addItem("Other 2")
        initial_layout.addWidget(self.client_combo_box)

        self.candidate_names_text_box = qtw.QTextEdit(
            self,
            lineWrapMode=qtw.QTextEdit.NoWrap,
            placeholderText="Enter candidate names separated by new lines",
            readOnly=False
        )

        initial_layout.addWidget(self.candidate_names_text_box)

        self.path_label = qtw.QLabel("Select a file to begin")
        initial_layout.addWidget(self.path_label)

        path_btn = qtw.QPushButton("Select File", clicked=lambda: self.get_file_path())
        initial_layout.addWidget(path_btn)

        check_headers_btn = qtw.QPushButton("Check Headers", clicked=self.check_headers)
        initial_layout.addWidget(check_headers_btn)

        rename_btn = qtw.QPushButton("Update Headers", clicked=self.update_headers)
        initial_layout.addWidget(rename_btn)

        self.process_data_btn = qtw.QPushButton("Process Data", clicked=self.process_data)
        initial_layout.addWidget(self.process_data_btn)

        self.layout().addLayout(initial_layout)

    def check_headers(self):

        try:
            self.get_data()
            self.replace_header_names()
            self.display_column_headers()
        except Exception as e:
            print(traceback.format_exc(), e)


    def update_headers(self):
        self.rename_columns()
        self.replace_header_names()
        self.display_column_headers()

    def replace_header_names(self):
        column_names_to_check = {
            'FNAME': ['FIRSTNAME'],
            'LNAME': ['LASTNAME'],
        }
        for replacement, check_list in column_names_to_check.items():
            for check in check_list:
                if check in self.df.columns:
                    self.df.rename(columns={check: replacement}, inplace=True)

        self.df['FNAME'] = self.df['FNAME'].astype(str)
        self.df['LNAME'] = self.df['LNAME'].astype(str)
        self.df['FULL_NAME'] = self.df['FNAME'] + ' ' + self.df['LNAME']

        candidate_names = self.candidate_names_text_box.toPlainText().split("\n")
        candidate_names = [name.strip().upper() for name in candidate_names if name.strip()]

        if candidate_names:
            self.df = self.df[~self.df['FULL_NAME'].isin(candidate_names)].reset_index(drop=True)

        if 'FULL_NAME' in self.df.columns:
            self.df.drop(columns=['FULL_NAME'], inplace=True)

    def get_file_path(self):
        self.file_path = filedialog.askopenfilename(initialdir=os.environ.get("PROJECT_DIRECTORY"))
        self.path_label.setText(self.file_path)
        return self.file_path

    def get_data(self):
        if not self.file_path:
            raise ("File path is required")

        self.df_initialized = False
        file_type = self.file_path.split(".")[-1]
        match file_type:
            case 'xlsx':
                print('xlsx')
                # d = pd.read_excel(self.file_path)
                # print('d shape', d.shape[0])
                self.df = pd.read_excel(self.file_path)
            case 'xls':
                print('xls')
                self.df = pd.read_excel(self.file_path)
            case 'csv':
                print('csv')
                self.df = pd.read_csv(self.file_path)
            case 'txt':
                print('txt')
                self.df = pd.read_csv(self.file_path, delimiter="\t")
            case _:
                raise f"File type not supported"

        self.df.columns = [col.upper() for col in self.df.columns]
        # print(self.df['REGION'].value_counts())
        # print(self.df['THREEAGE'].value_counts())
        # print(self.df['GENDER'].value_counts())
        # self.df.rename(columns={'FirstName': "FNAME", 'LastName': "LNAME"}, inplace=True)
        # print(self.df['zip'].value_counts())
        # print('get data', self.df.shape[0])

    def select_clients(self):
        client = None
        client_selection = self.client_combo_box.currentText()
        match client_selection:
            case 'Tarrance':
                print("Tarrance selected")
                checked_headers = self.get_checked_headers()
                client = Tarrance(self.df, checked_headers)
            case 'Baselice':
                print("Baselice selected")
                checked_headers = self.get_checked_headers()
                client = Baselice(self.df, checked_headers)
            case _:
                ''

        if client:

            project_number = os.path.basename(os.path.dirname(os.path.dirname(self.file_path)))
            save_path = f'{os.environ.get("PROJECT_DIRECTORY")}/{project_number}/SAMPLE/auto/'
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            print(project_number)
            lsam_count = 1
            csam_count = 1
            while True:
                if not os.path.exists(f'{save_path}{project_number}LSAM.csv'):
                    client.final_landline.to_csv(f'{save_path}{project_number}LSAM.csv', index=False)
                    break
                if not os.path.exists(f'{save_path}{project_number}LSAM{lsam_count}.csv'):
                    client.final_landline.to_csv(f'{save_path}{project_number}LSAM{lsam_count}.csv', index=False)
                    break
                lsam_count += 1

            while True:
                if not os.path.exists(f'{save_path}{project_number}CSAM.csv'):
                    client.final_cell.to_csv(f'{save_path}{project_number}CSAM.csv', index=False)
                    break
                if not os.path.exists(f'{save_path}{project_number}CSAM{csam_count}.csv'):
                    client.final_cell.to_csv(f'{save_path}{project_number}CSAM{csam_count}.csv', index=False)
                    break
                csam_count += 1
        print("Finished processing")

    def display_column_headers(self):
        # Create a new layout for column headers
        grid_layout = qtw.QGridLayout()

        # Clear any existing column header widgets
        if hasattr(self, 'header_widget_container'):
            self.layout().removeWidget(self.header_widget_container)
            self.header_widget_container.deleteLater()

        # Create a container widget for column headers
        self.header_widget_container = qtw.QWidget()
        self.header_widget_container.setLayout(grid_layout)
        self.layout().addWidget(self.header_widget_container)

        # Add labels, checkboxes, and text boxes for each column header in the DataFrame
        self.header_text_boxes = {}  # Dictionary to keep track of text boxes
        self.header_checkboxes = {}  # Dictionary to keep track of checkboxes

        for index, column in enumerate(self.df.columns):
            checkbox = qtw.QCheckBox()
            label = qtw.QLabel(column)
            text_box = qtw.QLineEdit()
            text_box.setText(column)  # Set the initial text to the column name

            grid_layout.addWidget(checkbox, index, 0)  # Add checkbox to the first column
            grid_layout.addWidget(label, index, 1)  # Add label to the second column
            grid_layout.addWidget(text_box, index, 2)  # Add text box to the third column

            # Store the text box and checkbox in dictionaries
            self.header_text_boxes[column] = text_box
            self.header_checkboxes[column] = checkbox

    def rename_columns(self):
        # Create a dictionary to map old column names to new names
        original_columns = list(self.df.columns)
        new_columns = {}

        for old_name, text_box in self.header_text_boxes.items():
            new_name = text_box.text().strip()
            if new_name and new_name != old_name:  # Only add if new name is different and non-empty
                new_columns[old_name] = new_name

        # Rename only the columns that have changed names
        if new_columns:
            self.df.rename(columns=new_columns, inplace=True)

    def get_checked_headers(self):
        checked_headers = [column for column, checkbox in self.header_checkboxes.items() if checkbox.isChecked()]
        return checked_headers

    def process_data(self):
        # print(self.df.shape[0])
        self.select_clients()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, df: pd.DataFrame = pd.DataFrame()):
        if not self.df_initialized:
            df['CALLIDL1'] = ''
            df['CALLIDL2'] = ''
            df['CALLIDC1'] = ''
            df['CALLIDC2'] = ''
            df['TFLAG'] = 0
            df['VEND'] = 5
            df['VTYPE'] = ''
            df['MD'] = ''
            df['BATCH'] = ''
            self.df_initialized = True

        self._df = df


app = qtw.QApplication([])
mw = MainWindow()
app.exec_()

