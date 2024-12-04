from .forms import SearchForm, ProductForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
import logging

logger = logging.getLogger(__name__)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # ページネーション
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})

def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()

    # フォームが有効な場合の処理
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = results.filter(name__icontains=query)

    # カテゴリでフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        results = results.filter(category__name=category_name)

    # 価格フィルタリング
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)

    # ソート
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')
    else:
        results = results.order_by('name')
        # 履歴をセッションに保存
    if 'search_history' not in request.session:
        request.session['search_history'] = []
    search_history = request.session['search_history']

    # 現在の検索条件を履歴に追加
    search_history.insert(0, {
        'category': category_name,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    })
    request.session['search_history'] = search_history[:10]  # 履歴は最新10件まで保持

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'form': form,
        'page_obj': page_obj,
        'results': results,
        'search_history': search_history,
    })

def add_to_favorites(request, product_id):
    if 'favorites' not in request.session:
        request.session['favorites'] = []

    favorites = request.session['favorites']
    
    # ログにセッションの内容を記録
    logger.debug("お気に入りリスト（保存前）: %s", favorites)

    if product_id not in favorites:
        favorites.append(product_id)
        request.session['favorites'] = favorites
        request.session.modified = True  # セッションの変更を反映
    
    logger.debug("お気に入りリスト（保存後）: %s", request.session.get('favorites'))

    return redirect('favorites_page')

