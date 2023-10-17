import secrets
import string

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializers, ChangePasswordSerializers, ForgotPasswordSerializers, \
    ForgotPasswordConfirmSerializers, DeleteAccountSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        serializers = RegisterSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response('Вы успешно зарегистрировались вам отправлено письмо на почту', status=201)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        serializer = DeleteAccountSerializer(data=request.data)

        if serializer.is_valid():
            deletion_password = serializer.validated_data.get('password')

            if deletion_password and user.check_password(deletion_password):
                user.delete()
                return Response("Аккаунт успешно удален.", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Неверный пароль для удаления аккаунта.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ActivateAPIView(APIView):
#
#     def get(self, request,  activation_code):
#         user = get_object_or_404(User, activation_code=activation_code)
#         user.is_active = True
#         user.activation_code = ''
#         user.save()
#         return Response('Успешно')
class ActivateAPIView(View):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()

        # Отправить HTML-шаблон с задним фоном и картинкой
        return render(request, 'activation_success.html')


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializers(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        serializers.is_valid()
        return Response('Вы успешно сменили пароль', status=200)


class ForgotPasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено на эту почту письмо с кодом для восстановления пароля', status=200)


class ForgotPasswordConfirmAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordConfirmSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Ваш пароль успешно обновлен', status=200)

