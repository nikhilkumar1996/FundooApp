import mongoengine as d
import datetime
from label.model import Label


class Notes(d.Document):
    note_id = d.SequenceField(primary_key=True)
    log_id = d.IntField()
    title = d.StringField(max_length=100)
    topic = d.StringField(max_length=100, required=True)
    desc = d.StringField(max_length=1000, required=True)
    is_trash = d.BooleanField(default=False)
    label_id = d.ListField(d.ReferenceField(Label, reverse_delete_rule=d.PULL))
    is_pinned = d.BooleanField(default=False)
    date_created = d.DateTimeField(default=datetime.datetime.now())

    def to_json(self):
        # std = dict()
        # std['note_id'] = self.note_id
        # std['log_id'] = self.log_id
        # std['label_id'] = self.label_id
        # return std

        return {"LogId": self.log_id,
                "Title": self.title,
                "Topic": self.topic,
                "Description": self.desc,
                "Is_Trash": self.is_trash,
                "Is_Pinned": self.is_pinned,
                "Label_Id": self.label_id,
                "DateCreated": str(self.date_created)}

