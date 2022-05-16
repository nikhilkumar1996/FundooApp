import mongoengine as d
import datetime
from label.model import Label
from user.model import User


class Notes(d.Document):
    note_id = d.SequenceField(primary_key=True)
    log_id = d.IntField()
    title = d.StringField(max_length=100)
    topic = d.StringField(max_length=100, required=True)
    desc = d.StringField(max_length=1000, required=True)
    is_trash = d.BooleanField(default=False)
    label_id = d.ListField(d.ReferenceField(Label, reverse_delete_rule=d.PULL), default=None)
    collaborator = d.ListField(d.ReferenceField(User, reverse_delete_rule=d.PULL), default=None)
    is_pinned = d.BooleanField(default=False)
    date_created = d.DateTimeField(default=datetime.datetime.now())

    def to_json(self):

        return {"LogId": self.log_id,
                "Title": self.title,
                "Topic": self.topic,
                "Description": self.desc,
                "Is_Trash": self.is_trash,
                "Is_Pinned": self.is_pinned,
                "Label_Id": self.label_id,
                "Collaborator": self.collaborator,
                "DateCreated": str(self.date_created)}

