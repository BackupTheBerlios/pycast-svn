import app
from conf import CASTDB
from kirbybase import KirbyBase, KBError
import datetime

Casts = KirbyBase()
Cast2=Casts.select(CASTDB, ['name','url'],['',''],['name','url'])

print Cast2
