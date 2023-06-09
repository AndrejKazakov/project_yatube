from .models import Post
from django_filters import FilterSet, DateFromToRangeFilter, NumberFilter, CharFilter, DateFilter


class PostFilter(FilterSet):
    cost_lt = NumberFilter(label='Цена', field_name='cost', lookup_expr='lt')
    title = CharFilter(label='Заголовок', lookup_expr='icontains')
    text = CharFilter(label='Текст поста', lookup_expr='icontains')
    date_start = DateFilter(label='Дата начала', field_name='pub_date', lookup_expr='gt')
    date_end = DateFilter(label='Дата окончания', field_name='end_date', lookup_expr='lt')

    class Meta:
        model = Post
        fields = ['title', 'text', 'cost_lt', 'date_start', 'date_end']
