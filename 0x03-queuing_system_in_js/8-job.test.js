import { createQueue } from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518732',
    message: 'This is the code 1234 to verify your account',
  },
];

describe('unittest for queue system', () => {
  before(() => {
    queue.testMode.enter();
  });
  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(15, queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs', (done) => {
    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);

    done();
  });

  it('should be of the right type', () => {
    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
  });
});
