"""
globals file for hubspot3
"""
__version__ = "3.1.6"

BASE_URL = "https://api.hubapi.com"

OBJECT_TYPE_COMPANIES = 'companies'
OBJECT_TYPE_CONTACTS = 'contacts'
OBJECT_TYPE_PRODUCTS = 'products'

DATA_TYPE_BOOL = 'bool'
DATA_TYPE_DATETIME = 'datetime'
DATA_TYPE_ENUM = 'enumeration'
DATA_TYPE_NUMBER = 'number'
DATA_TYPE_STRING = 'string'

VALID_PROPERTY_DATA_TYPES = (
    DATA_TYPE_BOOL,
    DATA_TYPE_DATETIME,
    DATA_TYPE_ENUM,
    DATA_TYPE_NUMBER,
    DATA_TYPE_STRING,
)

WIDGET_TYPE_BOOLEAN_CHECKBOX = 'booleancheckbox'
WIDGET_TYPE_CHECKBOX = 'checkbox'
WIDGET_TYPE_DATE = 'date'
WIDGET_TYPE_FILE = 'file'
WIDGET_TYPE_NUMBER = 'number'
WIDGET_TYPE_RADIO = 'radio'
WIDGET_TYPE_SELECT = 'select'
WIDGET_TYPE_TEXT = 'text'
WIDGET_TYPE_TEXTAREA = 'textarea'

VALID_PROPERTY_WIDGET_TYPES = (
    WIDGET_TYPE_BOOLEAN_CHECKBOX,
    WIDGET_TYPE_CHECKBOX,
    WIDGET_TYPE_DATE,
    WIDGET_TYPE_FILE,
    WIDGET_TYPE_NUMBER,
    WIDGET_TYPE_RADIO,
    WIDGET_TYPE_SELECT,
    WIDGET_TYPE_TEXT,
    WIDGET_TYPE_TEXTAREA,
)

ASSOCIATION_TYPE_CONTACT_TO_COMPANY = 1
VALID_ASSOCIATION_TYPES = (
    ASSOCIATION_TYPE_CONTACT_TO_COMPANY,
)
