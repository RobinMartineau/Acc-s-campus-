from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.badge import getBadges

#Mock du modèle Badge
class MockBadge:
    def __init__(self, uid, actif, creation, id_utilisateur):
        self.uid = uid
        self.actif = actif
        self.creation = creation
        self.id_utilisateur = id_utilisateur

#T7.1 – Aucun badge enregistré
def test_get_badges_aucun_badge():
    db = MagicMock()
    db.query().all.return_value = []

    try:
        getBadges(db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Aucun badge trouvé"

#T7.2 – Liste de badges
def test_get_badges_liste_complete():
    db = MagicMock()
    badges = [
        MockBadge(uid="A1B2C3F6", actif=True, creation="2025-03-31", id_utilisateur=12),
        MockBadge(uid="X7W6V5U4", actif=False, creation="2025-03-28", id_utilisateur=8),
    ]
    db.query().all.return_value = badges

    response = getBadges(db)

    assert len(response) == 2
    assert response[0].uid == "A1B2C3F6"
    assert response[0].actif is True
    assert response[0].creation == "2025-03-31"
    assert response[0].id_utilisateur == 12

    assert response[1].uid == "X7W6V5U4"
    assert response[1].actif is False
    assert response[1].creation == "2025-03-28"
    assert response[1].id_utilisateur == 8
