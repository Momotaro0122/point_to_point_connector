'''
point_to_point_ui.py
Description:All point to point connector ui widgets and function will place in here.
Show: None
Author: Martin Lee
Created: 09 May 2023
Last Updated: 09 May 2023 - Martin Lee
Usuage - --
'''
# Import statements and other UI-related code
import maya.cmds as mc
from maya import OpenMayaUI as omui
import ast
import point_to_point_constraint
reload(point_to_point_constraint)

from point_to_point_constraint import pp_constraint

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from shiboken import wrapInstance


class PointToPointConstraintUI(QDialog):
    def __init__(self, parent=None):
        for widget in QApplication.allWidgets():
            if widget.objectName() == "Point to Point Constraint":
                # print("ok")
                widget.deleteLater()
        super(PointToPointConstraintUI, self).__init__(parent)
        self.setWindowTitle("Point to Point Constraint")
        self.setObjectName("Point to Point Constraint")
        self.setMinimumSize(400, 100)
        self.setMaximumSize(600, 300)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.point1_line_edit = QLineEdit()
        self.point2_line_edit = QLineEdit()

        self.select_point1_button = QPushButton("Select")
        self.select_point2_button = QPushButton("Select")

        self.execute_button = QPushButton("Execute Constraint")

    def create_layouts(self):
        self.create_instructions()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.instructions_label)

        point1_layout = QHBoxLayout()
        point1_layout.addWidget(self.point1_line_edit)
        point1_layout.addWidget(self.select_point1_button)

        point2_layout = QHBoxLayout()
        point2_layout.addWidget(self.point2_line_edit)
        point2_layout.addWidget(self.select_point2_button)

        main_layout.addLayout(point1_layout)
        main_layout.addLayout(point2_layout)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)

    def create_connections(self):
        self.select_point1_button.clicked.connect(self.select_point1)
        self.select_point2_button.clicked.connect(self.select_point2)
        self.execute_button.clicked.connect(self.execute_constraint)

    def select_point1(self):
        selected = mc.ls(sl=True)
        if selected:
            self.point1_line_edit.setText(str(selected[0:]))

    def select_point2(self):
        selected = mc.ls(sl=True)
        if selected:
            self.point2_line_edit.setText(str(selected[0:]))

    def execute_constraint(self):
        point1 = ast.literal_eval(self.point1_line_edit.text())  # Turn string to list.
        point2 = ast.literal_eval(self.point2_line_edit.text())  # Turn string to list.

        if point1 and point2:
            if len(point1) == len(point2):
                for p1, p2 in zip(point1, point2):
                    pp_constraint(p1, p2)
            else:
                matching_dialog = MatchingDialog(point1, point2, parent=maya_main_window())
                matching_dialog.exec_()
        else:
            QMessageBox.warning(None, "Warning", "Please select two points before executing the constraint.")

    def create_instructions(self):
        instructions = (
            "1. Select vert(s) for Mesh 1 and press 'Select'.\n"
            "2. Select vert(s) for Mesh 2 and press 'Select'.\n"
            "3. Press 'Execute Constraint' to apply the constraint.\n"
            "4. If the number of verts in Mesh 1 and Mesh 2 does not match, the Point Matching dialog will appear."
        )
        self.instructions_label = QLabel(instructions)
        self.instructions_label.setWordWrap(True)


class MatchingDialog(QDialog):
    def __init__(self, point1, point2, parent=None):
        super(MatchingDialog, self).__init__(parent)

        self.setWindowTitle("Point Matching")
        self.setMinimumSize(400, 100)
        self.setMaximumSize(600, 300)

        self.create_widgets(point1, point2)
        self.create_layouts()
        self.create_connections()

    def create_widgets(self, point1, point2):
        self.point1_list = QListWidget()
        self.point2_list = QListWidget()
        # vertex select scene.
        self.point1_list.itemSelectionChanged.connect(self.select_point1_item)
        self.point2_list.itemSelectionChanged.connect(self.select_point2_item)

        self.point1_list.addItems(point1)
        self.point2_list.addItems(point2)

        self.add_button = QPushButton("Add Match")
        self.remove_button = QPushButton("Remove Match")
        self.match_list = QListWidget()

        self.execute_button = QPushButton("Execute Constraint")

    def select_point1_item(self):
        item = self.point1_list.currentItem()
        if item:
            point = item.text()
            mc.select(point, replace=True)

    def select_point2_item(self):
        item = self.point2_list.currentItem()
        if item:
            point = item.text()
            mc.select(point, replace=True)

    def create_layouts(self):
        self.create_instructions()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.instructions_label)

        points_layout = QHBoxLayout()
        points_layout.addWidget(self.point1_list)
        points_layout.addWidget(self.point2_list)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)

        match_layout = QHBoxLayout()
        match_layout.addLayout(buttons_layout)
        match_layout.addWidget(self.match_list)

        main_layout.addLayout(points_layout)
        main_layout.addLayout(match_layout)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)

    def create_connections(self):
        self.add_button.clicked.connect(self.add_match)
        self.remove_button.clicked.connect(self.remove_match)
        self.execute_button.clicked.connect(self.execute_constraint)

    def add_match(self):
        selected_point1 = self.point1_list.currentItem()
        selected_point2 = self.point2_list.currentItem()

        if selected_point1 and selected_point2:
            match_str = "{} - {}".format(selected_point1.text(), selected_point2.text())
            self.match_list.addItem(match_str)

    def remove_match(self):
        current_item = self.match_list.currentItem()
        if current_item:
            row = self.match_list.row(current_item)
            self.match_list.takeItem(row)

    def execute_constraint(self):
        for i in range(self.match_list.count()):
            item_text = self.match_list.item(i).text()
            p1, p2 = item_text.split(" - ")
            pp_constraint(p1, p2)

        self.accept()

    def create_instructions(self):
        instructions = (
            "1. Select a verts in both Mesh 1 and Point Mesh 2.\n"
            "2. Press 'Add Match' to add the selected points as a match.\n"
            "3. To remove a match, select it in the Match list and press 'Remove Match'.\n"
            "4. Press 'Execute Constraint' to apply the constraints to the matched points."
        )
        self.instructions_label = QLabel(instructions)
        self.instructions_label.setWordWrap(True)


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)


