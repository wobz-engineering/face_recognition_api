# face_recognition_api

### Upload to Cloud Build

```bash

# Create a Docker repository in Artifact Registry
gcloud artifacts repositories create wobz-docker-images --repository-format=docker --location=us-west1 --description="Wobz docker images"

# Verify that your repository was created
gcloud artifacts repositories list

# Build an image using gcloud Dockerfile
gcloud builds submit --tag us-west1-docker.pkg.dev/wobz-goberment-cms/wobz-docker-images/face-id-recognition:latest .

```

### Upload to Cloud Build with YAML

```bash

# Build an image using cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml

```

### Endpoints

/generate-encodings

```bash
curl --location --request POST 'https://SERVER_URL/generate-encodings' \
--form 'file=@"face-photo.png"'
```


/generate-encodings

```bash
curl --location --request POST 'https://SERVER_URL/compare-faces' \
--form 'file=@"FaceToCompare.png"' \
--form 'encodings="[-0.15266633033752441,......]"'
```