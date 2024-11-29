from rest_framework.response import Response


def get_Response(success,message,status_code,data=None):
    
    return Response(
        {
            "success":success,
            "message":message,
            "data": data if data else {}, 
        },
        status_code=status_code,
    )