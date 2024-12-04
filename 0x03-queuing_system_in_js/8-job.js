export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  for (const job of jobs) {
    const queueJob = queue.create('push_notification_code_3', job);

    queueJob.on('enqueue', () => {
        console.log(`Notification job created: ${queueJob.id}`);
    });
    queueJob.on('complete', () => {
      console.log(`Notification job ${queueJob.id} completed`);
    });
    queueJob.on('failed', (err) => {
      console.error(`Notification job ${queueJob.id} failed: ${err}`);
    });
    queueJob.on('progress', (percent) => {
      console.log(`Notification job ${queueJob.id} ${percent}% complete`);
    });
    queueJob.save()
  }
}
