import mongoengine as m


class User(m.Document):
    userId = m.SequenceField(primary_key=True)
    name = m.StringField(max_length=20, required=True)
    email = m.StringField(max_length=50, required=True)
    phone_no = m.IntField(max_value=9999999999, required=True)
    password = m.StringField(max_length=9999999, required=True)
    is_active = m.BooleanField(default=False)

    def to_json(self):
        return {"Name": self.name,
                "Email": self.email,
                "PhoneNo": self.phone_no,
                "Password": self.password,
                "Active": self.is_active}
