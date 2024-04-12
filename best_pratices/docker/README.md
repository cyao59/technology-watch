# Useful command

### Run docker image in local
gcloud auth configure-docker
docker buildx build --platform linux/amd64 -t eu.gcr.io/uc-mh-private-pns-stg/uc-mh-private-pns:latest /Users/cyao/mh/uc-mh-private-pns/dbt/
docker push  eu.gcr.io/uc-mh-private-pns-stg/uc-mh-private-pns:lates
 