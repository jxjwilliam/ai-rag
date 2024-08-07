# RAG Python

## Q/A

- CHANGELOG.md, CONTRIBUTING.md, Dockerfile, .dockerignore, flow.json
  
## WSGI (Web Server Gateway Interface)

In Prod-env, opt for a dedicated production `WSGI server`. Here are some options:

- **Gunicorn*: A high-speed, thread-pooled WSGI server that works well with Python web applications.
- **uWSGI**: A versatile WSGI server that supports various protocols and interfaces.
- **Waitress**: A lightweight WSGI server suitable for small applications.
- **mod_wsgi**: An Apache module for serving WSGI applications.
- **gevent** and **eventlet**: Libraries that provide asynchronous capabilities for WSGI servers.

Remember to put an `HTTP server (reverse proxy)` in front of the `WSGI server` for added security and efficiency. Popular choices include `nginx` and `Apache`. Alternatively, consider using hosting platforms like `PythonAnywhere`, `Google App Engine`, or `AWS Elastic Beanstalk`. These services manage server setup, networking, and domain configuration.

## Activate Virtual Environment

```bash
$ cd __backend-python__
$ source venv/bin/activate
```

## API calls

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"query": "what is collection manager"}' http://localhost:5000/query
```
