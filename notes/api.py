import json
from flask_restful import Resource

from user.model import User
from .model import Notes
from flask import json, request
from utility.util import token_required, get_cache_value
from utility import logger
from utility.custom_exceptions import InternalServerException, NotFoundException
from label.model import Label
import redis

r = redis.Redis(
    host="localhost",
    port=6379
)


class NotesOperations(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
        This API Creates Notes with Labels for Registered User
        :param kwargs: User fields of User Registered and present in token data
        :param request: login id, Title, Topic, Description, label id
        :return:Creates Notes
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        logger.logging.info("Adding Notes")
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
        logger.logging.info('Note Created')
        return {"message": "Note is Created"}, 201

    @token_required
    def get(self, **kwargs):
        """
         This API retrieves the particular Note for the Registered User and present in token data
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Shows Notes of the User
        """
        user = kwargs.get('user')
        key = f"getuser{user.userId}"
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data
        note_id = request.args.get("note_id")
        notes = Notes.objects.filter(note_id=note_id).first()
        if notes:
            logger.logging.info("Checking if user exist")
            if notes.log_id == user.userId:
                display = []
                note_data = notes.to_json()
                collab_fields, label_fields = [], []

                if notes.collaborator:
                    logger.logging.debug("Checking If Collaborator Is Present")
                    collaborators = note_data.get('Collaborator')
                    for collab in collaborators:
                        collab_fields.append(collab.to_json())
                    note_data['Collaborator'] = collab_fields
                    display.append(note_data)

                if notes.label_id:
                    logger.logging.debug('Checking If Label Is Present ')
                    label_id = note_data.get('Label_Id')
                    for label in label_id:
                        label_fields.append(label.to_json())
                    note_data['Label_Id'] = label_fields

                    display.append(note_data)

                    logger.logging.debug("Note is Displayed")
                    get_cache_value(key, display, 100)
                    return {"key": key, "user_note": display}
                else:
                    logger.logging.debug("Note Without Labels And Collaborators Is Displayed")
                    return {"message": notes.to_json()}, 200

            else:
                logger.logging.error("User Id Not Verified")
                return {"message": "User Id is not Verified"}, 404
        else:
            logger.logging.error("Can't Find Notes")
            return {"message": "Cannot find Any Note"}, 401

    @token_required
    def patch(self, **kwargs):
        """
        This API updates the Notes content ('Topic') for the  Registered User
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Updates the Notes of the user
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.filter(note_id=record['note_id']).first()
        try:
            if not notes:
                logger.logging.error("Can't find Note Id")
                return {"message": "Note Id Not Found"}, 401
            if notes:
                if notes.log_id == user.userId:
                    notes.update(topic=record['topic'])

                    logger.logging.info("Updated Note")
                    return {'message': 'Updated Content in Note'}, 201
                else:
                    logger.logging.error("User Id not verified")
                    return {"message": "User Id is not Verified"}, 401
            raise NotFoundException('Note not found', 400)

        except NotFoundException as exception:
            logger.logging.error("Some Error Occurred")
            return {"message": exception.__dict__}

    @token_required
    def delete(self, **kwargs):
        """
        This API deletes the Notes of the User with User Validation
        :param kwargs: User fields in token required decorator
        :param request: note_id
        :return: Deletes Notes
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects.filter(note_id=record['note_id']).first()
        try:
            if not notes:
                logger.logging.error("Note not found")
                return {"message": "Note Id Not Found"}, 401
            if notes:
                if notes.log_id == user.userId and notes.is_trash:
                    notes.delete()
                    logger.logging.info("Note Is Deleted")
                    return {'message': "Note Deleted"}, 201
                else:
                    logger.logging.error("Missing User Id or Note is not Trashed ")
                    return {"message": "User Id is not Verified or Note is not trashed first "}, 401

            raise NotFoundException('Note not found', 400)
        except NotFoundException as exception:
            logger.logging.error("Some Error Occurred")
            return {"message": exception.__dict__}, 405


class PinNotes(Resource):
    @token_required
    def patch(self, **kwargs):
        """
        This API Pins the Note and display all Pinned Notes with User Validation
        :param kwargs: User fields in token required decorator
        :return: Displays all Pinned Notes
        """
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

                logger.logging.debug("Note is Pinned")
                return {"message": "Note Pinned Successfully", "NotesPinned": all_notes}, 201
            else:
                logger.logging.error("User Id Not Verified")
                return {"message": "User Id is not verified"}, 401
        else:
            logger.logging.error("Note Id Not Found")
            return {"message": "Note Id not found"}, 401


class TrashNote(Resource):
    @token_required
    def patch(self, **kwargs):
        """
         This API Trash a Note and display all Trashed Notes with User Validation
        :param kwargs:  User fields in token required decorator
        :return: Displays all Trashed Notes
        """
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
                logger.logging.debug("Note is Trashed")
                return {"message": "Note Trashed Successfully", "TrashNotes": all_notes}, 201
            else:
                logger.logging.error("User Id Not Verified")
                return {"message": "User Id is not verified"}, 401
        else:
            logger.logging.error("Note Id Not Found")
            return {"message": "Note Id not found"}, 401


class Collaborators(Resource):
    @token_required
    def post(self, **kwargs):
        """
        This API adds Collaborator for a Note with User Validation
        :param kwargs: User fields in token required decorator
        :return: Adds Collaborator
        """
        user = kwargs.get('user')
        record = json.loads(request.data)
        notes = Notes.objects(note_id=record['note_id']).first()
        if notes:
            if notes.log_id == user.userId:
                collaborator = record['collaborator']
                for collab in collaborator:
                    obj = User.objects(userId=collab)
                    for c1 in obj:
                        notes.collaborator.append(c1)

        notes.save()
        logger.logging.debug("Collaborator Added ")
        return {"message": "Collaborator added in Notes"}, 201


class GetAllNotes(Resource):
    def get(self):
        """
        This API Display all Notes for all Users
        :return: Displays all Created Notes in DB
        """
        notes = Notes.objects()
        all_notes = []
        for note in notes:
            note_data = note.to_json()
            collab_fields, label_fields = [], []

            if note.collaborator:
                collaborators = note_data.get('Collaborator')
                for collab in collaborators:
                    collab_fields.append(collab.to_json())
                note_data['Collaborator'] = collab_fields
                all_notes.append(note_data)

            if note.label_id:
                label_id = note_data.get('Label_Id')
                for label in label_id:
                    label_fields.append(label.to_json())
                note_data['Label_Id'] = label_fields
                all_notes.append(note_data)

        logger.logging.debug("ALl Notes Displayed")
        return {'message': 'success', 'data': all_notes}, 200





















