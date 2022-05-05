import json
from flask_restful import Resource
from .model import Notes
from flask import json, request, jsonify
from utility.util import token_required
from label.model import Label


class NotesOperations(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
        This API Creates Notes for User Registered
        :param kwargs: User Fields of User Registered and present in token data
        :param request: login Id, Title, Topic, Description
        :return:Creates Notes
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes(log_id=user.userId,
                       title=record['Title'],
                       topic=record['Topic'],
                       desc=record['Description'])
        label_id = record['label_id']
        for lab in label_id:
            obj = Label.objects(label_id=lab)
            for l1 in obj:
                notes.label_id.append(l1)

        notes.save()
        return {"message": "Note is Created"}, 201

    @token_required
    def get(self, **kwargs):
        """
         This API retrieves the Notes for the User Registered and present in token data
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Show Notes of the User
        """
        user = kwargs.get('user')
        note_id = request.args.get("note_id")
        notes = Notes.objects.filter(note_id=note_id).first()
        if notes:
            if notes.log_id == user.userId:
                return {"note accessed": notes.to_json()}, 200

            else:
                return {"message": "User Id is not Verified"}, 404
        else:
            return {"message": "Cannot find Any Note"}, 401

    @token_required
    def patch(self, **kwargs):
        """
        This API updates the Notes content ('Topic') for the user registered
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Updates the Notes of the user
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.filter(note_id=record['note_id']).first()
        if not notes:
            return {"message": "Note Id Not Found"}, 401
        if notes:
            if notes.log_id == user.userId:
                notes.update(topic=record['topic'])

                return {'message': 'Updated Content in Notes'}, 201
            else:
                return {"message": "User Id is not Verified"}, 401
        else:
            return {"message": "Cannot process the request"}

    @token_required
    def delete(self, **kwargs):
        """
        This API deletes the Notes of the User
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Deletes Notes
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.filter(note_id=record['note_id']).first()
        if not notes:
            return {"message": "Note Id Not Found"}, 401
        if notes:
            if notes.log_id == user.userId and notes.is_trash:
                notes.delete()
                return {'message': "Note Deleted"}, 201
            else:
                return {"message": "User Id is not Verified"}, 401
        else:
            return {"message": "Cannot process the request"}, 405


class PinNotes(Resource):
    @token_required
    def patch(self, **kwargs):
        data = Notes.objects()
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.get(note_id=record['note_id'])
        if notes:
            if notes.log_id == user.userId:
                notes.is_pinned = True
                notes.save()
                all_notes = []
                for note in data:
                    if note.is_pinned:
                        all_notes.append(note.to_json())
                return {"message": "Note Pinned Successfully", "NotesPinned": all_notes}, 201
            else:
                return {"message": "User Id is not verified"}, 401
        else:
            return {"message": "Note Id not found"}, 401


class TrashNote(Resource):
    @token_required
    def patch(self, **kwargs):
        data = Notes.objects()
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.get(note_id=record['note_id'])
        if notes:
            if notes.log_id == user.userId:
                notes.is_trash = True
                notes.save()
                all_notes = []
                for note in data:
                    if note.is_trash:
                        all_notes.append(note.to_json())
                return {"message": "Note Trashed Successfully", "TrashNotes": all_notes}, 201
            else:
                return {"message": "User Id is not verified"}, 401
        else:
            return {"message": "Note Id not found"}, 401


class GetLabels(Resource):
    #     def get(self):
    #         notes = Notes.objects()
    #         _label = []
    #         for note in notes:
    #             label1 = []
    #             label_data = Label.objects()
    #             for lab in label_data:
    #                 label1.append(lab.to_json())
    #             all_label = []
    #             for i in note:
    #                 all_label.append(label1)
    #                 note.to_json()['Label_Id'] = all_label
    #             _label.append(note.to_json())
    #             print(_label)
    #
    #         return {"message": "Notes with Labels", "data": _label}, 200

    def get(self):
        notes = Notes.objects.all()
        all_notes = []
        for data in notes:
            note_data = data.to_json()
            label_id = note_data.get('Label_Id')

            label_fields = []
            for fields in label_id:
                label_fields.append(fields.to_json())
            note_data['Label_Id'] = label_fields
            all_notes.append(note_data)

        return {'message': 'success', 'data': all_notes}, 200


















