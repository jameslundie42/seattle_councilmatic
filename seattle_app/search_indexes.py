from councilmatic_search.search_indexes import BillIndex
from haystack import indexes
from .models import SeattleBill
from django.conf import settings
import pytz

app_timezone = pytz.timezone(settings.TIME_ZONE)

class SeattleBillIndex(BillIndex, indexes.Indexable):

    def get_model(self):
        return SeattleBill

