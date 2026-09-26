from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from .models import Resource, Comment
from .forms import ResourceForm, SignUpForm, CommentForm


def home(request):
    total_resources = Resource.objects.count()
    total_subjects = Resource.objects.values('subject').distinct().count()
    recent_resources = Resource.objects.all()[:5]

    context = {
        'total_resources': total_resources,
        'total_subjects': total_subjects,
        'recent_resources': recent_resources,
    }
    return render(request, 'resources/home.html', context)


def resource_list(request):
    # Start with all resources
    queryset = Resource.objects.all()

    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    subject = request.GET.get('subject', '')
    semester = request.GET.get('semester', '')
    resource_type = request.GET.get('resource_type', '')
    branch = request.GET.get('branch', '')
    sort_by = request.GET.get('sort', 'newest')

    # Apply search filter using Q objects
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    # Apply categorical filters
    if subject:
        queryset = queryset.filter(subject__icontains=subject)

    if semester:
        queryset = queryset.filter(semester=semester)

    if resource_type:
        queryset = queryset.filter(resource_type=resource_type)

    if branch:
        queryset = queryset.filter(branch=branch)

    # Apply sorting
    if sort_by == 'popular':
        queryset = queryset.order_by('-upvotes', '-created_at')
    elif sort_by == 'downloads':
        queryset = queryset.order_by('-download_count', '-created_at')
    else:  # newest (default)
        queryset = queryset.order_by('-created_at')

    context = {
        'resources': queryset,
        'search_query': search_query,
        'subject_query': subject,
        'semester_query': semester,
        'type_query': resource_type,
        'branch_query': branch,
        'sort_by': sort_by,
        'resource_types': Resource.ResourceType.choices,
        'branches': Resource.Branch.choices,
    }
    
    # Return partial template for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'resources/partials/resource_grid.html', context)
    
    return render(request, 'resources/resource_list.html', context)


def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    comments = resource.comments.all()
    comment_form = CommentForm(user=request.user)
    context = {
        'resource': resource,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def add_comment(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.author_name = request.user.username
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Return 405 for non-POST requests
        return redirect('resources:resource_detail', pk=pk)
    return redirect('resources:resource_detail', pk=pk)


@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, 'Resource added successfully!')
            return redirect('resources:resource_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceForm()

    return render(request, 'resources/add_resource.html', {'form': form})


def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    action = request.GET.get('action', 'download')

    if action == 'external' and resource.external_url:
        # Open external link - don't increment download count
        return redirect(resource.external_url)
    
    # Default: download file
    if resource.file:
        # Increment download count only for file downloads
        resource.download_count += 1
        resource.save()
        return redirect(resource.file.url)
    elif resource.external_url:
        # Fallback to external URL if no file
        return redirect(resource.external_url)
    else:
        messages.error(request, 'No file or URL associated with this resource.')
        return redirect('resources:resource_detail', pk=pk)


def upvote_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.upvotes += 1
    resource.save()
    messages.success(request, 'Thanks for the upvote!')
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'resources/partials/upvote_button.html', {'resource': resource})
    
    # Safe fallback redirect - avoid using HTTP_REFERER directly
    return redirect('resources:resource_detail', pk=pk)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('resources:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})