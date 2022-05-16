from flask import request, json
from flask_restful import Resource
from utility.util import token_required
from .model import Label


class LabelOperations(Resource):
    @token_required
    def post(self, **kwargs):
        user = kwargs.get('user')
        record = json.loads(request.data)
        label = Label(log_id=user.userId,
                      label=record['label'])
        label.save()
        return {"message": "Label Created"}, 201

    @token_required
    def get(self, **kwargs):
        user = kwargs.get('user')
        labels = Label.objects.filter(log_id=user.user_Id)
        if not labels:
            return{"message": "Labels couldn't be found"}, 400
        user_label = []
        for label in labels:
            user_label.append(label.to_json())
            return{"message": user_label}
        else:
            return {"message": "Some error Occurred"}, 405

    @token_required
    def patch(self):
        record = json.loads(request.data)
        labels = Label.objects.get(label_id=record['label_id'])
        if not labels:
            return {"message": "Label not Found"}, 401
        else:
            labels.update(label=record["label"])
            return {"message": "Label is Updated"}, 201

    @token_required
    def delete(self):
        record = json.loads(request.data)
        labels = Label.objects.get(label_id=record['label_id'])
        if not labels:
            return {"message": "Label not found"}, 401
        else:
            labels.delete()
            return {"message": "Label is Deleted"}, 201







