# devConnector

> Social network of developers app built with the Django and Next.js.
> This is a full stack application with authentication, profiles, posts, projects, votes.

## Version 📌

### 2 (current)
- This is the second version of the app using Next.js and Django REST Framework.
- Google OAuth2 authentication is added.
- JWT tokens are used for authentication.
- HttpOnly cookie's based authentication.
- Enhanced UI/UX.
### 1
- This is the first version of the app using Django templates.
- CSRF tokens are used for authentication.
- Session based authentication.
- Basic UI/UX.

## Build with 🛠️

- Django
- Django REST Framework
- Djoser
- PostgreSQL
- Next.js

## Tools 🧰

- AWS S3
- Digital Ocean
- Postman

## Quick Start 🚀

### Clone the repository

```bash
git clone https://github.com/ndayishimiyeeric/dev_connector.git
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Setup .env.local file

```bash
DEVELOPMENT_MODE=
DJANGO_SECRET_KEY=
DEBUG=

AWS_SES_ACCESS_KEY_ID=
AWS_SES_SECRET_ACCESS_KEY=
AWS_SES_REGION_NAME=
AWS_SES_FROM_EMAIL=

DOMAIN=
AUTH_COOKIE_SECURE=False

GOOGLE_AUTH_KEY=
GOOGLE_AUTH_SECRET_KEY=

REDIRECT_URLS=
```

### Run migrations

```bash
python manage.py migrate
```

### Run server

```bash
python manage.py runserver
```

## Author ✒️

👤 **Eric Ndayishimiye**

- **GitHub**: [@ndayishimiyeeric](https://github.com/ndayishimiyeeric)
- **Twitter**: [@odaltongain](https://twitter.com/odaltongain)
- **LinkedIn**: [Ndayishimiye Eric](https://linkedin.com/in/nderic)


## Contributing 🖇️
Contributions, issues, and feature requests are welcome!

## Show your support

Give a ⭐️ if you like this project!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details