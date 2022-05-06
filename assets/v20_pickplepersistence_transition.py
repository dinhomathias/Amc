#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script prepares the file(s) saved by PicklePersistence for v20. How to do it:
1. Run this script *after* upgrading to v20.
2. Enter the path of your persistence file below.

Note: This script will not handle directly pickled `telegram.Bot` instances and `telegram.ext.*`
instances. Make sure to remove these before running this script.

WARNING: Save a backup of your pickle file(s) before running this!
"""

# Must be the same value as passed to the `filename` parameter of PicklePersistence
persistence_file_path = "ENTER FILE PATH"

# Don't touch anything below this line!
# -------------------------------------------------------------------------------------------------
import telegram

if telegram.__version__.startswith('1'):
    raise RuntimeError("This transition script must be run with v20!")
import pickle
from pathlib import Path

from telegram import TelegramObject
from telegram.ext._picklepersistence import _BotPickler

fields_to_change = {
    'bot': '_bot',
    'voice_chat_ended': 'video_chat_ended',
    'voice_chat_scheduled': 'video_chat_scheduled',
    'voice_chat_started': 'video_chat_started',
    'voice_chat_participants_invited': 'video_chat_participants_invited',
}


def modified_setstate(self, state) -> None:
    # This contains values from __slots__
    data = state[1] if isinstance(state, tuple) else state
    # Now handle fields which have been renamed:
    for old_field, new_field in fields_to_change.items():
        if old_field in data:
            data[new_field] = data.pop(old_field)

    # And finally set the state:
    for key, val in data.items():
        setattr(self, key, val)


class CustomBotPickler(_BotPickler):
    def __init__(self, *args, **kwargs):
        super().__init__('bot', *args, **kwargs)  # we don't need the bot here so just pass a dummy

    def persistent_id(self, obj):
        # Replace the v13 string with the v20 version as a persistent_id, so it works correctly.
        if isinstance(obj, str) and obj == 'bot_instance_replaced_by_ptb_persistence':
            return "a known bot replaced by PTB's PicklePersistence"
        # Reassign the correct setstate method:
        if isinstance(obj, TelegramObject):
            obj.__class__.__setstate__ = TelegramObject.__setstate__


class BotUnpickler(pickle.Unpickler):
    def find_class(self, module_name: str, name: str):
        if not module_name.startswith('telegram.'):
            return super().find_class(module_name, name)
        if name == "DefaultValue":
            obj = getattr(telegram._utils.defaultvalue, name)
        else:
            obj = getattr(telegram, name)  # Hoping that the data is a part of public API!
        obj.__setstate__ = modified_setstate
        return obj


def convert(path: Path):
    print(f'Loading data from {path.name}...\n')
    pp_data = BotUnpickler(file=path.open('rb')).load()
    print('Converting data...\n')
    CustomBotPickler(path.open('wb')).dump(pp_data)  # repickle the data:


if __name__ == "__main__":
    fp = persistence_file_path
    possible_files = [
        f"{fp}_user_data",
        f"{fp}_bot_data",
        f"{fp}_chat_data",
        f"{fp}_conversations",
        f"{fp}_callback_data",
    ]
    p = Path(fp)
    found = False
    if p.exists():
        convert(p)
        found = True
    else:
        for f in possible_files:
            if Path(f).exists():
                convert(f)
                found = True
    if not found:
        raise RuntimeError(f"Could not find the files to convert in {fp}!")
    else:
        print('\nDone. Run your bot to make sure everything works.')