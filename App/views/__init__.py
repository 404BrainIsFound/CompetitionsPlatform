# blue prints are imported 
# explicitly instead of using *
from .index import index_views
from .auth import auth_views
from .competition import comp_views
from .student import student_views

views = [index_views, auth_views, comp_views, student_views] 
# blueprints must be added to this list