from rest_framework import serializers
from .models import Flight,Reservation, Passenger


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )
        
        
class PassengerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Passenger
        fields = "__all__"
  

class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many=True, required=True)  ## bu kısmı yukarıdaki serializerden almış olduk
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")
        
         # gelen data içinde hem pessenger var ehmde flight bilgileri var bunların birbirinden ayrılmış olmaları lazım  aynı zamanda işlemi yapan user id yi de kaydetmek istiyoruz çünkü elimizde token bilgisi var request içinde id gelmiyor 
    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")   # pop passenger bilgilerini valdasyon yapılan datadan çıkartır aynı zamanda çıkarttığı datayıda bize verir böylece passenger bilgisi elimizde 
        validated_data["user_id"] = self.context["request"].user.id  # işlem yapan (istek atan) id yide validasyon dataya ekliyoruz
        reservation = Reservation.objects.create(**validated_data)  # ve validasyondan geçmiş gelmiş  datayı kaydediyoruz
        
        for passenger in passenger_data:  ## herbir pessenger verisini gezip alıyoruz
            pas = Passenger.objects.create(**passenger) ## pessengere aldığımız objeyi create ediyoruz pessenger tablosuna kaydediyoruz
            reservation.passenger.add(pas)   ## ***   şimdi sıra geldi reservation tablosundaki pessenger kolonuna pessenger bilgisini eklemeye, flight bir adet ama pessenger birden çok olabilecektir bu yüzden bu şekilde tek tek eklenmesini sağladık 
        
        reservation.save()
        return reservation
            
        
        
class StaffFlightSerializer(serializers.ModelSerializer):  ## staff için farklı ir serializer yazdık  ki daha  ayrıntılı bilgi alsınlar
    
    reservation = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservation",
        )
        
        
    
    