# import datetime
from datetime import date
from datetime import datetime
import pytz
# today = datetime.datetime.now(pytz.timezone('America/Panama'))
today=datetime.now(pytz.timezone('America/Panama'))
today = str(today)[0:10].split("-")
today.reverse()
return "-".join(today)
