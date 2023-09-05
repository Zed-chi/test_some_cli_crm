"""
Menu semantic
show options
choose option
exit
"""
import os
import sys

from color_print import ColorPrint as cprint


def get_choice():
    while True:
        try:
            choice = int(input("Choose Option >> "))
            return choice
        except Exception:
            cprint.print_fail("wrong menu num")


class MenuItem:
    def __init__(self, title, func=None, parent=None, finite=False, root=False):
        self.title = title
        self.children = []
        self.func = func
        self.parent = parent
        if root:
            self.children.append(MenuItem("Exit", sys.exit, self, True))
        elif not finite:
            self.children.append(MenuItem("Back", lambda: "back", self, True))

    def add_child(self, menu_item):
        menu_item.parent = self
        self.children.insert(0, menu_item)

    def show(self):
        print()
        cprint.print_warn(f"[{self.title}]")
        if self.children:
            for num, item in enumerate(self.children):
                cprint.print_info(f"{num}. {item.title}")
        print()

    def loop(self):
        if not self.children and not self.func:
            return
        while True:
            self.show()
            if self.func:
                try:
                    result = self.func()
                except Exception as e:
                    cprint.print_fail(str(e))
                return "back"

            num = get_choice()
            os.system("cls" if os.name == "nt" else "clear")
            if num + 1 > len(self.children) or num + 1 < 0:
                print(
                    f"{num+1} > {len(self.children)} or {num+1} < {len(self.children)}"
                )
                continue
            item = self.children[num]
            result = item.loop()
            if result == "back":
                return
