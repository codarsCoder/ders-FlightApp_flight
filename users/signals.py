from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

## bu işlem sonrası biryere ekleme çağırma yapmıyoruz bu oto olarak çalışacak bu işlem views te işime yarayacak   
@receiver(post_save, sender=User) ## burada bir sinyal yazıldı ve save  işlemi sonrasında(post=sonra) işlem yap dendi , User  (sender) kayıt edildiğinde 
#sinyal yollayacağız  bu sinyali receiver yakalayacak  sinyal yollayan User yakalayan receiver
def create_Token(sender, instance=None, created=False, **kwargs):  #  sender bilgileri kullanlarak token oluşturacak ,created=False  token oluşturması  sonrsı oto true olacak  ve 
    if created:  #token create yapldıysa created true olacak 
        Token.objects.create(user=instance)   #instance  içinde artık token var
# djangodaki Token tablosuna User içeriğini kaydet 
# yukarıda create token  hazır bir metod onu çağırdık   
#