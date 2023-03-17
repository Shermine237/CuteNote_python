#   Note class
import json
import os
from uuid import uuid4
from datetime import datetime
from glob import glob

from Packages.api.constants import FILES_USER_DIR


def load_notes():
    notes = glob(os.path.join(FILES_USER_DIR, "*.json"))  # Select all *.json files
    notes_list = []
    for note_json in notes:
        # Take content
        with open(note_json, "r") as file:
            note_data = json.load(file)
        # Take uuid from name
        name_note = os.path.basename(note_json)  # give name like uuid.json
        uuid = os.path.splitext(name_note)[0]   # give name without extension
        # Recreate Note object from json data
        title = note_data.get("title")
        content = note_data.get("content")
        date_creation = note_data.get("date_creation")
        date_modify = note_data.get("date_modification")
        note_obj = Note(title, content, True, uuid, date_creation, date_modify)
        # Add note to list
        notes_list.append(note_obj)
    return notes_list


class Note:
    def __init__(self, title, content="", recreate=False, uuid=None, date_create=None, date_modify=None):
        #   Attributes
        self.note_title = title
        self.note_content = content
        if recreate:
            self.note_uuid = uuid
            self.date_creation = date_create
            self.date_last_modification = date_modify
        else:
            self.note_uuid = str(uuid4())
            self.date_creation = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.date_last_modification = None

    def __repr__(self):  # to give a string representation of object (as a name)
        return f"{self.note_title} ({self.note_uuid})"

    #   Methods Getter
    def get_uid(self):
        return self.note_uuid

    def get_title(self):
        return self.note_title

    def get_content(self):
        return self.note_content

    def get_date_creation(self):
        return self.date_creation

    def get_date_last_modification(self):
        return self.date_last_modification

    #   Methods Setter
    def update(self, content=None, title=None):
        if title:
            self.note_title = title
        if content:
            self.note_content = content
        self.update_date()

    #   Methods utilities
    def save(self):
        if not os.path.exists(FILES_USER_DIR):  # If the folder don't exist
            os.makedirs(FILES_USER_DIR)
        data = {"title": self.note_title,
                "content": self.note_content,
                "date_creation": self.date_creation,
                "date_modification": self.date_last_modification}
        #   write data in a file
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)  # incident is tabulation

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)
            return True
        return False

    def update_date(self):
        self.date_last_modification = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #   Methods as attribute (to use without () )
    @property
    def path(self):
        return os.path.join(FILES_USER_DIR, self.note_uuid + ".json")
