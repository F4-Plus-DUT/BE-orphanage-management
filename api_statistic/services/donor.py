from datetime import datetime, timedelta
from django.db.models import Sum
from django.template.loader import render_to_string

from api_activity.models import Activity
from api_statistic.models import Donor
from api_user.models import Profile
from base.services.send_mail import SendMail


class DonorService:
    @classmethod
    def get_donate_statistics(cls, start_date, end_date):
        donates = Donor.objects.filter(created_at__date__range=[start_date, end_date]).aggregate(
                                        total_donate=Sum("amount"))
        activities = Activity.objects.filter(created_at__date__range=[start_date, end_date]).aggregate(
                                            total_expense=Sum("expense"))
        total_donate = donates['total_donate'] or 0
        total_expense = activities['total_expense'] or 0
        date_statistic = []

        date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        date_end = datetime.strptime(end_date, '%Y-%m-%d').date()
        date = date_start
        while date <= date_end:
            donor = Donor.objects.filter(created_at__date=date).aggregate(
                                        donate=Sum("amount"))
            expense = Activity.objects.filter(created_at__date=date).aggregate(
                expense=Sum("expense"))
            date_statistic.append({
                "day": date,
                "donate": donor['donate'] or 0,
                "expense": expense['expense'] or 0
            })
            date = date + timedelta(days=1)

        response = {
            "total_donate": total_donate,
            "total_expense": total_expense,
            "details": date_statistic,
        }
        return response

    @classmethod
    def get_filter_query(cls, request):
        activity = request.query_params.get("activity")

        activity = None if activity == 'all' else activity

        filter_args = dict()

        if activity:
            filter_args.update(activity__id=activity)

        queryset = Donor.objects.filter(**filter_args)
        return queryset

    @classmethod
    def send_mail_to_donor(cls, serializer, email):
        data = serializer.data
        profile = Profile.objects.filter(id=data.get('profile')).first()
        activity = Activity.objects.filter(id=data.get('activity')).first()
        activity_name = activity.title if activity else ""
        if profile:
            personal_email = profile.personal_email if (not profile.account) or profile.personal_email != profile.account.email else None
            cls.send_mail(name=profile.name, email=profile.account.email, personal_email=personal_email,
                          send_email=True, activity_name=activity_name, amount=data.get("amount"), note=data.get("note")
                          )
            return
        if email and email != "" and not profile:
            cls.send_mail(name=email, email=email, personal_email=None, send_email=True,
                          activity_name=activity_name, amount=data.get("amount"), note=data.get("note"))
            return

    @classmethod
    def send_mail(
            cls,
            email=None,
            name=None,
            phone=None,
            personal_email=None,
            send_email=False,
            activity_name="",
            amount=0,
            note="",
            base_link="",
    ):
        if send_email:
            # token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f"{base_link}"
            content = render_to_string(
                "thank_for_donate.html",
                {"name": name, "activity_name": activity_name, "amount": amount, "note": note, "link": link, "token": ""},
            )
            SendMail.start(
                [email, personal_email], "[Thank for your donate]", content
            )
