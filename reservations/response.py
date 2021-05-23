from rest_framework.views import APIView
from rest_framework.response import Response


class Responses(APIView):
    def getResponse(self, data, status, meta={}, msg=''):
        return Response(status=status,
                        data={"status": status, "data": data, 'message': msg, 'meta': meta}, )

    def getErrorResponse(self, status, error, data={}, meta={},  msg=''):
        return Response(status=status,
                        data={"status": status, 'data': data, "error": error, 'message': msg, 'meta': meta}, )

