import mongoengine as d
import datetime


class Notes(d.Document):
    note_id = d.SequenceField(primary_key=True)
    log_id = d.IntField()
    title = d.StringField(max_length=100)
    topic = d.StringField(max_length=100, required=True)
    desc = d.StringField(max_length=1000, required=True)
    is_trash = d.BooleanField(default=False)
    date_created = d.DateTimeField(default=datetime.datetime.now())

    def to_json(self):
        return {"LogId": self.log_id,
                "Title": self.title,
                "Topic": self.topic,
                "Description": self.desc,
                "Is_Trash": self.is_trash,
                "DateCreated": str(self.date_created)}

