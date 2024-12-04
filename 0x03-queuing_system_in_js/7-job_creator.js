import { createQueue } from 'kue';

const queue = createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account',
  },
];

for (const job of jobs) {
  const queueJob = queue.create('push_notification_code_2', job).save((err) => {
    if (!err) {
      console.log(`Notification job created: ${queueJob.id}`);
    }
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
}
