from .api import NotesOperations, PinNotes, TrashNote, Collaborators, GetAllNotes

notes_routes = [
    (NotesOperations, '/notes'),
    (PinNotes, '/pin_notes'),
    (TrashNote, '/trash_notes'),
    (Collaborators, '/collaborators'),
    (GetAllNotes, '/display_notes')
]
