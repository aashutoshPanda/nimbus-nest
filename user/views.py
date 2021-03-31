# python imports
import os
from django.core.files import File as DjangoCoreFile
import shutil
import secrets
from mysite.settings import BASE_DIR
import cloudinary.uploader
from rest_framework.parsers import MultiPartParser, JSONParser
from itertools import chain
# django imports
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# local imports
from .models import Profile
from folder.models import Folder
from .serializers import ProfileSerializer, UserSerializer
from .decorators import *
from file.decorators import *
from folder.serializers import FolderSerializer, FolderSerializerWithoutChildren
from file.serializers import FileSerializer
from folder.decorators import allow_id_root_helper, check_id_folder, check_id_not_root, check_is_owner_folder, check_request_attr, update_last_modified_folder
from folder.utils import set_recursive_trash
from .utils import is_valid_email

RECOVER = ["id", "TYPE"]


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
        data = ProfileSerializer(profile).data
        return Response({'token': token.key, **data}, status=status.HTTP_201_CREATED)


class Register(APIView):
    def post(self, request):
        if User.objects.filter(username=request.data.get('username'),).exists():
            return Response({"message": "Already Present"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            username=request.data.get('username'),
            email=request.data.get('username'),
        )
        user.set_password(str(request.data.get('password')))
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
        root_folder = Folder(name="ROOT", owner=user)
        root_folder.save()
        profile.root = root_folder
        profile.save()
        data = ProfileSerializer(profile).data
        return Response({'token': token.key, **data}, status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        print(request.user)
        request.user.auth_token.delete()
        return Response({"message": "logged out"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = ProfileSerializer(profile).data
        return Response(data=data)

    def patch(self, request):
        profile = Profile.custom_objects.get_or_none(user=request.user)
        if(profile == None):
            return Response(data={"message": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)

        if(not(profile.user == request.user or request.user.is_staff)):
            return Response(data={"message": "Not allowed"}, status=status.HTTP_401_UNAUTHORIZED)

        if("email" in request.data):
            new_email = request.data["email"]
            if(is_valid_email(new_email)):
                updated = True
                profile.user.email = new_email
            else:
                return Response(data={"message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        if("gender" in request.data):
            new_gender = request.data["gender"]
            if(new_gender in [1, 2, 3, 4]):
                updated = True
                profile.gender = new_gender
            else:
                return Response(data={"message": "Invalid gender"}, status=status.HTTP_400_BAD_REQUEST)

        if("capacity" in request.data):
            if(not request.user.is_staff):
                return Response(data={"message": "Admin Rights required"}, status=status.HTTP_401_UNAUTHORIZED)

            updated = True
            new_capacity = request.data["capacity"]
            profile.capacity = new_capacity

        if(updated):
            profile.user.save()
            profile.save()

        data = ProfileSerializer(profile).data
        return Response(data=data, status=status.HTTP_200_OK)


class ProfilePicture(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    def post(self, request, format=None):
        try:
            file = request.data.get('picture')
            user_profile = Profile.objects.get(user=request.user)
            cloudinary_response = cloudinary.uploader(
                file, width=450, height=450, crop="thumb", gravity="faces", zoom=0.65, radius="max")
            user_profile.profile_picture_url = cloudinary_response["secure_url"]
            user_profile.save()
            data = ProfileSerializer(user_profile).data
            return Response(data=data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class ListOfUsers(APIView):

    def get(self, request):
        data = UserSerializer(User.objects.all(), many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class Favourites(APIView):

    def get(self, request):

        # folders
        folders = Folder.objects.filter(
            favourite=True, owner=request.user, trash=False)
        folders = FolderSerializerWithoutChildren(folders, many=True).data
        for folder in folders:
            folder["type"] = "folder"
        # files
        files = File.objects.filter(
            favourite=True, owner=request.user, trash=False)
        files = FileSerializer(files, many=True).data
        for file in files:
            file["type"] = "file"

        # combined
        result_list = list(chain(folders, files))

        return Response(data=result_list, status=status.HTTP_200_OK)


class Recent(APIView):

    def get(self, request):
        # folders
        folders = Folder.objects.filter(owner=request.user, trash=False)
        folders = FolderSerializerWithoutChildren(folders, many=True).data
        for folder in folders:
            folder["type"] = "folder"
        # files
        files = File.objects.filter(owner=request.user, trash=False)
        files = FileSerializer(files, many=True).data
        for file in files:
            file["type"] = "file"

        # combined
        result_list = list(chain(folders, files))

        return Response(data=result_list, status=status.HTTP_200_OK)


class Trash(APIView):

    def get(self, request):
        # folders
        folders = Folder.objects.filter(owner=request.user, trash=True)
        folders = FolderSerializerWithoutChildren(folders, many=True).data
        for folder in folders:
            folder["type"] = "folder"
        # files
        files = File.objects.filter(owner=request.user, trash=True)
        files = FileSerializer(files, many=True).data
        for file in files:
            file["type"] = "file"

        # combined
        result_list = list(chain(folders, files))

        return Response(data=result_list, status=status.HTTP_200_OK)


class SharedWithMe(APIView):

    def get(self, request):
        # folders
        folders = request.user.shared_with_me_folders.all()
        folders = FolderSerializerWithoutChildren(folders, many=True).data
        for folder in folders:
            folder["type"] = "folder"
        # files
        files = request.user.shared_with_me_files.all()
        files = FileSerializer(files, many=True).data
        for file in files:
            file["type"] = "file"

        # combined
        result_list = list(chain(folders, files))

        return Response(data=result_list, status=status.HTTP_200_OK)


class Path(APIView):
    @ check_request_attr(["id", "TYPE"])
    @ check_id_with_type
    # allow id in folder enabled
    def get(self, request, *args, **kwargs):
        id = request.GET["id"]
        type = request.GET["TYPE"]

        if(type == "FILE"):
            start_node = File.objects.get(id=id)
        elif(type == "FOLDER"):
            request = allow_id_root_helper(request)
            id = request.GET["id"]
            start_node = Folder.objects.get(id=id)

        if(start_node.owner != request.user):
            return Response(data={"message": "Not allowed"}, status=status.HTTP_401_UNAUTHORIZED)

        path = []
        while(start_node.parent != None):
            path.append({
                "name": start_node.name,
                "id": start_node.id
            })
            start_node = start_node.parent
        path.append({
            "name": start_node.name,
            "id": start_node.id
        })
        path.reverse()
        return Response(data=path)


class RecoverFolder(APIView):

    @ check_request_attr(["id"])
    @ check_id_folder
    @ check_id_not_root
    @ check_is_owner_folder
    def get(self, request, * args, **kwargs):
        # check if folder's parent is in Trash
        # if in trash move this folder to root
        # break link between them
        id = request.GET["id"]
        root_folder = request.user.profile.root
        folder = Folder.objects.get(id=id)
        parent_folder = folder.parent

        if(parent_folder.trash):
            folder.parent = root_folder
            folder.save()
        set_recursive_trash(folder, False)
        data = FolderSerializer(folder).data
        return Response(data=data, status=status.HTTP_200_OK)


class RecoverFile(APIView):
    @ check_request_attr(["id"])
    @ check_id_file
    @ check_is_owner_file
    def get(self, request, * args, **kwargs):
        # check if file's parent is in Trash
        # if in trash move this file to root
        # break link between them

        id = request.GET["id"]
        root_folder = request.user.profile.root
        file = File.objects.get(id=id)
        parent_folder = file.parent
        if(parent_folder.trash):
            file.parent = root_folder
        file.trash = False
        file.save()
        data = FileSerializer(file).data
        return Response(data=data, status=status.HTTP_200_OK)


def create_local_folder(parent_path, folder_name):
    new_folder_path = parent_path.joinpath(folder_name)
    new_folder_path.mkdir(parents=True, exist_ok=True)
    return new_folder_path


def create_folder(parent_path, folder):
    folder_name = folder.name
    new_folder_path = create_local_folder(parent_path, folder_name)
    for child_folder in folder.children_folder.all():
        create_folder(new_folder_path, child_folder)
    for child_file in folder.children_file.all():
        child_file.download_to(new_folder_path)
    return new_folder_path


class DownloadFolder(APIView):

    def get(self, request, * args, **kwargs):
        id = request.GET["id"]
        folder = Folder.objects.get(id=id)
        folder_name = folder.name
        transaction = secrets.token_hex(4)
        zip_dir = (BASE_DIR).joinpath(transaction)
        # base_folder_name = folder.name
        new_folder = create_folder(zip_dir, folder)
        new_folder_zip = shutil.make_archive(
            folder_name+transaction, 'zip', str(new_folder))
        print("new path zip = ", new_folder_zip)
        local_file = open(folder_name+transaction+".zip", 'rb')
        djangofile = DjangoCoreFile(local_file)
        file = File(file=djangofile,
                    name=f"{folder_name}.zip",
                    owner=request.user,
                    parent=None)
        print("done till here")
        file.save()
        data = FileSerializer(file).data
        return Response(data=data, status=status.HTTP_200_OK)
