
from rest_framework.views import APIView
from rest_framework.response import Response


class Responses(APIView):
    def getResponse(status, data, meta={}, msg=''):     # return successful response
        return Response(status=status,
                        data={"status": status, "data": data, 'message': msg, 'meta': meta}, )

    def getErrorResponse(status, error, data={}, meta={},  msg=''):     # return error response
        return Response(status=status,
                        data={"status": status, 'data': data, "error": error, 'message': msg, 'meta': meta}, )