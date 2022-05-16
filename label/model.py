from mongoengine import Document, StringField, IntField, SequenceField


class Label(Document):
    label_id = SequenceField(primary_key=True)
    label = StringField()
    log_id = IntField()

    def to_json(self):
        return{"label_id": self.label_id,
               "label": self.label,
               "log_id": self.log_id
        }