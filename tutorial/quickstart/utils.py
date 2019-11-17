from quickstart.serializers import SignUpSerializer,UserSerializer

def jwt_response_payload_handler(token,user=None,request=None):
    user = SignUpSerializer(user,context={'request':request}).data
    return {
        'token': token,
        'username':user['username'],
        'email':user['email'],
        'url':user['url']
    }