from menu import MenuItem

from . import funcs

"""
Logic:
2.Contract_menu
    - Create
    - Sign
    - Finish 
    - List All
"""

contracts = MenuItem("Contracts")


contracts.add_child(MenuItem(title="List All", func=funcs.list_contracts))
# contracts.add_child(MenuItem(title="Finish", func=funcs.finish_contract))
contracts.add_child(MenuItem(title="Sign", func=funcs.sign_contract))
contracts.add_child(MenuItem(title="Create", func=funcs.create_contract))
