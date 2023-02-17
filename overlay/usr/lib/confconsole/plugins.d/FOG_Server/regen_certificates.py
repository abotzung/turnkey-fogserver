'''Regenerate certificates'''
# Alexandre Botzung <alexandre.botzung@grandest.fr> - dec. 2022
import os


def run():
    if interactive:
        console.msgbox(
            'FOG root certificates',
            'WARNING : Regenerate certificates may cause already deployed FOG Client to NOT communicate properly with the server.',
            autosize=True)
        mavar=console.yesno("Are you sure to regenerate certificates for this FOG instance?")
        if mavar == "ok":
               os.system('regencert-fogserver')
               os.system('recompileipxe-fogserver')


