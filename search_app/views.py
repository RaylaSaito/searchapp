from django.shortcuts import render
from .models import Product, Category, SearchHistory, Favorite
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def add_search_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        if query:
            SearchHistory.objects.create(user=request.user, query=query)
            return JsonResponse({'success': True, 'message': '検索履歴に追加しました。'})
        return JsonResponse({'success': False, 'message': 'キーワードを入力してください。'})
    return JsonResponse({'success': False, 'message': '無効なリクエストです。'})

@login_required
def toggle_favorite(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            if not created:
                favorite.delete()
                return JsonResponse({'success': True, 'message': f'{product.name} をお気に入りから削除しました。'})
            return JsonResponse({'success': True, 'message': f'{product.name} をお気に入りに追加しました。'})
        except Exception as e:
            logger.error(f"Error in toggle_favorite: {e}")
            return JsonResponse({'success': False, 'message': 'サーバーエラーが発生しました。'}, status=500)
    return JsonResponse({'success': False, 'message': '無効なリクエストです。'}, status=400)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'search.html', {'favorites': favorites})

@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    if not history.exists():
        return render(request, 'search_history.html', {'history': None, 'message': '検索履歴はありません。'})
    return render(request, 'search.html', {'history': history})

@login_required
def favorites_api(request):
    """
    ユーザーのお気に入りリストをJSON形式で返すビュー
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    favorite_list = [
        {
            'id': fav.product.id,
            'name': fav.product.name,
            'price': fav.product.price,
        }
        for fav in favorites
    ]
    return JsonResponse({'favorites': favorite_list}, safe=False)

@login_required
def favorites_list_api(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    favorites_data = [
        {
            'id': fav.product.id,
            'name': fav.product.name,
            'price': fav.product.price,
        }
        for fav in favorites
    ]
    return JsonResponse({'favorites': favorites_data})

@login_required
def search_view(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', 'name')

    results = Product.objects.all()

    if query:
        results = results.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        results = results.filter(category__id=category)

    if min_price:
        results = results.filter(price__gte=min_price)

    if max_price:
        results = results.filter(price__lte=max_price)

    if sort == 'price_asc':
        results = results.order_by('price')
    elif sort == 'price_desc':
        results = results.order_by('-price')
    else:
        results = results.order_by('name')

    # お気に入りリスト
    favorites = request.user.favorite_entries.all()  # 修正済み

    # 検索履歴
    search_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')

    categories = Category.objects.all()

    return render(request, 'search.html', {
        'query': query,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'results': results,
        'categories': categories,
        'search_history': search_history,
        'favorites': favorites,  # お気に入りをテンプレートに渡す
    })

