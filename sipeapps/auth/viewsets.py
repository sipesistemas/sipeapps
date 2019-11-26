from rest_framework import parsers, renderers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from sipeapps.auth.models import Token, Usuario
from sipeapps.auth.permissions import CheckPermission
from sipeapps.auth.serializers import AuthTokenSerializer, UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    permission_classes = (CheckPermission,)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['usuario']
        token, created = Token.objects.get_or_create(usuario=usuario)
        return Response({'usuario': UsuarioSerializer(instance=usuario).data, 'token': token.chave})


obtain_auth_token = ObtainAuthToken.as_view()
