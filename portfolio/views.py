from django.shortcuts import render, get_object_or_404
from .models import PortfolioItem, PortfolioImage
from django.templatetags.static import static

# Create your views here.
def home(request):
    portfolio_items = PortfolioItem.objects.all()
    return render(request, 'portfolio/home.html',{
        "items": portfolio_items,
        "metatitle": "Portfolio | Rudransh Joshi",
        "metadescription": "Explore my portfolio of previous works and discover how I can help you bring your ideas to life. As a skilled and experienced programmer, I have delivered high-quality results for numerous clients in the past. From blogs to chatbots to anime downloaders, my portfolio showcases my creativity, attention to detail, and commitment to excellence. Whether you're looking for inspiration or considering working with me, browse my portfolio now and see the possibilities.",
        "metaimage": static("portfolio/meta/previous-works.png"),
        "metakeywords": "portfolio, previous works",
    })

def portfolio_item(request, slug):
    item = get_object_or_404(PortfolioItem, slug=slug)
    images = PortfolioImage.objects.filter(portfolio_item=item)
    return render(request, 'portfolio/portfolio-item.html', {
        "item": item,
        "images": images,
        "metatitle": item.title,
        "metadescription": item.description,
        "metaimage": item.thumbnail.url,
        "metakeywords": item.tags
    })