#   App windows
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QInputDialog, QListWidgetItem, QMessageBox

from Packages.DesignUI import MainWindows, Label, ListWidget, TextEdit, PushButton
from Packages.api.note import Note, load_notes


class Windows(MainWindows):
    def __init__(self):
        super().__init__("Cute Note")

        # Widget
        all_note_label = Label("ALL NOTES")
        self.list_widget = ListWidget()
        self.create_button = PushButton("Create")
        self.create_button.setDisabled(False)

        self.delete_button = PushButton("Delete")
        self.open_button = PushButton("Open")

        self.title_label = Label("Select Note to Open")
        self.text_edit = TextEdit()
        self.save_button = PushButton("Save")

        # Layouts
        main_layout = QHBoxLayout(self)
        left_v_layout = QVBoxLayout()
        right_v_layout = QVBoxLayout()
        left_bottom_h_layout = QHBoxLayout()

        main_layout.addLayout(left_v_layout)
        main_layout.addLayout(right_v_layout)
        main_layout.setStretch(0, 1)  # (a, b) a: index of first widget, b: value of proportion of space
        main_layout.setStretch(1, 2)  # 2+1 = 100 % of space

        left_v_layout.addWidget(all_note_label)
        left_v_layout.addWidget(self.list_widget)
        left_v_layout.addWidget(self.create_button)
        left_v_layout.addLayout(left_bottom_h_layout)

        left_bottom_h_layout.addWidget(self.delete_button)
        left_bottom_h_layout.addWidget(self.open_button)

        right_v_layout.addWidget(self.title_label)
        right_v_layout.addWidget(self.text_edit)
        right_v_layout.addWidget(self.save_button)

        # Widget Connections
        self.create_button.clicked.connect(self.create_note)
        self.delete_button.clicked.connect(self.delete_note)
        self.open_button.clicked.connect(self.open_note)
        self.save_button.clicked.connect(self.save_note)
        self.list_widget.itemDoubleClicked.connect(self.open_note)
        self.list_widget.itemSelectionChanged.connect(self.note_selected)

        # Keyboard Connection
        QShortcut(QKeySequence("Backspace"), self.delete_button, self.delete_note)  # <--
        QShortcut(QKeySequence("Delete"), self.delete_button, self.delete_note)  # DEL
        QShortcut(QKeySequence(QKeySequence.New), self.create_button, self.create_note)  # Ctrl + N
        QShortcut(QKeySequence(QKeySequence.Save), self.save_button, self.save_note)   # Ctrl + S

        # Run methods
        self.load_all_notes()

    # Methods
    def get_selected_item(self):
        selected_items = self.list_widget.selectedItems()     # Return a list of item
        if selected_items:
            return selected_items[0]    # We will use only one of selected item (the first)

    def add_item_list_view(self, item):
        note_item = QListWidgetItem(item.get_title())
        note_item.note = item  # add attribute object to identify note
        self.list_widget.addItem(note_item)
        self.list_widget.setCurrentItem(note_item)

    def load_all_notes(self):
        notes = load_notes()
        for note in notes:
            self.add_item_list_view(note)

    def clear_note(self):
        self.text_edit.clear()
        self.title_label.clear()

    # Slot
    def note_selected(self):
        self.delete_button.setDisabled(False)
        self.open_button.setDisabled(False)

    def create_note(self):
        title, is_result = QInputDialog().getText(self, "Add a note", "Title: ")
        if is_result and title:
            new_note = Note(title)
            new_note.save()
            self.add_item_list_view(new_note)
            self.open_note()

    def delete_note(self):

        selected_item = self.get_selected_item()
        result = selected_item.note.delete()    # Delete to disk
        if result:
            item_row = self.list_widget.row(selected_item)  # Take row of item
            self.list_widget.takeItem(item_row)     # Delete row to listWidget
            self.clear_note()

    def open_note(self):
        self.save_button.setDisabled(False)
        selected_item = self.get_selected_item()
        if not selected_item:
            return
        self.clear_note()
        self.title_label.setText(f"Title:   {selected_item.note.get_title()}\n"
                                 f"Created on:  {selected_item.note.get_date_creation()}\n"
                                 f"Last modification:   {selected_item.note.get_date_last_modification()}")
        if selected_item.note.get_content():
            self.text_edit.setText(selected_item.note.get_content())
        else:
            self.text_edit.setPlaceholderText("Empty content")

    def save_note(self):
        selected_item = self.get_selected_item()
        if not selected_item:
            return
        text_in_text_edit = self.text_edit.toPlainText()
        if text_in_text_edit != selected_item.note.get_content():
            selected_item.note.update(text_in_text_edit)
            popup = QMessageBox(self)
            popup.setText(f"{selected_item.note.get_title()} saved")
            popup.exec()
