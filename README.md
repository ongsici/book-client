## Client Service 

FastAPI was used to serve the client service. The homepage will allow users to search for books by Genre or Title. A GET request is then sent to the [backend server](https://github.com/ongsici/book-data).

Backend server is hosted on Azure's Container Instance by deploying the Docker image [here](https://github.com/users/ongsici/packages/container/package/book-data).
Three environment variables were used for this client Docker image - `BOOK_DATA_URL`, `BOOK_DATA_PORT` and `BOOK_DATA_ENDPOINT`.

### Local Installation
Prepare the .env file with the necessary variables.

```
conda create -n book-client python=3.10 -y
conda activate book-client

chmod +x docker_build.sh
./docker_build.sh

docer run -it -p 8080:8080 --env-file .env book-client
```
