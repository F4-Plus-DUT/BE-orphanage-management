from datetime import datetime, timedelta
from django.db.models import Sum
from django.template.loader import render_to_string

from api_activity.models import Activity
from api_children.models import Children
from api_statistic.models import Donor
from api_user.models import Profile, Account
from api_user.statics import RoleData
from base.services.send_mail import SendMail


class DonorService:
    @classmethod
    def get_box_dashboard(cls):
        children = Children.objects.all().count()
        employee = Account.objects.filter(roles__in=[RoleData.EMPLOYEE.value.get('id')]).count()
        customer = Account.objects.filter(roles__in=[RoleData.CUSTOMER.value.get('id')]).count()
        donor = Donor.objects.all().count()
        res = [{"key": "child",
                "title": "Trẻ em",
                "color": "#ffa39e",
                "value": children,
                "rateString": "hiện tại"},
               {"key": "employee",
                "title": "Nhân viên",
                "color": "#91caff",
                "value": employee,
                "rateString": "hiện tại"},
               {"key": "donor",
                "title": "Tổng số",
                "color": "#ff7a45",
                "value": donor,
                "rateString": "lần ủng hộ"},
               {"key": "customer",
                "title": "Khách",
                "color": "#135200",
                "value": customer,
                "rateString": "hiện tại"}
               ]
        return res

    @classmethod
    def get_total_statistics(cls):
        donates = Donor.objects.all().aggregate(total_donate=Sum("amount"))
        activities = Activity.objects.all().aggregate(total_expense=Sum("expense"))
        donates['total_donate'] = donates['total_donate'] or 0
        activities['total_expense'] = int(activities['total_expense']) if activities['total_expense'] else 0
        date_statistic = {**donates, **activities}
        return date_statistic

    @classmethod
    def get_donate_statistics(cls, start_date, end_date, activity_type):
        donates = Donor.objects.filter(created_at__date__range=[start_date, end_date]).aggregate(
                                        total_donate=Sum("amount"))

        if activity_type != "all" and activity_type:
            activities = Activity.objects.filter(activity_type=activity_type, created_at__date__range=[start_date, end_date]).aggregate(
                                            total_expense=Sum("expense"))
        else:
            activities = Activity.objects.filter(created_at__date__range=[start_date, end_date]).aggregate(
                total_expense=Sum("expense"))
        total_donate = int(donates['total_donate']) if donates['total_donate'] else 0
        total_expense = int(activities['total_expense']) if activities['total_expense'] else 0
        date_statistic = []

        date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        date_end = datetime.strptime(end_date, '%Y-%m-%d').date()
        date = date_start
        while date <= date_end:
            donor = Donor.objects.filter(created_at__date=date).aggregate(
                                        donate=Sum("amount"))
            if activity_type != "all" and activity_type:
                expense = Activity.objects.filter(activity_type=activity_type, created_at__date=date).aggregate(
                    expense=Sum("expense"))
            else:
                expense = Activity.objects.filter(created_at__date=date).aggregate(
                    expense=Sum("expense"))
            date_statistic.append({
                "day": date,
                "donate": donor['donate'] or 0,
                "expense": int(expense['expense']) if expense['expense'] else 0
            })
            date = date + timedelta(days=1)

        response = {
            "total_donate": int(total_donate),
            "total_expense": int(total_expense),
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
