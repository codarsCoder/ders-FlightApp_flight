from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from .models import Flight, Reservation
from rest_framework.permissions import IsAdminUser
from .permissions import IsStafforReadOnly
from datetime import datetime, date


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly,)  # bu ermission custom olrak yazıld permissions.py bak
    
    def get_serializer_class(self):  ## * kullanıcı staff ise serializerini ayrıntılı bir şekilde gösteren bir serializer ile değiştireceğiz bunnun için serializeri gösteren get_serializer_class metodunu override ediyoruz
        serializer = super().get_serializer_class()  ##  parentin serializerini aldık normalde FlightSerializer  olarak yazılı
        if self.request.user.is_staff:
            return StaffFlightSerializer   ## ! staff ise  StaffFlightSerializer  yoksa normal parentin serializerini     serializer_class = FlightSerializer  return edecek
        return serializer
    
    def get_queryset(self):   ## geçmişteki seferleri göstermenin bir anlamı olmayacak diye geçmiş uçuşları filtreleyeceğiz  
        now = datetime.now()  # şuanki zaman
        current_time = now.strftime('%H:%M:%S')  # şuanki zamanı  saat dakika saniye cinsindn aldık 
        today = date.today()   ##  normal tarihimizi aldık 
        
        if self.request.user.is_staff:
            return super().get_queryset()   ## kulanıcı staff ise normal tanımlanan, parentteki query seti kullan 
        
        else:
            queryset = Flight.objects.filter(date_of_departure__gt=today)  # veritabanında uçuş tarihi date_of_departure olarak saklanıyor  __gt   büyüktür demekti bugünden büyk 
            
            if Flight.objects.filter(date_of_departure=today):
                today_qs = Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time)   ## peki ynı gün içinde birde saate bakalım saat de geçmişse  etd saatinden büyük olanları alalım
                queryset = queryset.union(today_qs)   ## !  iki query seti birleştirmek için union metodu kullanılır 
            return queryset
    
    
class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    
    def get_queryset(self):  #   permissiona göre query setin sonucunu değiştireceğiz 
        queryset = super().get_queryset()  ## parentteki tüm bilgiyi al yani hemen üstteki  ReservationView e gelen bilgiyi aldık     queryset = Reservation.objects.all() eklindede yazabilirdik ama dinamik olmaz!!!
        if self.request.user.is_staff:      ### ! serializerde usere self.context["request"].user.id  ile ulaşabiliriz ama viewste bu şekilde ulaşılabilir
            return queryset
        return queryset.filter(user= self.request.user)
    

