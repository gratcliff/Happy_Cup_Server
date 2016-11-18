from django.forms import ModelForm
from .models import VarietyPack, Subscription
import stripe


class VarietyPackForm(ModelForm):

    """ This form adds custom validation for the variety pack product.
    The clean() method ensures that an admin will not create an "empty" variety pack. 
    """

    class Meta:
        model = VarietyPack
        fields = '__all__'


    def clean(self):
    	cleaned_data = super(VarietyPackForm, self).clean()
    	coffee_qty = cleaned_data.get('coffee_qty')
    	coffees = len(cleaned_data.get('coffees'))
    	merchandise = len(cleaned_data.get('merchandise'))

    	if coffee_qty == 0 and coffees > 0:
    		self.add_error('coffee_qty', 'Enter the number of bags of coffee included in this pack.')

    	if coffee_qty > 0 and coffees == 0:
    		self.add_error('coffees', 'Select the coffees available in this pack.')

    	if coffees == 0 and merchandise == 0 and coffee_qty == 0:
    		self.add_error('coffees', 'No products are included in this pack.')
    		self.add_error('merchandise', 'No products are included in this pack.')



class SubscriptionForm(ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        cleaned_data = super(SubscriptionForm, self).clean()
        coffees = len(cleaned_data.get('coffees'))
        wholesale = len(cleaned_data.get('wholesale_coffees'))
        if self.instance.stripe_id:
            id = self.instance.stripe_id
        else:
            amount = int(cleaned_data.get('price')*100)
            id = "%s-week-plan" % (cleaned_data.get('frequency'))

        if coffees == 0 and wholesale == 0:
            self.add_error('coffees', 'No products are included in this subscription.')
            self.add_error('wholesale_coffees', 'No products are included in this subscription.')
            return
        try:
            plan = stripe.Plan.retrieve(id)
            if cleaned_data.get('frequency'):
                self.add_error('frequency', 'This subscription plan already exists. ID: %s' % (id,))
            return
        except Exception as e:
            print e.args
            interval = 'week'
            currency = 'usd'
            name = "%s Week Plan" % (cleaned_data.get('frequency'),)
            plan = stripe.Plan.create(
                    amount=amount,
                    currency=currency,
                    interval=interval,
                    name=name,
                    id=id
                )
            if plan.get('id'):
                cleaned_data['stripe_id'] = plan['id']

            







    


