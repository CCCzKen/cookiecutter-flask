# -*- coding: utf-8 -*-

from flask_script import Manager, Server

from app import app

manager = Manager(app)

manager.add_command('runserver', Server(port={{ cookiecutter.port | int }}))


if __name__ == "__main__":
    manager.run()
