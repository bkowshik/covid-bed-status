# Infrastructure


Reference: [GCP developer pro-tips: How to schedule a recurring Python script on GCP](https://cloud.google.com/blog/products/application-development/how-to-schedule-a-recurring-python-script-on-gcp)



## Workflow


### Pub/Sub

> PubSub topic exists purely to connect the two ends of our pipeline: It is an intermediary mechanism for connecting the Cloud Scheduler job and the Cloud Function, which holds the actual Python script that we will run. Essentially, the PubSub topic acts like a telephone line, providing the connection that allows the Cloud Scheduler job to talk, and the Cloud Function to listen.

```bash
# Create a new Pub/Sub topic.
gcloud pubsub topics create 'download-covid-bed-status'

# TEST: Publish a message to the topic.
gcloud pubsub topics publish 'download-covid-bed-status' \
    --message 'Hello, world!' \
    --attribute 'action=download'
```


### Cloud Function

> The Cloud Function subscribes to this topic. This means that it is alerted whenever a new message is published. When it is alerted, it then executes the Python script.

```bash
# Connect function with Pub/Sub topic.
gcloud functions deploy 'download-covid-bed-status' \
    --entry-point 'download' \
    --runtime 'python37' \
    --trigger-resource 'download-covid-bed-status' \
    --trigger-event 'google.pubsub.topic.publish'

# TEST: Call function with test data.
gcloud functions call 'download-covid-bed-status' --data='{"message": "Hello, world!"}'
```


### Scheduler

> Cloud Scheduler is a managed Google Cloud Platform (GCP) product that lets you specify a frequency in order to schedule a recurring job. In a nutshell, it is a lightweight managed task scheduler.

```bash
# Schedule message to Pub/Sub.
gcloud scheduler jobs create pubsub 'download-covid-bed-status' \
    --schedule '0 * * * *' \
    --topic 'download-covid-bed-status' \
    --message-body 'This is a job that runs every hour.'

# TEST: Trigger the job.
gcloud scheduler jobs run 'download-covid-bed-status'
```
