'''Regenerate secrets'''
# Alexandre Botzung <alexandre.botzung@grandest.fr> - dec. 2022
import os


def run():
    if interactive:
        console.msgbox(
            'FOG secrets',
            'WARNING : Regenerate secrets may cause already deployed FOG Nodes to NOT communicate properly with this server.',
            autosize=True)
        mavar=console.yesno("Are you sure to regenerate secrets for this FOG instance?")
        if mavar == "ok":
               os.system('regensecret-fogserver')

