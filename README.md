# Warung Omega


## Scope
Warung Omega is an e-commerce website designed to facilitate buying of seafood products by consumers without the involvement of businesses and hidden costs. The functions that a user will be able to perform in this platform are:
- Browse through the database of available product on different category.
- View Product dashboard
- Choose as much seafood product as you can
- Payment using debit/credit card
View receipt details
Wait for the seafood products to get delivered

## Problem
Warung Omega, a local seafood restaurant, seeks to expand its customer base and increase revenue by transitioning to a digital platform. The restaurant currently operates solely as a brick-and-mortar establishment, limiting its reach to local customers. The primary challenge lies in developing an e-commerce website that effectively showcases the restaurant's diverse seafood offerings, facilitates seamless online ordering and payment processes, and ensures timely and reliable delivery. Additionally, the website must be user-friendly and visually appealing to attract a wider customer base.

## Technology Used:
- FastAPI
- Jinja
- Postgre
- Supabase
- RestAPI
- Tortoise, ORM
- Midtrans Payment Gateway
- Oauth

### How to run this code?
1. Clone this repo
```
git clone https://github.com/roniantoniius/Warung-Omega-Ecommerce.git
```

2. Make your virtual environment
```
python -m venv env
```

3. Run your virtual environment and select interpreter
```
.\env\Scripts\activate
```

4. Go to `app` directory
```
cd app
```

5. Install requirements:
```
pip install -r requirements.txt
```

6. Configure and make your own `.env` file:
```
YOUR_OWN_EMAIL
YOUR_OWN_PASS
YOUR_OWN_SECRET
YOUR_OWN_MIDTRANS_SERVER_KEY
YOUR_OWN_MIDTRANS_CLIENT_KEY
YOUR_OWN_DB_USERNAME
YOUR_OWN_DB_PASSWORD
YOUR_OWN_DB_NAME
```