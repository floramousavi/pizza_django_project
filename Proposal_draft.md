# Pizza Take-Out Website Proposal

## Project Purpose
This project is a Django based web application for a pizza take-out restaurant. Customers can browse menu items, customize pizzas, add items to cart, place orders, and view previous orders. Administrators can manage pizzas, toppings, drinks, and orders. The project will use Django authentication, forms, templates, static files, and admin.
## Target Audience
Any customer should be able to register, login, order and customize a pizza, and see the order history. The pizza store employees should be able to view the orders and manage menu items.
## Main Features
The app cntains following features:
* Home page 
* Menu page 
* Pizza detail/customization page 
* Cart page 
* Checkout page 
* Order history page 
* Login page 
* Register page
## Preliminary Relational Model
The pizza App database has following six core models:

* Pizza(id, name, description, image, available)
* PizzaSize(id, name, price, topping_extra_price)
* Topping(id, name, available)
* Drink(id, name, size, price, available)
* Order(id, user_id, created_at, total_price, status)
* OrderItem(id, order_id, pizza_id, drink_id, pizza_size_id, quantity, item_name_snapshot, item_price_snapshot)

The model relationships are as follows:

* A Pizza can have many allowed Toppings 
* A Topping can belong to many Pizzas 
* An OrderItem for a pizza can include many selected toppings 
* One Order contains many OrderItems 
* One Order belongs to one user

Foreign keys are as follows:
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