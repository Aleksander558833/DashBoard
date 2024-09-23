from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Responses
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponsesForm

class PostList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] =self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'Post'

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = '/posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Назначаем текущего пользователя автором
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ResponseList(LoginRequiredMixin, ListView):
    form_class = ResponsesForm
    model = Responses
    template_name = 'response_list.html'
    context_object_name = 'response_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs

class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponsesForm
    model = Responses
    template_name = 'response_create.html'
    success_url = reverse_lazy('post_list')


    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = self.request.user
        response.post_id = self.kwargs['pk']
        response.save()
        return super().form_valid(form)

class ResponseDelete(DeleteView):
    model = Responses
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response_list')

def response_status(request, pk):
    response_objects = Responses.objects.get(pk=pk)
    response_objects.status = True
    response_objects.save()
    return redirect(reverse_lazy('response_list'))
