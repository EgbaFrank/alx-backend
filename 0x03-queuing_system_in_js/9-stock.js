import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const server = express();

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
];

function getItemById(id) {
  for (const product of listProducts) {
    if (product.id === id) {
      return product;
    }
  }
  return null;
}

async function reserveStockById(itemId, stock) {
  try {
    await setAsync(`item.${itemId}`, stock);
    console.log(`Stock reserved for item.${itemId}: ${stock}`);
  } catch (err) {
    console.error(`Error setting stock for item.${itemId}: ${err}`);
    throw err;
  }
  return null;
}

async function getCurrentReservedStockById(itemId) {
  try {
    const stock = await getAsync(`item.${itemId}`);
    if (stock === null) {
      console.warn(`No stock found for item.${itemId}`);
      return 0;
    }
    return parseInt(stock, 10);
  } catch (err) {
    console.error(`Error retrieving stock for item.${itemId}: ${err}`);
    throw err;
  }
}

const getAllItems = () => listProducts.map((product) => ({
  itemId: product.id,
  itemName: product.name,
  price: product.price,
  initialAvailableQuantity: product.stock,
}));

server.get('/list_products', (req, res) => {
  res.json(getAllItems());
});

server.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;

  try {
    if (!itemId || Number.isNaN(itemId)) {
      return res.status(400).json({ error: 'Invalid itemId' });
    }

    const product = getItemById(parseInt(itemId, 10));

    if (!product) {
      return res.status(404).json({ status: 'Product not found' });
    }

    const quantity = await getCurrentReservedStockById(itemId);

    product.currentQuantity = product.stock - (quantity !== null ? quantity : 0);

    res.status(200).json(product);
  } catch (err) {
    console.error(`Error fetching product ${itemId}:`, err);
    return res.status(500).json({ error: 'Internal server error' });
  }
  return null;
});

server.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;

  const parsedItemId = parseInt(itemId, 10);

  try {
    if (!itemId || Number.isNaN(parsedItemId)) {
      return res.status(400).json({ error: 'Invalid itemId' });
    }

    const product = getItemById(parsedItemId);

    if (!product) {
      return res.status(404).json({ status: 'Product not found' });
    }
    const quantity = await getCurrentReservedStockById(parsedItemId);

    if (quantity >= product.stock) {
      return res.status(409).json({ status: 'Not enough stock available', itemId: parsedItemId });
    }

    await reserveStockById(parsedItemId, 1);

    res.json({ status: 'Reservation confirmed', itemId: parsedItemId });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
  return null;
});

const PORT = 1245;

server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
