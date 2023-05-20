from django.shortcuts import render
from django.http.response import HttpResponse
from djangoapp.models import Mobiles,Reviews,Carts,Orders
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from djangoapp.serializers import MobileSerializer,MobileModelserializer,Userserializer,Reviewserializer,Cartserializer,Orderserializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import validators

#serializers-convert queryset into json data

# Create your views here.

def home(request):
    return HttpResponse("hello world")


class MobilesView(APIView):
    def get(self,request,*args,**kwargs):
          qs=Mobiles.objects.all()
          serializer=MobileSerializer(qs,many=True)
          return Response(data=serializer.data)


    def post(self,request,*args,**kwargs):
        serializer=MobileSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get("name")
            price=serializer.validated_data.get("price")
            band=serializer.validated_data.get("band")
            display=serializer.validated_data.get("display")
            processor=serializer.validated_data.get("processor")
            Mobiles.objects.create(name=name,price=price,band=band,display=display,processor=processor)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MobileDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
         qs=Mobiles.objects.get(id=id)
         serializer=MobileSerializer(qs)
         return Response(data=serializer.data)
        except:
            return Response({"msg":"object doesnot exist"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(data=request.data)
            if serializer.is_valid():
                object.name=serializer.validated_data.get("name")
                object.pricr=serializer.validated_data.get("price")
                object.band=serializer.validated_data.get("band")
                object.display=serializer.validated_data.get("display")
                object.processosr=serializer.validated_data.get("processosr")
                object.save()
                return Response(data=serializer.data)
        except:
            return Response({"msg":"object doesnot exist"},status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,*args,**kwargs):
                id=kwargs.get("id")
                try:
                    object=Mobiles.objects.get(id=id)
                    object.delete()
                    return Response({"msg":"delete"})
                except:
                    return Response({"msg":"object doesnot exist"},status=status.HTTP_404_NOT_FOUND)


class MobileModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelserializer(qs,many=True)
        return Response(data=serializer.data)


    def post(self,request,*args,**kwargs):
        serializer=MobileModelserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MobileModelDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=Mobiles.objects.get("id")
        serializer=MobileModelserializer(id=id)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Mobiles.objects.get(id=id)
        serializer=MobileModelserializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=Mobiles.objects.get(id=id)
        object.delete()
        return Response({"mssg":"deleted"})

#list
#create
#retrive
#update
#destroy
#python native type------->queryset-==serialization
#querset---------->python native type==deserialization

class MobileViewSetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializers=MobileModelserializer(qs,many=True)
        return Response(data=serializers.data,status=status.HTTP_200_OK)

    def create(self,request,*args,**kwargs):
        serializer=MobileModelserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelserializer(object)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Mobiles.objects.get(id=id)
        serializer=MobileModelserializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


#custom method
class MobileModelViewSetView(viewsets.ModelViewSet):
    # authentication_class = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MobileModelserializer
    queryset = Mobiles.objects.all()


    @action(methods=["post"],detail=True)
    def add_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=Reviewserializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    #api/v4/oxegen/mobiles/{pid}/get_reviews
    # @action(methods=["get"],detail=True)
    # def get_reviews(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     mobile=Mobiles.objects.get(id=id)
    #     reviwes=mobile.reviews_set.all()
    #     serializer=Reviewserializer(reviwes,many=True)
    #     return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        serializer=Cartserializer(
            data=request.data,
            context=
            {"user":user,
            "product":mobile,
             }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    @action(methods=["get"],detail=False)
    def my_cart(self,request,*args,**kwargs):
        qs=Carts.objects.all()
        serializer=Cartserializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def orders(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=Orderserializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["get"],detail=False)
    def my_orders(self,request,*args,**kwargs):
        qs=Orders.objects.all()
        serializer=Orderserializer(qs,many=True)
        return Response(data=serializer.data)



#apiview,
class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer

#api/v4/myg/mobiles/{pid}/add_review

class ReviewView(viewsets.ModelViewSet):
    serializer_class = Reviewserializer
    queryset = Reviews.objects.all()

#api/v4/myg/mobiles/carts

class CartsView(viewsets.ModelViewSet):
  queryset = Carts.objects.all()
  serializer_class = Cartserializer
  # authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      return Carts.objects.filter(user=self.request.user)


class OrderView(viewsets.ModelViewSet):
    serializer_class = Orderserializer
    queryset = Orders.objects.all()

