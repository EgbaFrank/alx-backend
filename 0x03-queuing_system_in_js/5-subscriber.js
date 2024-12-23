import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

client.subscribe('holberton school channel');

client.on('message', (channel, message) => {
	console.log(message);
	if (message === 'KILL_SERVER') {
		client.unsubscribe('holberton school channel', (err) => { if (err) console.error(err); });
		client.quit((err) => { if (err) console.error(err) });
	}
});
