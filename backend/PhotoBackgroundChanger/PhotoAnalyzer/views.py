from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import io
import base64
import requests
from PIL import Image
from rembg import remove
from .serializers import PhotoSerializer
from dotenv import load_dotenv
from .models import Photo
from django.core.files.base import ContentFile

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
    def remove_background(self, photo_path):
        """Remove background from product photo using rembg"""
        try:
            # Read the image file
            with open(photo_path, 'rb') as input_file:
                input_data = input_file.read()

            # Remove background
            output_data = remove(input_data)

            # Convert to PIL Image
            product_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
            return product_image
        except Exception as e:
            raise Exception(f"Error removing background: {str(e)}")

    def generateAIBackground(self, context):
        """Generate a new background using DALL-E"""
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

    def composite_images(self, product_image, background_url):
        """Composite product image onto new background"""
        try:
            # Download background image
            bg_response = requests.get(background_url, timeout=30)
            bg_response.raise_for_status()
            background_image = Image.open(io.BytesIO(
                bg_response.content)).convert("RGBA")

            # Get dimensions
            product_width, product_height = product_image.size
            bg_width, bg_height = background_image.size

            # Use the larger dimensions to ensure both images fit well
            # Add some padding around the product
            padding = 50
            target_width = max(product_width + padding * 2, bg_width)
            target_height = max(product_height + padding * 2, bg_height)

            # Resize background to target size (maintain aspect ratio and crop if needed)
            bg_ratio = bg_width / bg_height
            target_ratio = target_width / target_height

            if bg_ratio > target_ratio:
                # Background is wider, fit to height
                new_bg_height = target_height
                new_bg_width = int(bg_ratio * new_bg_height)
            else:
                # Background is taller, fit to width
                new_bg_width = target_width
                new_bg_height = int(new_bg_width / bg_ratio)

            background_image = background_image.resize(
                (new_bg_width, new_bg_height), Image.Resampling.LANCZOS)

            # Crop background to target size (center crop)
            if new_bg_width > target_width or new_bg_height > target_height:
                left = (new_bg_width - target_width) // 2
                top = (new_bg_height - target_height) // 2
                right = left + target_width
                bottom = top + target_height
                background_image = background_image.crop(
                    (left, top, right, bottom))

            # Create composite image
            composite = Image.new(
                "RGBA", (target_width, target_height), (255, 255, 255, 255))
            composite.paste(background_image, (0, 0))

            # Calculate position to center the product on the background
            product_x = (target_width - product_width) // 2
            product_y = (target_height - product_height) // 2

            # Paste product image onto background (with alpha channel for transparency)
            composite.paste(product_image, (product_x,
                            product_y), product_image)

            # Convert to RGB (remove alpha channel for final output)
            composite_rgb = Image.new("RGB", composite.size, (255, 255, 255))
            composite_rgb.paste(composite, mask=composite.split()[
                                3] if composite.mode == "RGBA" else None)

            # Convert to base64 for sending to frontend
            buffer = io.BytesIO()
            composite_rgb.save(buffer, format="PNG", quality=95)
            img_str = base64.b64encode(buffer.getvalue()).decode()

            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            raise Exception(f"Error compositing images: {str(e)}")

    def post(self, request):
        photo_id = request.data.get("photo_id")
        context = request.data.get("context")

        try:
            if not photo_id:
                return Response({"message": "Photo ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Get the photo object
            photo = Photo.objects.get(id=photo_id)
            photo_path = photo.photo.path

            # Step 1: Remove background from product photo
            product_image = self.remove_background(photo_path)

            # Step 2: Generate new background
            background_url = self.generateAIBackground(context)

            # Step 3: Composite product onto new background
            final_image = self.composite_images(product_image, background_url)

            return Response({"background": final_image}, status=status.HTTP_200_OK)

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
