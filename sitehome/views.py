from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.templatetags.static import static
from .models import MySocialLink, TimelineItem, ContactMessage, HireRequest
from blog.models import BlogPost
from portfolio.models import PortfolioItem
import requests

def validate_recaptcha(response):
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': response
    }
    result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()
    return result['success'], result['score']

# Create your views here.
def error_400(request, exception):
    context = {
        "error_code": 400,
        "error_title": "Bad Request",
        "error_msg": "Your request couldn't be processed.",
        "error_tip": "Please try again later."

    }
    return render(request, 'error.html', status=400, context=context)

def error_403(request, exception):
    context = {
        "error_code": 403,
        "error_title": "Forbidden",
        "error_msg": "You don't have permission to access this page.",
        "error_tip": "But there are plenty of other things you can access."

    }
    return render(request, 'error.html', status=403, context=context)

def error_404(request, exception):
    context = {
        "error_code": 404,
        "error_title": "Not Found",
        "error_msg": "Sorry, we couldn't find this page.",
        "error_tip": "But dont worry, you can find plenty of other things on our homepage."

    }
    return render(request, 'error.html', status=404, context=context)

def error_500(request):
    context = {
        "error_code": 500,
        "error_title": "Internal Server Error",
        "error_msg": "Your request couldn't be processed at this moment.",
        "error_tip": "But you should definitely try again later."

    }
    return render(request, 'error.html', status=500, context=context)

def home(request):
    # TODO: {
    #   ADD DATA TO MODELS, DEPLOY ON INSTANCE USING NGINX WITH BROTLI, LINK THE DOMAIN, ENABLE SSL, PUSH TO GITHUB
    #   RESUME.PDF
    #   REVIEWS & TESTIMONIALS
    #   EMAIL SENDING
    #   DASHBOARD PAGE: DELETE ACCOUNT, CHANGE EMAIL
    #   FORM VALIDATION USING DJANGO FORMS
    # }

    timeline = TimelineItem.objects.order_by("-date")[:3]
    portolioitems = PortfolioItem.objects.order_by("-date")[:4]
    blogposts = BlogPost.objects.order_by("-publish_date")[:4]
    return render(request, 'sitehome/home.html', {
        "timeline": timeline,
        "portfolio": portolioitems,
        "posts": blogposts,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        "metaimage": static("hello-world.png"),
        "resume": static("resume.pdf")
    })

def contact(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']
        recatpcha_response = request.POST['g-recaptcha-response']
        success, score = validate_recaptcha(recatpcha_response)
        if success and score>=0.7:
            contact = ContactMessage(name=fullname, email=email, message=message, score=score)
            contact.save()
            # send mail later
            messages.success(request, "Your message has been sent successfully.", extra_tags="border-green-400")
        else:
            messages.error(request, "You seem to be a bot. Your message wasn't sent. Please try again later, if you think it's a mistake.", extra_tags="border-red-400")
        
        return redirect('home')

def allmylinks(request):
    links = MySocialLink.objects.order_by('name')
    return render(request, 'sitehome/allmylinks.html', {
        "links": links,
        "fontawesome_kit_id": settings.FONTAWESOME_KIT_ID,
        "metatitle": "All My Links | Rudransh Joshi",
        "metadescription": f"All links to my socials in one place. Connect to me on GitHub, YouTube, Instagram, Discord, Hackerrank, Reddit and {len(links) - 6} others.",
        "metaimage": static("sitehome/meta/allmylinks.png"),
        "metakeywords": "contact, all my links, github, instagram, rudransh, rudransh joshi, discord, reddit"
    })

def hireme(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            name = request.POST['fullname']
            email = request.POST['email']
            budget = request.POST['budget']
            timeframe = request.POST['timeframe']
            service = request.POST['service']
            message = request.POST['message']
            success, score = validate_recaptcha(request.POST['g-recaptcha-response'])
            if success and score>=0.7:
                hirerequest = HireRequest(user=request.user, name=name, email=email, budget=budget, timeframe=timeframe, service=service, message=message, score=score)
                hirerequest.save()
                try:
                    payload = {
                        "content": f"Hey <@544832319589187584>,\nA new hire request from **{name}** has arrived.\n\n**Email:** {email}\n**Budget:** ${budget}\n**Timeframe:** {timeframe}\n**User:** {request.user.username}\n_ _",
                        "embeds": [
                            {
                                "title": f"{service}",
                                "description": f"{message}",
                                "color": 65280,
                                "footer": {
                                    "text": f"ReCaptcha Score: {score}"
                                },
                                "timestamp": hirerequest.timestamp.isoformat()
                            }
                        ],
                        "attachments": []
                    }
                    requests.post(settings.DISCORD_WEBHOOK_URL, json=payload)
                except Exception:
                    pass
                messages.success(request, "Your hire request has been sent successfully.", extra_tags="border-green-400")
            else:
                messages.error(request, "You seem to be a bot. Your message wasn't sent. Please try again later, if you think it's a mistake.", extra_tags="border-red-400")
        else:
            messages.error(request, "You need to be logged in to send a hire request. Please log in <b><a href='/blog/login/?ref=/hire-me/'>here</a></b>.", extra_tags="border-red-400")

    return render(request, 'sitehome/hireme.html', {
        "metatitle": "Hire Me | Rudransh Joshi",
        "metadescription": "Looking for a reliable and talented freelancer for your next project? You've come to the right place! I specialize in Web Development, Scripting & Automation, Chatbots, and have worked with numerous clients in the past. Whether you're an individual or a startup looking for quality work, I'm here to help. My approach is unique, fast, and genuine, and I always strive to exceed my clients' expectations. Contact me today to discuss your project and see how I can bring your ideas to life.",
        "metaimage": static("sitehome/meta/hire-me.png"),
        "metakeywords": "hire me, freelancer, web, scripting, automation, chatbots, django, discord, tailwind",
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY
    })

def timeline(request):
    objects = TimelineItem.objects.order_by('-date')
    # Group items having same year together
    timeline = {}
    for item in objects:
        if not item.date.year in timeline.keys():
            timeline[item.date.year] = [item]
        else:
            timeline[item.date.year].append(item)

    return render(request, 'sitehome/timeline.html', {
        "timeline": timeline,
        "metatitle": "Rudransh Joshi | Timeline",
        "metadescription": "My journey over time and some of my achievements I earned over a past few years. I don't exactly know what you were expecting but, I guess, Never gonna give you up would suffice xD",
        "metaimage": static("sitehome/meta/timeline.png")
    })