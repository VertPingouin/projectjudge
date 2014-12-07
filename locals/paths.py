import os

def filepath(name, extension):
    if extension:
        return os.path.join('files', 'chinesesquid', name, name + '.' + extension)
    else:
        return os.path.join('files', 'chinesesquid', name)


