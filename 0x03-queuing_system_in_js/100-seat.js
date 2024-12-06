import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

const app = express();
const queue = createQueue();
const client = createClient();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveSeat(number) {
  if (Number.isInteger(number) && number >= 0) {
    await setAsync('available_seats', number);
  }
}

(async () => {
  await reserveSeat(50);
})();

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');

  return seats !== null ? Number(seats) : 0;
}

let reservationEnabled = true;

queue.process('reserve_seat', async (job, done) => {
  try {
    const seats = await getCurrentAvailableSeats();
    const newSeats = seats - 1;

    if (newSeats < 0) {
      done(new Error('Not enough seats available'));
    }

    await reserveSeat(newSeats);

    console.log(`Reserved 1 seat. Remaining seats: ${newSeats}`);

    if (newSeats === 0) {
      reservationEnabled = false;
    }
    done();
  } catch (err) {
    console.error(`Error processing reservation job: ${err.message}`);
    done(err);
  }
});

app.get('/available_seats', async (req, res) => {
  try {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
  } catch (err) {
    console.error(`Error fetching available seats: ${err.message}`);
    res.status(500).json({ error: 'Could not retrieve available seats' });
  }
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.send({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (!err) {
      res.send({ status: 'Reservation in process' });
    } else {
      res.send({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', (req, res) => {
  res.send({ status: 'Queue processing' });
});

const PORT = 1245;

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
