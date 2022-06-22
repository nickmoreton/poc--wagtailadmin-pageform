# A Wagtail page with custom form

The problem site is using a custom field that fetches salesforce data:

```python
class SalesforcePicklistFieldPanel(FieldPanel):
    def __init__(self, field_name, sf_entity, sf_field_name, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)
        self.sf_entity = sf_entity
        self.sf_field_name = sf_field_name

        # get_picklist_choices makes a call to salesforce
        self.widget = Select(
            choices=get_picklist_choices(self.sf_entity, self.sf_field_name)
        )

    # def get_form_options(self):
    #     self.widget = Select(
    #         choices=get_picklist_choices(self.sf_entity, self.sf_field_name)
    #     )
    #     return super().get_form_options()

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(sf_entity=self.sf_entity, sf_field_name=self.sf_field_name)
        return kwargs
```

The same happens if the code is on the `__init__` method or the `get_form_options` method.

- When the page is loaded in the admin you expect it to be called and that works OK. Live Salesforce settings are used in the call from `local.py` in development or `production.py` when deployed.
- When tests are run either in development or CI those settings aren't available. When test are been setup those functions get called and the return from salesforce stops the process. I don't think live salesforce data is required in the tests and there seems to be mocks in place but the setup creates pages and thats when the functions get called, I think.

## Things I tried without success.

- Add a setting in `test.py` to prevent the functions running during tests, kind of worked but a hack and the container build process fails then.
- Some variations of the above `SalesforcePicklistFieldPanel` but they all still made calls during setup.

## A test POC that seems to work.

This site repo has a fake setup as best I can do to try and see when the function calls are made.

```python
# imports as usual

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
    )

    currency = forms.ChoiceField(
        choices=currency_choices,  # just a reference to the function is enough
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
    user_owner = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("user_owner"),
        FieldPanel("currency"),
        FieldPanel("body"),
    ]

    base_form_class = HomePageForm

```

