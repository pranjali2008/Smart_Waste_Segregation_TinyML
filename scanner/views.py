import os
import sys

from django.shortcuts import redirect, render
from .models import WasteScan


# code folder ko Python path me add karna
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(BASE_DIR, 'code')

if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from infer_waste import classify_image


def scanner(request):

    if request.method == 'POST':

        image = request.FILES.get('waste_image')

        if image:

            # Image ko database/media me save karna
            scan = WasteScan.objects.create(
                image=image
            )

            # Uploaded image ka actual path
            image_path = scan.image.path

            # AI model aur labels ka path
            model_path = os.path.join(
                BASE_DIR,
                'models',
                'waste_classifier_float32.tflite'
            )

            labels_path = os.path.join(
                BASE_DIR,
                'models',
                'labels.txt'
            )

            # AI se waste classify karna
            predicted_class, confidence = classify_image(
                model_path,
                labels_path,
                image_path
            )

            # Waste type ke according Green Coins
            coin_rewards = {
                'plastic': 10,
                'paper': 10,
                'cardboard': 10,
                'metal': 15,
                'organic': 10,
                'battery': 20,
            }

            green_coins = coin_rewards.get(
                predicted_class.lower(),
                    5
            )

            # Waste type ke according Carbon Credits
            carbon_rewards = {
                'plastic': 5,
                'paper': 3,
                'cardboard': 3,
                'metal': 6,
                'organic': 4,
                'battery': 8,
            }

            carbon_credits = carbon_rewards.get(
                predicted_class.lower(),
                2
            )

            # Scan ke saath coins save karna
            scan.waste_type = predicted_class
            scan.confidence = confidence
            scan.green_coins = green_coins
            scan.carbon_credits = carbon_credits
            scan.save()

            return render(
                request,
                'scanner/scanner.html',
                {
                    'message': 'Image successfully uploaded!',
                    'scan': scan,
                    'prediction': predicted_class,
                    'confidence': confidence,
                    'green_coins': green_coins,
                    'carbon_credits': carbon_credits,
                }
            )

    return render(
        request,
        'scanner/scanner.html'
    )

def dashboard(request):

    scans = WasteScan.objects.all().order_by('-scanned_at')

    total_scans = scans.count()
    total_coins = sum(scan.green_coins for scan in scans)
    total_carbon_credits = sum(scan.carbon_credits for scan in scans)

    organic_count = scans.filter(
        waste_type__iexact='organic'
    ).count()

    battery_count = scans.filter(
        waste_type__iexact='battery'
    ).count()

    recyclable_count = scans.filter(
        waste_type__iexact='plastic'
    ).count()

    recyclable_count += scans.filter(
        waste_type__iexact='paper'
    ).count()

    recyclable_count += scans.filter(
        waste_type__iexact='cardboard'
    ).count()

    return render(
        request,
        'scanner/dashboard.html',
        {
            'scans': scans,
            'total_scans': total_scans,
            'total_coins': total_coins,
            'total_carbon_credits': total_carbon_credits,
            'organic_count': organic_count,
            'recyclable_count': recyclable_count,
            'battery_count': battery_count,
        }
    )

def clear_scans(request):
    if request.method == 'POST':
        WasteScan.objects.all().delete()

    return redirect('dashboard')