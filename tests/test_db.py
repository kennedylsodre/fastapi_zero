from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    new_user = User(
        username='Kennedy', email='klacerda@teste.com', password='teste'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Kennedy'))

    assert user.username == 'Kennedy'
