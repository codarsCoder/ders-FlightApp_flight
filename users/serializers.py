from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(  # modelde required değil bu yüzden burada tekrar şarta bağlaadık
        required=True,    
        validators = [UniqueValidator(queryset=User.objects.all())]  # ve uniq olsun istedik  tüm user bilgilerinde arayacakve tweek olmasını sağlayacak  UniqueValidator  rest api nin getirdiği özellik 
        )
    
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password], # validate_password  djangonun kendi kullandığı validasyon sadece password validasyonu yapacak
        style = {"input_type" : "password"}
    )
    password2 = serializers.CharField(
        write_only = True, #sadece data alırken yaz get işlemlerinde gösterme 
        required = True,
        style = {"input_type" : "password"}
    )
    
    class Meta:
        model = User
        fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'password2']
        
        # object validasyon:  normalde mevcut olan bir fieldle ilgili validasyon işlemi için   validate_fieldismi yazılarak kullanılır  ama burada biz çoklu fields validasyonu yapacağız bu yüzden object validasyon metodunu kullandık
    def validate(self, data):   #override ederek validate işlemlerine password kontrolü ekledik
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"message" : "Password fields didnt match!"}
            )
        return data
    
    
    def create(self, validated_data):   #data içine pass2 eklendi ama tabloda yeri yok burada onu çıkarıp sonra kayıt işlemini yapmak için create override ettik 
        password = validated_data.get("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    ## normalde token işlemlerinde arka planda  token serialize ediliyor , biz sinyale token oluşturduk token serializer sadece key dönüyor user bilgilerinide eklemek istiyoruz
    ## bunun için  TokenSerializer import   TOKEN SERİALİZER İÇİNE USER  BİLGİLERİNİDE KOYACAĞIZ
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
    
    
class CustomTokenSerializer(TokenSerializer):  ##   custom ile artık kendi  UserTokenSerializerini   değil benim yazdığım serializeri dön diyoruz
    user = UserTokenSerializer(read_only = True)
    
    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")     ## TOKEN SERİALİZER SADECE KEY DÖNÜYORDU ARTIK USER BİLGİLERİNİDE DÖNECEK
        
        ### SON BİR İŞLEM KALDI settings.py/base.py içine  REST_AUTH_SERIALIZERS = {
   ### 'TOKEN_SERIALIZER': 'users.serializers.CustomTokenSerializer',}  ekliyoruz
    

        
