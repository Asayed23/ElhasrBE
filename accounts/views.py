from django.shortcuts import render
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework import permissions,generics
from django.shortcuts import render,get_object_or_404
from rest_framework import status
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .models import UserProfile, accountToken
from .serializer import UserSerializer, RegisterSerializer,ChangePasswordSerializer

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
    parser_class = (FileUploadParser,)






class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    http_method_names = ['get', 'post', 'head', 'put']
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):

        if 'username' in request.data and  User.objects.filter(

                username=request.data['username']).exists():

            return Response({"errorCode": "username exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = UserProfile()


        if 'phoneNumber' in request.data and not UserProfile.objects.filter(

                phoneNumber=request.data['phoneNumber']).exists():
            user = serializer.save()
            # print("hello")
            user_profile.user = user
            
            user_profile.phoneNumber = request.data['phoneNumber']
            if 'fullName' in request.data:
                user_profile.fullName = request.data['fullName']

            if 'email' in request.data:
                user_profile.email = request.data['email']
            
            if 'villaArea' in request.data:
                user_profile.villaArea = request.data['villaArea']

            if 'accountToken' in request.data and not request.data['accountToken']=="":

                user_token=accountToken()
                # user=get_object_or_404(User, id=user.id)
                user_token.userId=user
                user_token.token=request.data["accountToken"]
                user_token.save()
            user_profile.save()
            user_response=UserSerializer(user, context=self.get_serializer_context()).data
            user_profile_response=UserProfile.objects.get(user=user_response['id'])






            return Response({
                "id": user_response['id'],
                "username": user_response['username'],



                "phoneNumber": user_profile_response.phoneNumber,
                "fullName": user_profile_response.fullName,

                'email':user_profile_response.email,

                'villaArea':user_profile_response.villaArea,
                "token": AuthToken.objects.create(user)[1],
            })


        else:
            return Response({"errorCode": "phone number exist"}, status=status.HTTP_400_BAD_REQUEST)



        return Response({"errorCode":6003}, status=status.HTTP_400_BAD_REQUEST)





from django.contrib.auth import login,authenticate

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)

        if 'password' in request.data and 'username' in request.data:
            user1 = authenticate(request, username=request.data['username'], password=request.data['password'])
        else:
            return Response({"errorCode": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if user1 is not None:
            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data['user']

            login(request, user)
            User = get_user_model()
            user_response=User.objects.filter(username=request.data['username'])
            user_profile_response = UserProfile.objects.get(user=request.user.id)

            if 'accountToken' in request.data and not request.data['accountToken']=="":
                if not accountToken.objects.filter(token=request.data["accountToken"]).exists():
                    user_token=accountToken()
                    userid=get_object_or_404(User, username=request.data['username'])
                    user_token.userId=userid
                    user_token.token=request.data["accountToken"]
                    user_token.save()


            return Response({
                "id": request.user.id,
                "username": request.user.username,
                "phoneNumber": user_profile_response.phoneNumber,
                "fullName": user_profile_response.fullName,
                'email':user_profile_response.email,
                'villaArea':user_profile_response.villaArea,

                "token": AuthToken.objects.create(user)[1],
            })
        else:
            return Response({"errorCode": "BAD Request"}, status=status.HTTP_400_BAD_REQUEST)

        return super(LoginAPI, self).post(request, format=None)




from shutil import copyfile
from django.contrib.admin.views.decorators import staff_member_required          

@staff_member_required
def download_page(request):
    context={}     
    copyfile("./db.sqlite3", "./static/db.sqlite3")
    return render(request, "./static/db.sqlite3" , context)





from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
# from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    http_method_names = ['get', 'post', 'head', 'put','update']
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("oldPassword")):
                return Response({"oldPassword": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("newPassword"))
            self.object.save()
            response = {
                'status': 'success',    
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class restpassapi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    http_method_names = ['get', 'post', 'head', 'put']
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        username =request.data['username']


        u=get_object_or_404(User, username=username)
        u.set_password(request.data['password'])
        u.save()
        
        return Response({"status":"success"})
        


# def policy_page(request):
#     return render(request, "sppolicy.html" , {})








class numbercheckApi(APIView):
    # permission_classes = ()  # <-- And here


    def post(self, request, *args, **kwargs):
        
        if UserProfile.objects.filter(

                phoneNumber=request.data['phoneNumber']).exists():

            return Response({"Date": "phone number exist"})
        else:
            return Response({"Date": "phone number not exist"})
 

class editprofileApi(APIView):
    # permission_classes = ()  # <-- And here


    def post(self, request, *args, **kwargs):
        

        
        
        userId=request.data['userId']
        
        user=get_object_or_404(User, id=userId)
        userProfile_response=UserProfile.objects.get(user=user)
        if "fullName" in request.data and not request.data["fullName"]=="":
           
            userProfile_response.fullName=request.data["fullName"]
        if "villaArea" in request.data and not request.data["villaArea"]=="":
           
            userProfile_response.villaArea=request.data["villaArea"]
        if "email" in request.data and not request.data["email"]=="":
           
            userProfile_response.email=request.data["email"]
            
        userProfile_response.save()
        userProfile_response=UserProfile.objects.filter(user=user).values()

        
        
        return Response(userProfile_response)