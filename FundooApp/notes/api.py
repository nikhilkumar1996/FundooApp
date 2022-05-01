import json
from flask_restful import Resource
from .model import Notes
from flask import json, request
from utility.util import token_required


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
        note_id = request.args.get("Note_Id")
        notes = Notes.objects.filter(note_id=note_id).first()
        if notes:
            if notes.log_id == user.userId:
                return {"note accessed": notes.to_json()}, 200

            else:
                return {"message": "User Id not Found"}, 404
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
        notes = Notes.objects.filter(note_id=record['Note_Id']).first()
        if not notes:
            return {"message": "Note Id Not Found"}, 401
        if notes:
            if notes.log_id == user.userId:
                notes.update(topic=record['Topic'])
                return {'message': 'Updated Content in Notes'}, 201
            else:
                return {"message": "User Id not Found"}, 401
        else:
            return {"message": "Cannot process the request"}

    @token_required
    def delete(self, **kwargs):
        """
        This API deletes the Notes by turning is_trash = True
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Deletes Notes
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.filter(note_id=record['Note_Id']).first()
        if not notes:
            return {"message": "Note Id Not Found"}, 401
        if notes:
            if notes.log_id == user.userId:
                notes.is_trash = True
                notes.save()
                return {'message': "Note Deleted"}, 201
            else:
                return {"message": "User Id not Found"}, 401
        else:
            return {"message": "Cannot process the request"}, 405












