import os

wrong = ['9789899945418',
'9789899568792',
'9789898872036',
'9789896167509',
'9789727088430',
'9789723706444',
'9789722537629',
'5601072496293'
]

directory = "/home/hugo/Development/saleor/saleor/static/placeholders"
to_download = list()

def search_import_file() -> str:
    _directory = wrong
    for element in _directory: 
        if os.path.isdir(os.path.join(directory,element)):
            os.chdir(os.path.join(directory,element))
            _file = [i for i in os.listdir(os.path.curdir)]
            os.chdir(directory)
            if len(_file) == 0:
                to_download.append(element)
    return to_download

to_download = search_import_file()
print(len(to_download))
print((to_download))

