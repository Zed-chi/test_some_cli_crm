from menu import MenuItem
from . import funcs

"""
Logic:
1.Project_menu
    - Create
    - Work with
        - Add_contract
        - Finish project contract
    - List All
"""

projects = MenuItem("Projects")
projects.add_child(MenuItem("List All", parent=projects, func=funcs.list_projects))
projects.add_child(MenuItem("Finish Contract", func=funcs.finish_project_contract))
projects.add_child(MenuItem("Add Contract", func=funcs.add_contract))
projects.add_child(MenuItem("Create Project", func=funcs.create_project))
