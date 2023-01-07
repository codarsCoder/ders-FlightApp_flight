## flight api  yi test edeceğiz diye dosya başlığına yazdık 
from django.urls import reverse ## url name
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from flight.views import FlightView
from flight.models import Flight
from django.contrib.auth.models import User,Token

class FlightTestCase(APITestCase):
    
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    today = date.today()
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.flight = Flight.objects.create(   ## bu kısım olmadanda test yapılabilir şimdi biz hazır bir obje ıluşturduk
            flight_number='123ABC',
            operation_airlines='THY',
            departure_city='Adana',
            arrival_city='Ankara',
            date_of_departure=f'{self.today}', 
            etd=f'{self.current_time}',
        )
        self.user = User.objects.create_user(  ##USER OLUŞTURDUK
            username='admin',   
            password='Aa654321*'
        )
        self.token = Token.objects.get(user=self.user)
        ## urls kısmında basename="flights"  eklemeyi unutma
    def test_flight_list_as_non_auth_user(self):
        print(reverse('flights-list'))
        request = self.factory.get("/flight/flights/") ##  BURAYA ŞİMDİ BİR GET İSTEĞİ ATTIK  reverse(flights-list) revere metodu endpointi kısaca yazmayı sağlar reverse(flights-list)    ("/flight/flights/") ile aynı  
        response = FlightView.as_view({'get':'list'})(request)  ## BU KISMI PROGRAM KENDİSİ 
        self.assertEquals(response.status_code, 200)   # dönen status code 200 mü
        self.assertNotContains(response, 'reservation')  ## staf olmayan usere reservation bilgisi gelmeyecekti   bu kısım doğru çalışırsa bir ok daha alacağız
        self.assertEqual(len(response.data), 0)  ## dönen data sıfır mı  yani yoksa true verecek
    
   
    def test_flight_list_as_staff_user(self):  ##BİRTANEDE STAFF OLMUŞ USER İÇİN TEST YAZDIK 
        request = self.factory.get('/flight/flights/', HTTP_AUTHORIZATION=f'Token {self.token}')  ## bir istek attık endpoint ekledik aynı zamanda token ekledik ki staff olup olmadığını kontrol edelim
        self.user.is_staff = True
        self.user.save()
       # force_authenticate(request, user=self.user)  ##YUKARIDA TOKEN EKLEDİK AMA  TOKEN GÖNDERMEDEN  force_authenticate  İLE SANKİ STAFFMIŞ GİBİ YETKİLENDİR VARSAY DEDİK
        # request.user = self.user   token olmasaydı buraya bu şekilde user de eklememiz lazım ki staff useri request içinde bulabilsin
        response = FlightView.as_view({'get': 'list'})(request)  #yine istek attık 
        self.assertEqual(response.status_code, 200)   ## yukarıdaki işlemler sonrası ben 200 kodunun dönmesini bekliyorum burada döndü mü diye soruyorum 
        self.assertContains(response, 'reservation')  ## dönene response içinde reservation geçiyor mu , çünkü staff olan user bunu görecekti
        self.assertEqual(len(response.data), 0)  ##  data döndümü onu kontrol edebiliriz dönen data bir mi yani data varsa true verecek