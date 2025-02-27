# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import Sale
import datetime
from django.db.models import Sum, Avg, Count


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        df = pd.read_csv(file)
        df = df.dropna()
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        for _, row in df.iterrows():
            try:
                sale = Sale(
                    date=datetime.datetime.strptime(row['date'],
                                                    "%Y-%m-%d").date(),
                    region=row['region'],
                    product=row['product'],
                    quantity=row['quantity'],
                    price=row['price']
                )
                sale.save()

            except Exception as e:
                print(f"Error saving row: {row}, Error: {e}")

        return JsonResponse({'message': 'File uploaded successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_filtered_sales(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    region = request.GET.get('region')
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)

    sales = Sale.objects.filter(date__range=[start_date, end_date], region=region)

    total_sales = sales.aggregate(total_sales=Sum('price'))['total_sales'] or 0
    average_sales = sales.aggregate(avg_sales=Avg('price'))['avg_sales'] or 0
    transaction_count = sales.aggregate(transaction_count=Count('id'))[
                            'transaction_count'] or 0
    sales_list = sales.values('date', 'region', 'product', 'quantity', 'price')
    paginator = Paginator(sales_list, per_page)
    try:
        paginated_sales = paginator.page(page)
    except PageNotAnInteger:
        paginated_sales = paginator.page(
            1)
    except EmptyPage:
        paginated_sales = []
    return JsonResponse({
        'total_sales': total_sales,
        'average_sales': average_sales,
        'transaction_count': transaction_count,
        'sales_list': list(paginated_sales),
        'current_page': int(page),
        'total_pages': paginator.num_pages
    }, safe=False)
