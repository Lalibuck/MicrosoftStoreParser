from models import Application


def test_app_fulldata():
    app = Application(name='Taskade', company='Taskcade Inc.', release='2020', email='support@taskade.com')
    assert app.name == 'Taskade'
    assert app.company == 'Taskcade Inc.'
    assert app.release == '2020'
    assert app.email == 'support@taskade.com'


def test_app_partdata():
    app = Application(name='Taskade', company='Taskcade Inc.', release='', email='')
    assert app.name == 'Taskade'
    assert app.company == 'Taskcade Inc.'
    assert app.release == ''
    assert app.email == ''
