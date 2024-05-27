from django import forms
from .models import RoomRate, Discount, DiscountRoomRate, OverriddenRoomRate

class AddRoomRate(forms.ModelForm):
    class Meta:
        model = RoomRate
        fields = ['room_id', 'room_name', 'default_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_id'].required = True 
        self.fields['room_name'].required = True 
        self.fields['default_rate'].required = True 

        # instance = kwargs.get('instance')
        # if instance:
        #     # If instance exists (editing existing instance), disable the field
        #     self.fields['room_id'].disabled = True
        #     self.fields['room_id'].required = False 

class AddOverrideRate(forms.ModelForm):
    class Meta:
        model = OverriddenRoomRate
        fields = ['room_rate', 'overridden_rate', 'stay_date']
        widgets = {
            'stay_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_rate'].required = True 
        self.fields['overridden_rate'].required = True 
        self.fields['stay_date'].required = True 


class AddDiscount(forms.ModelForm):
    # room_specific_discount = forms.ModelMultipleChoiceField(RoomRate.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Discount
        fields = ['discount_id', 'discount_name', 'discount_type', 'discount_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discount_id'].required = True 
        self.fields['discount_name'].required = True 
        self.fields['discount_value'].required = True 
        # self.fields['room_specific_discount'].initial = [room for room in RoomRate.objects.all()] 


class FilterRange(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Start Date',
                'type': 'date'
    }))

    end_date = forms.DateField(widget=forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'End Date',
                'type': 'date'
    }))

    room_name = forms.ModelChoiceField(RoomRate.objects.all(), required=True)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].required = True 
        self.fields['end_date'].required = True 