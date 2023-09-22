from datetime import date
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Menu, Employee, EmployeeVote
from .serializers import RestaurantSerializer, MenuSerializer, RestaurantMenuListSerializer, MenuByDaySerializer, \
    EmployeeRegistrationSerializer, VoteSerializer, WinningMenuSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


class RestaurantCreateView(generics.CreateAPIView):
    serializer_class = RestaurantSerializer
    # permission_classes = (IsAuthenticated,)


class MenuCreateView(LoginRequiredMixin, generics.CreateAPIView):
    serializer_class = MenuSerializer
    # permission_classes = (IsAuthenticated,)


class RestaurantMenuListView(generics.ListAPIView):
    serializer_class = RestaurantMenuListSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        queryset = Menu.objects.filter(restaurant_id=restaurant_id).order_by('date')

        return queryset
    # permission_classes = (IsAuthenticated,)


class MenuByDayListView(generics.ListAPIView):
    serializer_class = MenuByDaySerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        day_of_week = self.kwargs['day_of_week']
        day = day_of_week.capitalize()
        queryset = Menu.objects.filter(day_of_week=day).order_by('date')
        return queryset


class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration is successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def vote(request):
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        menu_id = serializer.validated_data['menu_id']
        restaurant_id = serializer.validated_data['restaurant_id']
        user = request.user

        try:
            menu = Menu.objects.get(pk=menu_id)
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Menu.DoesNotExist:
            return Response({"detail": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if EmployeeVote.objects.filter(employee=user, menu=menu, date=menu.date).exists():
            return Response({"detail": "You have already voted for this menu"}, status=status.HTTP_400_BAD_REQUEST)

        menu.votes += 1
        menu.save()

        EmployeeVote.objects.create(employee=user, menu=menu, date=menu.date)

        return Response({"detail": "Vote submitted successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WinningMenuView(APIView):
    def get(self, request):
        from django.db.models import F
        from django.db.models import Max

        winning_menu = Menu.objects.filter(date=date.today()).annotate(
            total_votes=F('votes')).aggregate(Max('total_votes'))

        if winning_menu:
            max_votes = winning_menu['total_votes__max']
            winning_menus = Menu.objects.filter(date=date.today(), votes=max_votes)
            serializer = WinningMenuSerializer(winning_menus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No winning menu found"}, status=status.HTTP_404_NOT_FOUND)

