from rest_framework.response import Response


def get_Response(success,message,status,data=None,tokens=None):
    
    return Response(
        {
            "success":success,
            "message":message,
            "tokens":tokens,
            "data": data if data else {}, 
        },
        status=status,
    )