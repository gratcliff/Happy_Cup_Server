from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, Subscription, Merchandise, VarietyPack, ProductPromotion
from ..about_page.models import FullWidthSection, StaffMemberEntry
from ..locations.models import Location
from ..news.models import BlogPost
from ..cafe.models import Carousel, Cafe_hours, Cafe_content

from django.utils import timezone
from datetime import datetime, timedelta


class QuerySet(object):

	def __init__(self):

		self.coffee = Coffee.objects.all().select_related('roast','featured').prefetch_related('grinds', 'sizes')
		self.subscriptions = Subscription.objects.all().prefetch_related('coffees', 'coffees__grinds', 'coffees__sizes', 'coffees__roast')
		self.merchandise = Merchandise.objects.all().select_related('featured').prefetch_related('sizes')
		self.variety_pack = VarietyPack.objects.all().select_related('featured').prefetch_related('coffees', 'merchandise', 'merchandise__sizes', 'coffees__grinds')
		self.expired_promotions = ProductPromotion.objects.filter(expiration_date__lt=timezone.now(), expired=False)
		self.fullWidthSection = FullWidthSection.objects.all()
		self.staffMemberEntry = StaffMemberEntry.objects.all()
		self.location = Location.objects.all().select_related('type')
		self.blogPost = BlogPost.objects.all()
		self.cafeCarousel = Carousel.objects.all()
		self.cafeHours = Cafe_hours.objects.all()
		self.cafeContent = Cafe_content.objects.all()

		self.refresh_geocodes = Location.objects.filter(updated_at__lte=timezone.now()-timedelta(days=30)).first()


