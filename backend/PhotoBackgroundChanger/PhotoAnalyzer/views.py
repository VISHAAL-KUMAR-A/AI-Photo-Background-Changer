from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
from .serializers import PhotoSerializer
from dotenv import load_dotenv
from .models import Photo

load_dotenv()

# Create your views here.


class add_photo(APIView):
    def post(self, request):
        photo = request.FILES.get("photo")
        try:
            if photo:
                photo_serializer = PhotoSerializer(data={"photo": photo})
                if photo_serializer.is_valid():
                    photo_instance = photo_serializer.save()
                    return Response({
                        "message": "Photo added successfully",
                        "photo_id": photo_instance.id
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Photo not valid",
                        "errors": photo_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Photo not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Error adding photo",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class remove_photo(APIView):
    def delete(self, request):
        photo_id = request.data.get("photo_id")
        try:
            if photo_id:
                photo = Photo.objects.get(id=photo_id)
                photo.delete()
                return Response({"message": "Photo removed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Photo not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Error removing photo",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class generate_background(APIView):
    def generateAIBackground(self, photo, context):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set in environment variables")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Build prompt
        if context:
            prompt = f"Generate a professional product photo background with the following context: {context}. The background should be clean, modern, and suitable for e-commerce product photography."
        else:
            prompt = "Generate a professional, clean, modern product photo background suitable for e-commerce. The background should be neutral and complement the product."

        try:
            # Generate image using DALL-E 3
            # Note: DALL-E 3 only supports n=1 and specific sizes: "1024x1024", "1792x1024", "1024x1792"
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard"
            )
            return response.data[0].url
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def post(self, request):
        photo_id = request.data.get("photo_id")
        context = request.data.get("context")

        try:
            if photo_id:
                photo = Photo.objects.get(id=photo_id)
                background = self.generateAIBackground(photo, context)
                return Response({"background": background}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Photo ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Photo.DoesNotExist:
            return Response({"message": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({
                "message": "Configuration error",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Error generating background",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
