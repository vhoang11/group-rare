from grouprareapi.models import RareUser
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    rare_user = RareUser.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if rare_user is not None:
        data = {
            'id': rare_user.id,
            'bio': rare_user.bio,
            'profile_image_url': rare_user.profile_image_url,
            'created_on': rare_user.created_on,
            'active': rare_user.active,
            'uid': rare_user.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the levelupapi_gamer table
    rare_user = RareUser.objects.create(
        # id=request.data['id'],
        bio=request.data['bio'],
        profile_image_url=request.data['profile_image_url'],
        created_on=request.data['created_on'],
        active=request.data['active'],
        uid=request.data['uid']
    )

    # Return the gamer info to the client
    data = {
        'id': rare_user.id,
        'bio': rare_user.bio,
        'profile_image_url': rare_user.profile_image_url,
        'created_on': rare_user.created_on,
        'active': rare_user.active,
        'uid': rare_user.uid,
    }
    return Response(data)
