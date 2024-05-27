from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import RoomRate, Discount, OverriddenRoomRate, DiscountRoomRate
from .forms import AddRoomRate, AddOverrideRate, AddDiscount, FilterRange
from django.contrib import messages
from datetime import date, timedelta
import copy

# def room_rates(request):
#     rooms = RoomRate.objects.all()


#     price_grouping = {}

#     for room in rooms:
#         if float(room.default_rate) in price_grouping.keys():
#             price_grouping[float(room.default_rate)].append(room)
#         else:

#             price_grouping[float(room.default_rate)] = [room]

#     return render(request, 'home.html', {'rooms_grouped': price_grouping})


def add_rate(request):

    if request.method == 'POST':
        form = AddRoomRate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.warning(request, "Issue")
            return redirect('home')

    else:
        form = AddRoomRate()
        return render(request, 'add_rate.html', {'form': form})

    
def edit_rate(request, pk):
    if request.method == 'POST':
        current_room = RoomRate.objects.get(id=pk)
        form = AddRoomRate(request.POST, instance=current_room)

        if form.is_valid():
            form.save()
            messages.success(request, "Room Data Updated Successfully")
            return redirect('home')

        else:

            messages.error(request, "There Is An Issue Updating The Data")
            return redirect('home')


    else:
        current_room = RoomRate.objects.get(id=pk)
        form = AddRoomRate(instance=current_room)
        return render(request, 'update_rate.html', {'form': form})
    

def delete_rate(request, pk):
        
    current_room = RoomRate.objects.get(id=pk)
    current_room.delete()
    messages.warning(request, "Data Deleted Successfully...")
    return redirect('home')

def rate_details(request, pk):
#     print(request)
    room_rate = RoomRate.objects.get(id=pk)
    overridden_rates = room_rate.overrided_rate.all()

    print(overridden_rates)
    # for room_rate in room_rates:
    #     print(room_rate.overriden_rate.all())

    return render(request, 'overridden_rate.html', {'overridden_rates': overridden_rates, 'room_rate': room_rate})
 
def add_overriden_rate(request):


    if request.method == 'POST':
        form = AddOverrideRate(request.POST)

        print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.warning(request, "Issue")
            return redirect('home')

    form = AddOverrideRate()
    return render(request, 'add_override.html', {'form': form})

def edit_overriden_rate(request, pk):
    if request.method == 'POST':
        current_override = OverriddenRoomRate.objects.get(id=pk)
        form = AddOverrideRate(request.POST, instance=current_override)

        if form.is_valid():
            form.save()
            messages.success(request, "Room Data Updated Successfully")
            return redirect('home')

        else:

            messages.error(request, "There Is An Issue Updating The Data")
            return redirect('home')


    else:
        current_override = OverriddenRoomRate.objects.get(id=pk)
        form = AddOverrideRate(instance=current_override)
        return render(request, 'update_rate.html', {'form': form})
    

def delete_overriden_rate(request, pk):
        
    current_override = OverriddenRoomRate.objects.get(id=pk)
    current_override.delete()
    messages.warning(request, "Data Deleted Successfully...")
    return redirect('home')

def add_discount(request):
    if request.method == 'POST':
        form = AddDiscount(request.POST)

        print(form)
        if form.is_valid():
            discount = form.save()
            # if len(form.cleaned_data['room_specific_discount']) != len(RoomRate.objects.all()):
            #     for room in form.cleaned_data['room_specific_discount']:
            #         special_discount = DiscountRoomRate(
            #             room_rate = room,
            #             discount = discount
            #         )

            return redirect('discounts')
        else:
            messages.warning(request, "There Is An Issue Adding The Data")
            return redirect('discounts')

    form = AddDiscount()
    return render(request, 'add_discount.html', {'form': form})

def discounts(request):

    discounts = Discount.objects.all()

    return render(request, 'discount.html', {'discounts': discounts})


def edit_discount(request, pk):
    if request.method == 'POST':
        current_discount = Discount.objects.get(id=pk)
        form = AddDiscount(request.POST, instance=current_discount)

        if form.is_valid():
            form.save()
            messages.success(request, "Discount Data Updated Successfully")
            return redirect('discounts')

        else:
            messages.error(request, "There Is An Issue Updating The Data")
            return redirect('discounts')


    else:
        current_discount = Discount.objects.get(id=pk)
        form = AddDiscount(instance=current_discount)
        return render(request, 'update_discount.html', {'form': form})
    

