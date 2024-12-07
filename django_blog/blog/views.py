from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from django_blog.blog.forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView
from .models import Comment, Post
from .forms import CommentForm


# عرض تسجيل الدخول
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'auth/login.html', {'error': 'المستخدم أو كلمة المرور غير صحيحة'})
    return render(request, 'auth/login.html')


# تسجيل الخروج
def user_logout(request):
    logout(request)
    return redirect('login')


# عرض نموذج التسجيل
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


# عرض وتحرير الملف الشخصي
@login_required
def user_profile(request):
    if request.method == 'POST':
        # معالجة التحديثات
        new_email = request.POST.get('email')
        request.user.email = new_email
        request.user.save()
        return redirect('profile')
    return render(request, 'auth/profile.html', {'user': request.user})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_list')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class CommentListView(View):
    """View لعرض التعليقات الخاصة بمقالة معينة"""
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """إنشاء تعليق جديد على المقالة"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """تعديل تعليق موجود"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """حذف تعليق"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})