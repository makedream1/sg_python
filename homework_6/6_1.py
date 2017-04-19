import re

words = ['afoot', 'catfoot', 'dogfoot', 'fanfoot', 'foody', 'foolery', 'foolish', 'fooster', 'footage', 'foothot',
         'footle', 'footpad', 'footway', 'hotfoot', 'jawfoot', 'mafoo', 'nonfood', 'padfoot', 'prefool', 'sfoot',
         'unfool',
         'Atlas', 'Aymoro', 'Iberic', 'Mahran', 'Ormazd', 'Silipan', 'altered', 'chandoo', 'crenel', 'crooked', 'fardo',
         'folksy', 'forest', 'hebamic', 'idgah', 'manlike', 'marly', 'palazzo', 'sixfold', 'tarrock', 'unfold'
         ]
valid = []
regexp = re.compile(r'foo')
for item in words:
    if re.findall(regexp, item):
        valid.append(item)
print(valid)

