from django import forms
from . import views
CATEGORIES=[("F","Fashion"),("T","Toys"),("E","Electronics"),("H","Home"),("A","Antique")]
class DateInput(forms.DateInput):
    input_type='date'

class New_listing(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Title","label":"Title of the List"}))
    description=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter Description"}))
    bid_price=forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Bid Price"}))
    category=forms.CharField(widget=forms.Select(choices=CATEGORIES))
    end_date=forms.DateField(widget=DateInput)
    image=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Image URL"}))

class Edit_form(forms.Form):
     
    
    title=forms.CharField(widget=forms.TextInput(attrs={"value":"obj.item_name"}))
    



    