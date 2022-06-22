from django import forms
from django.db import models
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


def users():
    # pretend this is an API endpoint
    print("users API called")
    return [
        {"id": "1", "name": "Tim", "city": "London"},
        {"id": "2", "name": "Bob", "city": "Paris"},
        {"id": "3", "name": "Alice", "city": "Berlin"},
        {"id": "4", "name": "John", "city": "New York"},
    ]


def user_choices():
    print("user_choices called")
    user_choices = []
    for user in users():
        user_choices.append(
            (user["id"], f"{user['name']} - {user['city']}"),
        )
    return [("", "---")] + user_choices


def currencies():
    # pretend this is an API endpoint
    print("currencies API called")
    return [
        {"id": "1", "name": "Euro", "symbol": "€"},
        {"id": "2", "name": "Dollar", "symbol": "$"},
        {"id": "3", "name": "Pound", "symbol": "£"},
        {"id": "4", "name": "Yen", "symbol": "¥"},
    ]


def currency_choices():
    print("currency_choices called")
    currency_choices = []
    for currency in currencies():
        currency_choices.append(
            (currency["id"], f"{currency['name']} - {currency['symbol']}"),
        )
    return [("", "---")] + currency_choices


class HomePageForm(WagtailAdminPageForm):
    def __init__(
        self,
        data=None,
        files=None,
        parent_page=None,
        subscription=None,
        *args,
        **kwargs,
    ):
        print("form init called")
        super().__init__(data, files, parent_page, subscription, *args, **kwargs)

    user_owner = forms.ChoiceField(
        choices=user_choices,  # just a reference to the function is enough
        required=False,
    )

    currency = forms.ChoiceField(
        choices=currency_choices,  # just a reference to the function is enough
        required=False,
    )


class HomePage(Page):
    # simulate the salesforce fields that store an id like this:
    # sf_campaign_record_type = models.CharField(
    #     verbose_name=_("campaign record type"), blank=True, max_length=50
    # )
    # sf_campaign_group = models.CharField(
    #     verbose_name=_("campaign group"), blank=True, max_length=50
    # )
    # The page in gosh is an AbstractEmailForm but that shouldn't make too
    # much of a difference.
    user_owner = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=50, blank=True)

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("user_owner"),
        FieldPanel("currency"),
        FieldPanel("body"),
    ]

    base_form_class = HomePageForm
