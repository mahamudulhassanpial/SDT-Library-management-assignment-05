from typing import Any
from django import forms
from .models import Transactions
from accounts.models import UserLibraryAccount
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit = 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit:
            raise forms.ValidationError(
                f"Minimum deposit amount is {min_deposit}"
            )
        return amount

