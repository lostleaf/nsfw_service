# nsfw_service
Web service of Yahoo's open nsfw detector

## Run the service
First, build the docker file:

```
sudo docker build -t nsfw_service .
```

Then, you can run the built docker image:

```
sudo docker run -v FOLDER_TO_STORE_MISTAKE_SAMPLES:/nsfw_service/mistakes -p 5000:5000 --rm nsfw_service
```

You should replace FOLDER_TO_STORE_MISTAKE_SAMPLES to the absolute path of the folder you want to store the wrongly predicted samples

## Interfaces

There are currently two interfaces: predict whether images are NSFW and mistake(wrong prediction) report

### Prediction Interface

You can send a JSON array of image URLs to `/query` to predict the images. If the query is correctly executed, a JSON array of the NSFW probability will be returned. 

Here is an query example using `curl`:

```
curl -H "Content-Type: application/json" -X POST -d '["http://www.cosy.sbg.ac.at/~pmeerw/Watermarking/lena_color.gif", "http://httpbin.org/status/404"]' http://52.76.69.39:5000/query
```

The reture value should be:

```
[ 0.13406969606876373, null]

```

The first image is a human face, so it's not NSFW. The second URL leads to a 404 error, so the return value is NULL.

### Mistake Report Interface

You can send a JSON array of (image URL, class) pairs to `/query` to report mistakes. The `class` value here is the real class of the associated image. If the query is correctly executed, a JSON array of the boolean values, which indicates whether the corresponding image is successfully saved, will be returned. And the images will be stored in "True" and "False" subfolders of FOLDER_TO_STORE_MISTAKE_SAMPLES respectively.

Here is an example using curl:

```
curl -H "Content-Type: application/json" -X POST -d '[["http://www.cosy.sbg.ac.at/~pmeerw/Watermarking/lena_color.gif", false], ["http://httpbin.org/status/404", false]]' http://52.76.69.39:5000/report_mistake
```

The return value should be:

```
[true, false]
```

since the first URL of image could be successfully stored, and the second URL leads to 404 error.