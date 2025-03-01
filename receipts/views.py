from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date, time
import uuid
import re

# Dictionary to store receipts
receipt = {}

def calculate_points(retailer, total, items, purchase_date, purchase_time):
    points = sum(1 for c in retailer if c.isalnum())
    if total == int(total):
        points += 50
    if total % 0.25 == 0:
        points += 25
    points += (5 * len(items) // 2) if items else 0
    
    for item in items:
        item_shortDescription = item['shortDescription'].strip()
        if len(item_shortDescription) % 3 == 0:
            price = float(item['price'])
            points += round(price * 0.2)
    
    if purchase_date.day % 2 != 0:
        points += 6
    
    if time(14, 0) <= purchase_time <= time(16, 0):
        points += 10

    return points

def pattern_match(pattern, string):
    return re.fullmatch(pattern, string) is not None

def validate_retailer(value):
    return isinstance(value, str) and value.strip() and pattern_match(r"^[\w\s\-&]+$", value)

def validate_purchaseDate(value):
    try:
        datetime.strptime(value, "%Y-%m-%d").date()
        return True
    except ValueError:
        return False

def validate_purchaseTime(value):
    try:
        datetime.strptime(value, "%H:%M").time()
        return True
    except ValueError:
        return False

def validate_total(value):
    try:
        total = float(value)
        return total > 0
    except ValueError:
        return False

def validate_items(value):
    if not isinstance(value, list) or not value:
        return False
    for item in value:
        if not isinstance(item, dict) or not item:
            return False
        if 'shortDescription' not in item or 'price' not in item:
            return False
        if not pattern_match(r"^[\w\s\-&]+$", item['shortDescription']):
            return False
        try:
            float(item['price'])
        except ValueError:
            return False
    return True

class ReceiptCreate(APIView):
    def post(self, request, *args, **kwargs):
        global receipt
        try:
            data = request.data
            retailer = data.get('retailer')
            total = data.get('total')
            items = data.get('items')
            purchase_date = data.get('purchaseDate')
            purchase_time = data.get('purchaseTime')

            if not (validate_retailer(retailer) and validate_total(total) and validate_items(items) and validate_purchaseDate(purchase_date) and validate_purchaseTime(purchase_time)):
                return Response({"error": "The receipt is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            total = float(total)
            purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            purchase_time = datetime.strptime(purchase_time, "%H:%M").time()

            points = calculate_points(retailer, total, items, purchase_date, purchase_time)
            receipt_id = str(uuid.uuid4())
            receipt[receipt_id] = points

            return Response({"id": receipt_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "The receipt is invalid.", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReceiptRetrieve(APIView):
    def get(self, request, pk, *args, **kwargs):
        global receipt
        points = receipt.get(pk)
        if points is not None:
            return Response({"points": points}, status=status.HTTP_200_OK)
        return Response({"error": "No receipt found for that ID."}, status=status.HTTP_404_NOT_FOUND)
