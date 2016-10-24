from django.core.management.base import BaseCommand

from django.utils.crypto import get_random_string

import os


class Command(BaseCommand):
    help = "Generate a new SECRET_KEY"



    def handle(self, *args, **options):
    	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    	key = get_random_string(50, chars)

    	
    	return 'export SECRET_KEY="%s"' % (key,)

        