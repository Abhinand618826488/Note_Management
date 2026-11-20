from django.shortcuts import render
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer,NotesSerializer,TaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from notes_app.models import NotesDb,TaskDb
from django.shortcuts import get_object_or_404


class RegistrationView(APIView):
    def post(self,request):
        seriaalizer_instance = RegisterSerializer(data = request.data)
        if seriaalizer_instance.is_valid():
            seriaalizer_instance.save()
            return Response(data={
                "Message" : "Registarion successful...!"

            })
        else:
            return Response(data=seriaalizer_instance.errors)

class NotesListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes, many=True)
        return Response(serializer_instance.data)

    def post (self,request):
        serializer_instance = NotesSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class NotesRetrieveUpdateDeleteView(APIView):
     permission_classes = [IsAuthenticated]

     def get_object(self,request,id):
          return get_object_or_404(NotesDb, id=id, user=request.user)
            
     def put(self, request, id):
        note = self.get_object(request,id)
        serializer_instance = NotesSerializer(note, data=request.data)
        if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(serializer_instance.data)
        return Response(serializer_instance.errors)

        
     def delete(self, request, id):
        note = self.get_object(request,id)
        note.delete()
        return Response(
            {"Message": "Note deleted successfully."},
    
        )

class LogoutView(APIView):
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message" :"Logout success..!"
        })
            



class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = TaskDb.objects.filter(user=request.user)

        serializer_instance =TaskSerializer(tasks, many=True)

        return Response(serializer_instance.data)

    def post(self, request):
        serializer_instance = TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)
        
        return Response(serializer_instance.errors)


class TaskRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, request, id):
        return get_object_or_404(TaskDb, id=id, user=request.user)

    def get(self, request, id):
        task = self.get_task(request, id)
        serializer_instance =TaskSerializer(task)
        return Response(serializer_instance.data)

    def put(self, request, id):
        task = self.get_object(request, id)

        serializer_instance = TaskSerializer(task,data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)


    def delete(self, request, id):
        self.get_task(request, id).delete()
        return Response({
            "Message" : "delete successfuly...!"
        })