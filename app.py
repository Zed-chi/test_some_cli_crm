from colorama import just_fix_windows_console

from config import db
from contracts.options import contracts
from menu import MenuItem
from models import Contract, Project
from projects.options import projects

just_fix_windows_console()


def init():
    db.connect()
    db.create_tables([Contract, Project])


"""
Logic:
1.Project_menu
    - Create
    - Work with
        - Add_contract
        - Finish project contract
    - List All
2.Contract_menu
    - Create
    - Sign
    - Finish
    - List All
3. List Info
4.Exit
"""


def main():
    item = MenuItem("Main Menu", root=True)
    item.add_child(projects)
    item.add_child(contracts)
    try:
        item.loop()
    except KeyboardInterrupt:
        print("Bye")


if __name__ == "__main__":
    init()
    main()
