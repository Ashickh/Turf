from django.shortcuts import render
# from Turf.Turff.tasks import send_issue_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from Turff.tasks import *

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import *
import datetime

# Create your views here.

class UserView(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    serializer_class =  UserSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "User Fetching failed"}
        ground_list = User.objects.all()
        serializer = self.serializer_class(ground_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Users Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "User Creation failed"}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'User created successfully.'
     
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class GroundView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = GroundSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Ground Fetching failed"}
        user_list = Ground.objects.all()
        serializer = self.serializer_class(user_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Grounds Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Ground Creation failed"}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Ground created successfully.'
     
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PitchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PitchSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Pitch Fetching failed"}
        pitch_list = Pitch.objects.all()
        serializer = self.serializer_class(pitch_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Pitch Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Pitch Creation failed"}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Pitch created successfully.'
     
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TimeSlotView(generics.ListAPIView, generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    instance = TimeSlot.objects.all()
    # print(instance.values())

class TimeSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    lookup_field = 'id'

class BookingDatesView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookingDates.objects.all()
    serializer_class = BookingDateSerializer


    def post(self, request, *args, **kwargs):
     
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Booking Dates creation failed"}

        serializer = self.serializer_class(data=request.data)
            
        if serializer.is_valid(raise_exception=True):

            serializer.save()
        

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Booking Dates creation successful.'
    
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # value = BookingDates.total_price()
    # print(value)
    # instance = BookingDates.objects.all()
    # for i in instance:
    #     print(i.timeslot.price)
    # instance = BookingDates.objects.all()
    # # print(instance)
    # sum = 0
    # for i in instance:
        
    #     value = i.timeslot.price
    #     sum = sum + value
    # #     print(value)
    # # print(sum)
    # days = i.enddate-i.startdate
    # print(days)

    

class BookingDatesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookingDates.objects.all()
    serializer_class = BookingDateSerializer
    lookup_field = 'id'

class BookingView(generics.ListAPIView, generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Booking Fetching failed"}
        booking_list = Booking.objects.all()
        serializer = self.serializer_class(booking_list, many=True)

        val_list = Booking.objects.all().values_list()
        print(val_list)
        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Bookings Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)



    def post(self, request, *args, **kwargs):
     
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Booking failed"}

        serializer = self.serializer_class(data=request.data)

        id = request.data["cust_id"]
        ids = request.data["bookingdate_id"]

        send_mail = User.objects.get(id=id)
        e_mail = send_mail.email
        print(e_mail)
    


        if Booking.objects.filter(cust_id=id, bookingdate_id__in=ids).exists():

            print("already exists")

            response["status"] = status.HTTP_400_BAD_REQUEST
            response["message"] = "Dates already Exist"

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            print("ok")
            
            if serializer.is_valid(raise_exception=True):

                booking = serializer.save()
                # print(booking)
                
                booking.amount = booking.total_price()
            
                serializer.save()

                message = 'Your Turf Booking is Successful..! \n\n Turf Name:' "\n\n Ground: {author} \n\n Booking Date: {date}. \n \n Thank you.!"

                send_issue_mail.delay(e_mail, message)

                response["status"] = status.HTTP_200_OK
                response["data"] = serializer.data
                response["message"] = 'Booking successful.'
        
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):

        try:
                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Booking Removal Failed"}
                id = kwargs.get('id')
                user = Booking.objects.get(id=id)
                user.delete()
                response["status"] = status.HTTP_200_OK
            
                response["message"] = 'Booking Removed Successfully'
                return Response(response, status=status.HTTP_200_OK)
        except Exception:
                return Response(response, status= status.HTTP_400_BAD_REQUEST)

class LeagueView(APIView):

    serializer_class =  LeagueSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "League Fetching failed"}
        league_list = League.objects.all()
        serializer = self.serializer_class(league_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'League Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "League Creation failed"}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'League created successfully.'
        
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):

        try:
                response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Booking Removal Failed"}
                id = kwargs.get('id')
                user = Booking.objects.get(id=id)
                user.delete()
                response["status"] = status.HTTP_200_OK
            
                response["message"] = 'Booking Removed Successfully'
                return Response(response, status=status.HTTP_200_OK)
        except Exception:
                return Response(response, status= status.HTTP_400_BAD_REQUEST)

class MatchView(APIView):

    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Match Fetching failed"}
        match_list = Match.objects.all()
        serializer = self.serializer_class(match_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Match Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Match Creation failed"}

        serializer = self.serializer_class(data=request.data)

        # names = Match.find_match_name
        # print(names)

        if serializer.is_valid(raise_exception=True):
          
            serializer.save()
            

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Match created successfully.'
        
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,**kwargs):
       
                id = kwargs.get("id")
                instance = Match.objects.get(id=id)
                response={"status":status.HTTP_400_BAD_REQUEST,"message":"Match Details Updation Failed"}
                serializer = self.serializer_class(data=request.data, instance=instance)
                if serializer.is_valid():
                    serializer.save()
                    response["status"]=status.HTTP_200_OK
                    response["message"]="Match Updation Successfull"
                    response["data"]=serializer.data
                    return Response(response, status=status.HTTP_200_OK)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # except Exception as e:
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TeamsView(APIView):

    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Teams Fetching failed"}
        match_list = Teams.objects.all()
        serializer = self.serializer_class(match_list, many=True)

        response["status"] = status.HTTP_200_OK
        response["data"] = serializer.data
        response["message"] = 'Teams Fetched Succesfully'

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, "message": "Team Creation failed"}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            teams = serializer.save()
            teams.total_matches = teams.games_played()
            serializer.save()

            response["status"] = status.HTTP_200_OK
            response["data"] = serializer.data
            response["message"] = 'Team created successfully.'
        
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,**kwargs):
       
                id = kwargs.get("id")
                instance = Teams.objects.get(id=id)
                response={"status":status.HTTP_400_BAD_REQUEST,"message":"Team Details Updation Failed"}
                serializer = self.serializer_class(data=request.data, instance=instance)
                if serializer.is_valid(raise_exception=True):
                    teams = serializer.save()
                    teams.total_matches = teams.games_played()
                    serializer.save()
                    response["status"]=status.HTTP_200_OK
                    response["message"]="Team Updation Successfull"
                    response["data"]=serializer.data
                    return Response(response, status=status.HTTP_200_OK)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)