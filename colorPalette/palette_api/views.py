from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Color, Palette
from .serializers import ColorSerializer, PaletteSerializer

# Colors View
class ColorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Color.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ColorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Color.objects.filter(creator=self.request.user)

# Palettes View
class PaletteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Palette.objects.all()
    serializer_class = PaletteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Palette.objects.filter(Q(creator=user) | Q(users_with_access=user))

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class PaletteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Palette.objects.all()
    serializer_class = PaletteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Palette.objects.filter(Q(creator=user) | Q(users_with_access=user))

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj




class ShareableURLAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, palette_id):
        try:
            palette = Palette.objects.get(id=palette_id, creator=request.user)
            shareable_url = request.build_absolute_uri(f"/palettes/{palette_id}/")
            return Response({'shareable_url': shareable_url}, status=status.HTTP_200_OK)
        except Palette.DoesNotExist:
            return Response({'error': 'Palette not found'}, status=status.HTTP_404_NOT_FOUND)

class AccessPaletteAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PaletteSerializer

    def get_object(self):
        try:
            encrypted_palette_id = self.kwargs.get('encrypted_palette_id')
            palette_id = Palette.decode_id(encrypted_palette_id)
            palette = Palette.objects.get(id=palette_id)
            return palette
        except (Palette.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Invalid palette ID'}, status=status.HTTP_404_NOT_FOUND)