from rest_framework.urls import path
from Department import apis

urlpatterns = [
    path('list/<int:d_id>/',apis.DepartmentDetailsApiView.as_view())

]