# Image generation with Nanobanana AI
To freely use Nanobanana I do not use official API. It is not available in Belarus, so i've found the project, that use official API. I make requests to this project to get responses.
## How to run
To run the project, run the command in the project folder.
```
docker compose up
```
Now go to http://localhost:8000/docs.

You will see the automatic interactive API documentation
## How to use
In the form of the request body upload your image, then type your propmt in propmt input and execute it.
When status code of response is 200 response is the image. In a case of error response is json of such format:
```javascript
{
"status": "Error",
'result': error message
}
```
