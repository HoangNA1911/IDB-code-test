### Running the application locally 

- Step 1: Clone project
    ```
  git clone git@github.com:HoangNA1911/IDB-code-test.git
  cd <project folder>
    ```
- Step 2: Set Up a Virtual Environment (Optional)
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- Step 3: Install Dependencies
  ```
  pip install -r requirements.txt
  ```
- Step 4: Apply Database Migrations
  ```
  python manage.py migrate
  ```
- Step 5: Run the Development Server
  ```
  python manage.py runserver
  ```
