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
- Heroku

## How to run this code?
### A. Local
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

5. Install requirements
```
pip install -r requirements.txt
```

6. Configure and make your own `.env` file
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

7. Run your app
```
uvicorn main:app --reload
```

### B. Docker

1. Clone this repo
   ```bash
   git clone https://github.com/roniantonius/Warung-Omega-Ecommerce.git
   ```

2. Build the Docker image
   ```bash
   docker build -t warungomega:latest .
   ```

3. Run the Docker container
   ```bash
   docker run -d -p 8000:8000 warungomega:latest
   ```

4. Access the application
   Open a browser and go to `http://localhost:8000` to see the running FastAPI application.

5. (Optional) Push the image to Docker Hub  
   If you want to deploy this on a Kubernetes cluster, you’ll need to push the image to a container registry (e.g., Docker Hub).

   ```bash
   docker tag warungomega:latest roniantonius/warungomega:latest
   docker push roniantonius/warungomega:latest
   ```

### C. Kubernetes Deployment

To deploy the application on a Kubernetes cluster:

1. Apply the deployment configuration:
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. Apply the service configuration:
   ```bash
   kubectl apply -f service.yaml
   ```

3. Get the external IP address:
   ```bash
   kubectl get services
   ```
   Use the external IP listed under your service to access the application.


### List of Website Architecture on `document/` directory or at `SRS Warung Omega.pdf`
1. Use Case Diagram
2. Activity Diagram
3. Sequence Diagram
4. Class Diagram
5. State Chart Diagram
6. BPMN

## Documentation


![1  index](https://github.com/user-attachments/assets/fe1e21ad-02b8-43c5-8675-ad366c331a79)

![2  product-index](https://github.com/user-attachments/assets/42f864d1-8b97-403c-8af5-aed32a1b5318)

![3  product-page](https://github.com/user-attachments/assets/7f7ff4aa-014f-4990-a481-1ef84359964e)

![4  login](https://github.com/user-attachments/assets/e6b44ffc-f6eb-49e7-98cf-8f06367056e5)

![5  cart](https://github.com/user-attachments/assets/5164901f-1f3a-43ea-b151-5869623f1c9b)

![6  transaction 1](https://github.com/user-attachments/assets/b74c9af6-2d78-4bf7-a27e-100307c1061d)

![7  transaction 2](https://github.com/user-attachments/assets/18503262-6b88-4c94-8c44-a47cbbcd7a15)

![8  payment midtrans 1](https://github.com/user-attachments/assets/6b77581f-5203-4659-ae05-2bcf0fee9bd8)

![9  payment midtrans 2](https://github.com/user-attachments/assets/03758362-defc-490c-8238-ec00387f748c)

![10  sandbox test 1](https://github.com/user-attachments/assets/723efbe3-0bc1-429e-b9f1-0c4e2254b3ff)

![11  success payment](https://github.com/user-attachments/assets/cca8a208-4f7e-4e65-a6b9-f0277627d08c)

![12  success transaction](https://github.com/user-attachments/assets/71aa5b9f-f5e0-4c09-a8d8-c26fd6d3ed98)

![13  user transaction history](https://github.com/user-attachments/assets/bef66779-4a5a-42cc-96cf-351b40fcf2e9)

![14  responsive](https://github.com/user-attachments/assets/203b2c14-498a-4e0b-b06c-ab5a782bd971)
