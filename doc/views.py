from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .selializers import *
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from docm.pagination import MyPageNumberPagination
paginator= MyPageNumberPagination()
# Create your views here.
from rest_framework_simplejwt.authentication import JWTAuthentication



class UserRegistrationAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            return JsonResponse({ 'message': 'User registered successfully', 'status': status.HTTP_201_CREATED, 'success': True})
        except Exception as e:
             return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})           


class LogedInView(APIView):
    def post(self, request):
        try:

            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access': str(refresh.access_token), 
                    })    
            else:
                return JsonResponse({'success': True, 'status':status.HTTP_400_BAD_REQUEST, 'message': 'Invalid credentials'})
        except Exception as e:
             return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})           

class DocUploadedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        try:
            data=request.data
            created_by=request.user
            if request.user.is_superuser or request.user.is_staff:
                file=request.FILES['file']
                serializer_data=DocFileSerializer(data=data,context={'request': request})
                if serializer_data.is_valid():
                    serializer_data.save(uploaded_files=file, created_by=created_by)
                    return JsonResponse({'success': True, 'status':status.HTTP_201_CREATED, 'results':serializer_data.data})
                else:
                    return JsonResponse({'success': False, 'status':status.HTTP_501_NOT_IMPLEMENTED, 'message':serializer_data.errors})
            else:
                return JsonResponse({'success': False, 'status':status.HTTP_400_BAD_REQUEST, 'message':"You are not allow to create."})
        except Exception as e:
            return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})

    def get(self, request, pk=None):
        try:
            auth_user=self.request.user
            print(auth_user)
            if pk is not None:
                query=DocFile.objects.filter(id=pk).last()
                if query is not None:
                    serializer_data=DocFileDetailsSerializer(query, context={'request':request})
                    result={
                        "status":status.HTTP_200_OK,
                        "success":True,
                        "message":"File feteched successfully!",
                        "results":serializer_data.data
                    }
                    return Response(result)
                else:
                    return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"File not found."})
            else:
                created_by_q=request.GET.get("created_by" or None)
                page=request.GET.get("page")
                limit=request.GET.get("limit")
                if created_by_q is not None:
                    created_by=auth_user
                    query=DocFile.objects.filter(created_by=created_by).order_by("-created_at")
                    count=len(query)
                    if query is not None:
                        result_page= paginator.paginate_queryset(query, request)
                        if result_page is not None:
                            serializer_data=DocFileDetailsSerializer(result_page, many=True, context={'request': request})
                        else:
                            serializer_data=DocFileDetailsSerializer(many=True, context={'request': request})
                        result={
                            "status":status.HTTP_200_OK,
                            "success":True,
                            "message":"File feteched successfully!",
                            "results":serializer_data.data ,
                            "count":count                       
                        }
                        return Response(result)
                    else:
                        return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"You don't have any file."})
                else:
                    query=DocFile.objects.all().order_by("-created_at")
                    count=len(query)
                    if query is not None:
                        result_page= paginator.paginate_queryset(query, request)
                        if result_page is not None:
                            serializer_data=DocFileDetailsSerializer(result_page, many=True, context={'request': request})
                        else:
                            serializer_data=DocFileDetailsSerializer(many=True, context={'request': request})
                        result={
                            "status":status.HTTP_200_OK,
                            "success":True,
                            "message":"File feteched successfully!",
                            "results":serializer_data.data ,
                            "count":count                       
                        }
                        return Response(result)
                    else:
                        return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"There is no file."})
        except Exception as e:
            return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})

    authentication_classes = [JWTAuthentication] 
    def put(self, request, pk):
        try:
            if request.user.is_superuser or request.user.is_staff:
                query = DocFile.objects.filter(id=pk).last()
                if query is not None:
                    serializer_data=DocFileSerializer(instance=query, data=request.data, partial= True)
                    file = request.FILES['file'] if 'file' in request.FILES else None
                    if serializer_data.is_valid():
                        if file:
                            serializer_data.save(uploaded_files=file, updated_by=request.user)
                        else:
                            serializer_data.save(updated_by=request.user)
                        return JsonResponse({"status":status.HTTP_200_OK,"success":True,"result":serializer_data.data})
                    else:
                        return JsonResponse({"status":status.HTTP_400_BAD_REQUEST,"success":False,"message":serializer_data.errors})
                else:
                    return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"File not found."})
            else:
                return JsonResponse({'success': False, 'status':status.HTTP_400_BAD_REQUEST, 'message':"You are not allow to update."})

        except Exception as e:
            return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})



            
    def delete(self, request, pk):

        try:
            if request.user.is_superuser:
                doc_file= DocFile.objects.get(id=pk)
                if doc_file:
                    doc_file.delete()
                    return JsonResponse({"status": status.HTTP_204_NO_CONTENT, "success": True})
                else:
                    return JsonResponse({"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "File not found"})
                
            else:
                return JsonResponse({'success': False, 'status':status.HTTP_400_BAD_REQUEST, 'message':"You are not allow to delete."})

        except Exception as e:
            return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "success": False, "message":e.args[0]})



class DocFilePublicView(APIView):
    def get(self, request,pk=None):
        try:
            auth_user=self.request.user
            print(auth_user)
            if pk is not None:
                query=DocFile.objects.filter(id=pk).last()
                if query is not None:
                    serializer_data=DocFileDetailsSerializer(query, context={'request':request})
                    result={
                        "status":status.HTTP_200_OK,
                        "success":True,
                        "message":"File feteched successfully!",
                        "results":serializer_data.data
                    }
                    return Response(result)
                else:
                    return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"File not found."})
            else:
                page=request.GET.get("page")
                limit=request.GET.get("limit")
                query=DocFile.objects.all().order_by("-created_at")
                count=len(query)
                if query is not None:
                    result_page= paginator.paginate_queryset(query, request)
                    if result_page is not None:
                        serializer_data=DocFileDetailsSerializer(result_page, many=True, context={'request': request})
                    else:
                        serializer_data=DocFileDetailsSerializer(many=True, context={'request': request})
                    result={
                        "status":status.HTTP_200_OK,
                        "success":True,
                        "message":"File feteched successfully!",
                        "results":serializer_data.data ,
                        "count":count                       
                    }
                    return Response(result)
                else:
                    return JsonResponse({"success": False, "status":status.HTTP_404_NOT_FOUND, "message":"There is no file."})
        except Exception as e:
            return JsonResponse({"success": False, "status":status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"An error occurred while processing your request {e}."})

class UserStatusView(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def put(self, request, pk):
        query = User.objects.filter(id=pk).last()
        if query is not None:
            if request.user.is_superuser or request.user.is_staff:
                if request.user.is_staff:

                    if 'is_staff' in request.data:
                        query.is_staff = request.data.get('is_staff')
                        query.save()
                        return JsonResponse({"status": status.HTTP_200_OK, "success": True, "message": "is_staff status updated successfully"})
                
                elif request.user.is_superuser:
                    f=0
                    if 'is_staff' in request.data:
                        f=1
                        query.is_staff = request.data.get('is_staff')
                    if 'is_superuser' in request.data:
                        f=1
                        query.is_superuser = request.data.get('is_superuser')
                    if f:
                        query.save()
                        return JsonResponse({"status": status.HTTP_200_OK, "success": True, "message": "User status updated successfully"})
            return JsonResponse({"status": status.HTTP_403_FORBIDDEN, "success": False, "message": "Unauthorized"})
        else:
            return JsonResponse({"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "User not found"})
