from ta_logistics_application.models import ApplicationFields
from datetime import datetime

"""
This class is where all data constants should go so that they can be accessed
from models, forms, and views without error.
"""


class DataDefinitions():

    def __init__(self):
        self.GPA_CHOICES = (
            (4.0, '4.0'),
            (3.9, '3.9'),
            (3.8, '3.8'),
            (3.7, '3.7'),
            (3.6, '3.6'),
            (3.5, '3.5'),
            (3.4, '3.4'),
            (3.3, '3.3'),
            (3.2, '3.2'),
            (3.1, '3.1'),
            (3.0, '3.0'),
            (-1, '< 3.0'),
        )
        self.GRADE_CHOICES = ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', '< C-',)
        self.FIELD_TYPE_CHOICES = (
            ('TEXT', 'Text String'),
            ('INT', 'Integer Number'),
            ('REAL', 'Decimal Number'),
        )

        self.COMFORT_LVLS = (
            'Expert',
            'Advanced',
            'Moderate',
            'Novince',
            'None',
        )

        self.INT_FIELD = "INT"
        self.FLOAT_FIELD = "FLOAT"
        self.TEXT_FIELD = "TEXT"
        self.COMFORT_LVL_FIELD = "CMFT"

    def getActiveSemesters(self):
        ret = []
        curYear = datetime.now().year
        for i in range(curYear, curYear + 3):
            ret.append(('FA' + str(i)[-2:], 'Fall ' + str(i)))
            ret.append(('SP' + str(i)[-2:], 'Spring ' + str(i)))
        return tuple(ret)

    def getOptionalFields(self):
        ret = []
        for i in ApplicationFields.objects.filter(is_default=False):
            ret.append((i.id, i.field_text))
        return tuple(ret)
