The website is for a pizza take-out restaurant.
Customers can browse menu items, customize pizzas, add items to cart, place orders, and view previous orders.
Administrators can manage pizzas, toppings, drinks, and orders.
The project will use Django authentication, forms, templates, static files, and admin.

**Database models:**
* Pizza
* Topping
* Drink
* Order
* OrderItem
* PizzaSize

**Views:**
* Home page
* Menu page 
* Pizza detail/customization page 
* Cart page 
* Checkout page 
* Order history page 
* Login page 
* Register page

# Database Design:
The pizza app database has following six main models:
* Pizza stores pizza types such as Margherita or Pepperoni 
* Topping stores extra toppings that can be added 
* Drink stores drink products 
* Order stores one customer order 
* OrderItem stores each item inside an order
* PizzaSize stores size like Small, Medium and Large

The model relationships are as follows:
* One Order belongs to one user 
* One Order has many OrderItems 
* One OrderItem belongs to one Order 
* One OrderItem can represent either a pizza or a drink 
* One Pizza can allow many toppings 
* One Topping can belong to many pizzas 
* One pizza order item can include many selected toppings 
* One pizza size can belong to many pizzas
* One pizza can allow many sizes

Table attributes:
**For Pizza:**
* name 
* description 
* base price or relation to size pricing 
* image 
* available

**For PizzaSize:**
* name 
* price 
* topping_extra_price

**For Topping:**
* name 
* available

**For Drink:**
* name 
* size 
* price 
* available

**For Order:**
* user 
* created_at 
* total_price 
* status

**For OrderItem:**
* order 
* pizza or drink 
* pizza_size 
* quantity 
* item_price

**Personal touch:** Customers can see whether an order is pending, preparing or completed.

## Preliminary Relational Model

Pizza(id, name, description, image, available)

PizzaSize(id, name, price, topping_extra_price)

Topping(id, name, available)

Drink(id, name, size, price, available)

Order(id, user_id, created_at, total_price, status)

OrderItem(id, order_id, pizza_id, drink_id, pizza_size_id, quantity, item_name_snapshot, item_price_snapshot)

* A Pizza can have many allowed Toppings 
* A Topping can belong to many Pizzas 
* An OrderItem for a pizza can include many selected toppings 
* One Order contains many OrderItems 
* One Order belongs to one user

* Order.user_id → Django user 
* OrderItem.order_id → Order 
* OrderItem.pizza_id → Pizza 
* OrderItem.drink_id → Drink 
* OrderItem.pizza_size_id → PizzaSize

Why this database design have been made:
* pizzas need variable sizes 
* toppings must be customizable 
* drinks are simpler products 
* orders must preserve historical data 
* order status supports your personal-touch feature