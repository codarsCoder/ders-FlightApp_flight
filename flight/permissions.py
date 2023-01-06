from rest_framework import permissions


class IsStafforReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):  # bu isadminuser metoduna tlayıca çkanksım bu kısmı tekrar düzenledi
        if request.method in permissions.SAFE_METHODS:  #gelen istek safe metodardansa   yani creat yapan birmetodsa yani get  bunar safe metodolarak geçer 
            return True     #true dön izin ver
        return bool(request.user and request.user.is_staff)   ## safe değilse post put vs   ozaman  user bilgisi varsa ve  userimiz staffsa true dönmüş olacak
     
    
    
    ### yada yukarısı için if request.method =  GET benzeri birşey  de yazılabilir  ama doğrusu böyle