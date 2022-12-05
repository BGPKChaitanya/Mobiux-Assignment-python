from datetime import datetime

# imported data from file sales-data.txt

file = open("sales-data.txt", "r")
read = file.readlines()

data = {}
varieble = read[0].split(",")
length = len(varieble)
# print(varieble)
for i in range(length):
    sales_field = []
    for item in read[1:]:
        field_item = item.split(",")
        sales_field.append(field_item[i])
        key = varieble[i].lower()
        if " " in key:
            key = key.replace(" ", "_")
        if "\n" in key:
            key = key.replace("\n", "")
        data.update({key: sales_field})
# print(data)
    
#1. Total sales of the store.

sales = data.get('total_price')
prices = []
for pr in sales:
    pr.replace("\n", "")
    pr = int(pr)
    prices.append(pr)
sales = prices
print("Total sales of the store: " + str(sum(sales)))


#2. Month wise sales totals

dates = data.get("date")

sales_months_list = []
for date in dates:
    d = datetime.strptime(date, "%Y-%m-%d")
    sales_months_list.append(d.strftime("%B"))
month_set = list(set(sales_months_list))
sales_per_month = {}
monthly_index = {}
for m in month_set:
    index_list = [index for index in range(len(sales_months_list)) if sales_months_list[index]==m]
    monthly_index.update({m: index_list})
    price = 0
    for p in index_list:
        price += sales[p]
    sales_per_month.update({m: price})
print("Month wise sales totals: ", sales_per_month)


# 3. Most popular item (most quantity sold) in each month.
# 4. Items generating most revenue in each month.
# 5. For the most popular item, find the min, max and average number of orders each month.

item_names = data.get("sku")
quantity = data.get("quantity")
unit_price = data.get("unit_price")
total_price = sales

def most_popular_or_revenue_item(products):
    keys = list(products.keys())
    values = list(products.values())
    max_value = max(values)
    index_of_max_value = values.index(max_value)
    return keys[index_of_max_value]

sold_items_index_in_month = {}
# unique_item_per_month = {}
# monthly_each_product_details = {}
most_popular_item = {}
most_popular_item_order_details = {}
most_revenue_generate_item = {}
for mon in month_set:
    items = []
    month_item_index = monthly_index[str(mon)]
    for each in month_item_index:
        items.append(item_names[each])
    unique_items = list(set(items))
    monthly_item_quantity = {}
    each_product_details = {}
    each_product_revenue_details = {}
    for each_item in unique_items:
        each_item_index = [position for position in month_item_index if (each_item == item_names[position])]
        monthly_item_quantity.update({each_item: each_item_index})
        quantity_product = 0
        revenue_product = 0
        for each_position in each_item_index:
            quantity_product += int(quantity[each_position])
            revenue_product += int(sales[each_position])
        each_product_details.update({each_item:quantity_product})
        each_product_revenue_details.update({each_item: revenue_product})
    
    most_popular_item_in_month = most_popular_or_revenue_item(each_product_details)
    most_revenue_item_in_month = most_popular_or_revenue_item(each_product_revenue_details)
    sold_items_index_in_month.update({mon: monthly_item_quantity})
    # unique_item_per_month.update({mon: unique_items})
    # monthly_each_product_details.update({mon: each_product_details})
    most_popular_item.update({mon: most_popular_item_in_month})
    most_revenue_generate_item.update({mon: most_revenue_item_in_month})

    popular_item_index = monthly_item_quantity[most_popular_item_in_month]
    popular_item_quantities = [int(quantity[ind]) for ind in popular_item_index]
    # print(popular_item_quantities)

    min_orders = min(popular_item_quantities)
    max_order = max(popular_item_quantities)
    average_order = int(sum(popular_item_quantities) / len(popular_item_quantities))
    # print(min_orders, max_order, average_order)
    most_popular_item_order_details.update({mon: {"Minimum order": min_orders, "Maximum order": max_order, "Average order": average_order}})

# print(sold_items_index_in_month)
print("Most Popular Item in each month: ", most_popular_item)
print("Items generating most revenue in each month: ", most_revenue_generate_item)
print("Minimum, Maxium and Average number of orders for most popular: ", most_popular_item_order_details)

