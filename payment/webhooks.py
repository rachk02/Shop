import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Commande
from .tasks import paiement_reussi


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                commande = Commande.objects.get(id=session.client_reference_id)
            except Commande.DoesNotExist:
                return HttpResponse(status=404)
                # mark order as paid
            commande.payer = True
            commande.stripe_id = session.payment_intent
            commande.save()

            paiement_reussi.delay(commande.id)

    return HttpResponse(status=200)