def delete_discount(request, pk):
        
    current_discount = Discount.objects.get(id=pk)
    current_discount.delete()
    messages.warning(request, "Data Deleted Successfully...")
    return redirect('discounts')


def lowest_rate_calculator(discount_type, discount_value, default_rate):

    lowest_type = discount_type
    lowest_value = discount_value

    lowest_rate = lowest_value if lowest_type == 'Fixed' else \
                    (default_rate * lowest_value/100)
    
    return lowest_rate

def final_price(discounts, room):
    highest_discount = lowest_rate_calculator(discounts[0].discount_type, discounts[0].discount_value, room.updated_rate)

    for discount in discounts[1:]:
        if discount.discount_type == 'Fixed':
            if discount.discount_value > highest_discount: 
                highest_discount = discount.discount_value
        else:
            calculated_discount = lowest_rate_calculator(discount.discount_type, discount.discount_value, room.updated_rate)
            if calculated_discount > highest_discount: 
                highest_discount = calculated_discount
    
    lowest_price = room.updated_rate - highest_discount 
    if lowest_price < 0:
        room.lowest_price = 0
    else:
        room.lowest_price = round(lowest_price, 2)


def room_rates(request):
    rooms = RoomRate.objects.all()
    price_grouping = {}

    if rooms:
        discounts = Discount.objects.all()


        print(date.today())
        for room in rooms:
            room.updated_rate = room.default_rate

            room.discount_applied = False
            if room.overrided_rate.all():
                for override in room.overrided_rate.all():
                    if override.stay_date == date.today():
                        room.updated_rate = override.overridden_rate
            

            # highest_discount = discount[0].discount_value if highest_discount_type == 'Fixed' else \
            #         (room.default_rate * highest_value/100)
            if discounts:
                final_price(discounts, room)


        for room in rooms:
            print(room)
            if float(room.default_rate) in price_grouping.keys():
                price_grouping[float(room.default_rate)].append(room)
            else:

                price_grouping[float(room.default_rate)] = [room]

    return render(request, 'home.html', {'rooms_grouped': price_grouping})


def rate_offers(request):
    rooms = RoomRate.objects.all()

    if request.method == 'POST':
        form = FilterRange(request.POST)
        if form.is_valid():
            requested_data = {}

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            requested_data['duration'] = str(end_date - start_date).split(" ")[0]
            requested_data['room_name'] = form.cleaned_data['room_name']
            room_name = form.cleaned_data['room_name']

            requested_data['required_room'] = RoomRate.objects.get(id=requested_data['room_name'].id)

            discounts = Discount.objects.all()
            overriddes_in_range = room_name.overrided_rate.filter(stay_date__range= (start_date,  end_date))

            rates_in_range = [room_name]
            if overriddes_in_range:
                rates_list = []
                while start_date <= end_date:
                    room_rate = copy.deepcopy(room_name)
                    # current_date = start_date.strftime('%Y-%m-%d')
                    current_date = start_date
                    room_rate.updated_rate = room_rate.default_rate



                    for override in overriddes_in_range:
                        # print("check", type(override.stay_date), type(current_date))
                        if override.stay_date == current_date:
                            print("INNNNN")
                            room_rate.default_rate = override.overridden_rate
                            room_rate.updated_rate = override.overridden_rate

                            break
                    room_rate.lowest_price = room_rate.default_rate
                    
                    if discounts:
                        final_price(discounts, room_rate)
                    
                    rates_list.append(room_rate)

                    rates_list[-1].date = current_date
                    print("Check data", rates_list[-1])
                    # rates_list.append(current_date)
                    start_date += timedelta(days=1)

                
                print(rates_list, "dates_list")
            else:
                rates_list = []
                 
                while start_date <= end_date:
                    room_rate = copy.deepcopy(room_name)
                    # current_date = start_date.strftime('%Y-%m-%d')
                    current_date = start_date
                    room_rate.updated_rate = room_rate.default_rate
                    room_rate.lowest_price = room_rate.default_rate
                    
                    if discounts:
                        final_price(discounts, room_rate)

                    rates_list.append(room_rate)
                    rates_list[-1].date = current_date
                    
                    start_date += timedelta(days=1)

                print(rates_list)


            return render(request, 'rate_offers.html', {'form': form, 'rates_list': rates_list })
            


    form = FilterRange()

    return render(request, 'rate_offers.html', {'form': form, 'rooms': []})