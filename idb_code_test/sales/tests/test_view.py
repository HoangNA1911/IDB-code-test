import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from sales.models import Sale
import json



@pytest.mark.django_db
def test_upload_csv(client):
    """Test API upload CSV file"""
    csv_content = \
        (b"date,region,product,quantity,price"
         b"\n2024-01-01,USA,Keyboard,5,100"
         b"\n2024-01-02,USA,Mouse,3,50")
    csv_file = SimpleUploadedFile("test_sales.csv", csv_content, content_type="text/csv")

    response = client.post(reverse('upload_csv'), {'file': csv_file})

    assert response.status_code == 201
    assert Sale.objects.count() == 2


@pytest.mark.django_db
def test_get_filtered_sales(client):
    """Test API lấy dữ liệu có phân trang"""
    Sale.objects.create(date="2024-01-01", region="USA", product="Keyboard", quantity=5, price=100)
    Sale.objects.create(date="2024-01-02", region="USA", product="Mouse", quantity=3, price=50)
    Sale.objects.create(date="2024-01-05", region="USA", product="Laptop", quantity=2, price=800)

    url = reverse('get_filtered_sales') + "?start_date=2024-01-01&end_date=2024-02-01&region=USA&page=1&per_page=2"
    response = client.get(url)

    assert response.status_code == 200
    data = json.loads(response.content)

    assert data['total_sales'] == 950
    assert data['average_sales'] == pytest.approx(316.67, 0.1)
    assert data['transaction_count'] == 3
    assert len(data['sales_list']) == 2


@pytest.mark.django_db
def test_get_filtered_sales_no_data(client):
    """Test API khi không có dữ liệu phù hợp"""
    url = reverse('get_filtered_sales') + "?start_date=2024-01-01&end_date=2024-02-01&region=USA&page=1&per_page=2"
    response = client.get(url)

    assert response.status_code == 200
    data = json.loads(response.content)

    assert data['total_sales'] == 0
    assert data['average_sales'] == 0
    assert data['transaction_count'] == 0
    assert len(data['sales_list']) == 0

