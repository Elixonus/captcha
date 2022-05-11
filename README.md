# captcha :hugs:

To install the required dependencies, run the command ```pip install -r requirements.txt```

To start the captcha generator web server, go to the main directory and run the command
```flask run```
which will run ```wsgi.py``` and start the server

## API

```/api/new``` - create a new captcha and give the code of it in text

```/api/image?code=c``` - view the captcha image with the code matching c

```/api/check?code=c&number=n``` - check if the captcha with the code matching c has the number n as the solution, response is either "Good" or "Bad"
