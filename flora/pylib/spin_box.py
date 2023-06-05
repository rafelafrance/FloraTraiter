from typing import Callable
from typing import Union

import customtkinter as ctk


class Spinner(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        command: Callable = None,
        start: int = 0,
        low: int = 0,
        high: int = 0,
        **kwargs,
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.command = command
        self.low = low
        self.high = high

        self.grid_columnconfigure((0, 2), weight=0)  # noqa
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = ctk.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.prev_page,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(
            self,
            width=width - (2 * height),
            height=height - 6,
            border_width=0,
            justify="center",
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        if self.command:
            self.entry.bind("<Return>", self.update_entry)

        self.add_button = ctk.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.next_page,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, str(int(start)))

        self.entry.bind("<Tab>", self.next_page)

        self.entry.bind("<Right>", self.next_page)
        self.entry.bind("<Left>", self.prev_page)

        self.entry.bind("<Next>", self.next_page)
        self.entry.bind("<Prior>", self.prev_page)

    def next_page(self, _=None):
        try:
            value = int(self.entry.get()) + 1
            self.set(value)
        except ValueError:
            value = self.high
        self.set(value)
        if self.command is not None:
            self.command()

    def prev_page(self, _=None):
        try:
            value = int(self.entry.get()) - 1
        except ValueError:
            value = self.low
        self.set(value)
        if self.command is not None:
            self.command()

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def update_entry(self, _=None):
        try:
            value = int(self.entry.get())
            self.set(value)
        except ValueError:
            return
        if self.command is not None:
            self.command()

    def set(self, value: int):
        value = min(max(int(value), self.low), self.high)
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
