from logsettings import get_logger_config
from path import path
import os

# Django settings for grading_controller project.
ROOT_PATH = path(__file__).dirname()
REPO_PATH = ROOT_PATH.dirname()
ENV_ROOT = REPO_PATH.dirname()

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PRINT_QUERIES = False

ADMINS = (
# ('Your Name', 'your_email@example.com'),
    'gacco tech', 'tech@gacco.org',
)

MANAGERS = ADMINS

#General
GRADING_QUEUES_TO_PULL_FROM=['open-ended']
MESSAGE_QUEUES_TO_PULL_FROM=['open-ended-message']
REQUESTS_TIMEOUT = 60    # seconds
TIME_BETWEEN_XQUEUE_PULLS = 20 #seconds.  Time between pull_from_xqueue checking to see if new submissions are on queue.
TIME_BETWEEN_EXPIRED_CHECKS = 30 * 60 #seconds.  Time between check_for_expired checking for expired/to reset submissions.
GRADER_SETTINGS_DIRECTORY = "grader_settings/" #Directory contains conf files with workflow settings for graders
MAX_NUMBER_OF_TIMES_TO_RETRY_GRADING=10 #Maximum number of times graders should fail before submission goes back to lms
DEFAULT_ESTIMATED_GRADING_TIME = 3 * 24 * 60 * 60 # seconds, amount of time to display to students
MIN_RANDOMIZED_PROCESS_SLEEP_TIME = 0 # Minimum time for a process to sleep, to avoid process collision
MAX_RANDOMIZED_PROCESS_SLEEP_TIME = 10 * 60 # Maximum time for a process to sleep, to avoid process collision
RECENT_NOTIFICATION_CHECK_INTERVAL = 1 * 24 * 60 * 60 #in seconds. Will not save a record for a student notification check if it happens at least this timeframe apart
CONFIG_PREFIX = '' # To append at the beginning of the config file name

#Config for specific graders
#ML
MIN_TO_USE_ML = 100 #Minimum number of instructor graded essays needed to use machine learning
MAX_TO_USE_ML = 300 #Maximum number of instructor graded essays to use for ml model creation
ML_MODEL_PATH=os.path.join(REPO_PATH,"ml_models/") # Path to save and retrieve ML models from.
TIME_BETWEEN_ML_CREATOR_CHECKS= 5 * 60 # seconds.  Time between ML creator checking to see if models need to be made.
TIME_BETWEEN_ML_GRADER_CHECKS= 20 # seconds.  Time between ML grader checking to see if models need to be made.
USE_S3_TO_STORE_MODELS= False #Determines whether or not models are placed in Amazon S3
S3_BUCKETNAME="OpenEnded"
S3_FILE_TIMEOUT = 10 * 60 # 10 minutes.
ML_ESTIMATED_GRADING_TIME= 5 * 60 #Estimated grading time for machine learning in seconds
TIME_BEFORE_REMOVING_STARTED_MODEL = 10 * 60 * 60 # in seconds, time before removing an ml model that was started (assume it wont finish)

#Peer
MIN_TO_USE_PEER=20 #Minimum instructor graded (calibration) essays before peer grading can be used
PEER_GRADER_COUNT = 1 #Number of peer graders for each submission
PEER_GRADER_MINIMUM_TO_CALIBRATE = 3 #Minimum number of calibration essays each peer grader will see
PEER_GRADER_MAXIMUM_TO_CALIBRATE = 6 #Maximum number of calibration essays each peer grader will see
REQUIRED_PEER_GRADING_PER_STUDENT = 3 #Student must peer grade at least 3 submissions for each question they answer.
PEER_GRADING_TIMEOUT_INTERVAL = 7 * 24 * 60 * 60 #In seconds.  Time before a student is marked as "finished grading" if they have not peer graded anything.
PEER_GRADE_FINISHED_SUBMISSIONS_WHEN_NONE_PENDING = False #If there are no pending subs and a peer grader comes along, give them a finished sub to
                                                          #allow them to grade something

#Error units are defined as the absolute value of student calibration score minus actual score divided by maximum score
#abs(student_score-actual_score)/max_score
#If they are above this error, student will keep seeing calibration essays until they hit peer_grader_maximum_to_calibrate
PEER_GRADER_MIN_NORMALIZED_CALIBRATION_ERROR = .5

PEER_GRADER_MIN_SIMILARITY_FOR_MATCHING = 1

#Submission Expiration
EXPIRE_SUBMISSIONS_AFTER = 5 * 24 * 60 * 60  #Seconds.  This will send submissions back to lms with failure
RESET_SUBMISSIONS_AFTER = 5 * 60 #Seconds.  This will make submissions that are locked by graders available for grading again

EDIT_SUBMISSIONS_PERMISSION = "change_submission"
SUBMITTERS_GROUP = "submitters"

GENERATE_COURSE_DATA_EVERY = 5 * 60 # Generate data about courses.  In seconds.  See metrics/tasks for more details.
COURSE_DATA_PATH = os.path.join(REPO_PATH, "data/course/")

#SQLite settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'essaydb', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

XQUEUE_INTERFACE = {
    "url": "http://127.0.0.1:3032",
    "django_auth": {
        "username": "lms",
        "password": "abcd"
    },
    "basic_auth": ('anant', 'agarwal'),
}

GRADING_CONTROLLER_INTERFACE = {
    "url": "http://127.0.0.1:3033",
    "django_auth": {
        "username": "xqueue_pull",
        "password": "abcd",
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(REPO_PATH, "django_cache"),
        }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    str(os.path.join(REPO_PATH, "static/")),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7q%=)6+vz$1zy!-vm4-k-^tj5q)hbgukoud%%$6edcxn^i^u)a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'edx_ora.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'edx_ora.wsgi.application'

TEMPLATE_DIRS = (
    str(os.path.join(REPO_PATH, "templates/"))
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'controller',
    'staff_grading',
    'south',
    'peer_grading',
    'ml_grading',
    'metrics',
    'djcelery',
    )

LOGGING = get_logger_config(debug=True)

SESSION_COOKIE_NAME="controller_session_id"

AWS_ACCESS_KEY_ID= ""
AWS_SECRET_ACCESS_KEY= ""

#Celery settings
#BROKER_URL = 'redis://localhost:6379/6'
#BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
BROKER_URL = 'amqp://celery:celery@internal-g2-rabbitmq-1495176630.ap-northeast-1.elb.amazonaws.com:5672//'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_DEFAULT_QUEUE = 'ora_celery'
CELERY_TIMEZONE = 'Asia/Tokyo'

# Cache settings for ml grading pending counts.  See controller/grader_interface.py
RECHECK_EMPTY_ML_GRADE_QUEUE_DELAY = 60

# Maximum number of graders for any single submission.
MAX_GRADER_COUNT = 10
