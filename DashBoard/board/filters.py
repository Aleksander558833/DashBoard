from django_filters import FilterSet
from .models import Post, Responses


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }

class ResponseFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])
        self.filters['post'].label = 'Поиск по объявлению'
    class Meta:
        model = Responses
        fields = ('post',)