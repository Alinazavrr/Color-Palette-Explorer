from django.urls import path
from .views import (
    ColorListCreateAPIView, ColorDetailAPIView,
    PaletteListCreateAPIView, PaletteDetailAPIView,
    ShareableURLAPIView, AccessPaletteAPIView
)

urlpatterns = [
    path('colors/', ColorListCreateAPIView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailAPIView.as_view(), name='color-detail'),
    path('palettes/', PaletteListCreateAPIView.as_view(), name='palette-list'),
    path('palettes/<int:pk>/', PaletteDetailAPIView.as_view(), name='palette-detail'),
    path('palettes/<int:palette_id>/share/', ShareableURLAPIView.as_view(), name='palette-share'),
    path('palettes/<str:encrypted_palette_id>/', AccessPaletteAPIView.as_view(), name='palette-access'),
]