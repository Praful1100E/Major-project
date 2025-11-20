const express = require('express');
const app = express();

const PORT = parseInt(process.env.PORT, 10) || 3000;

app.get('/', (req, res) => {
  res.json({
    message: 'Major-project API',
    endpoints: ['/', '/status']
  });
});

app.get('/status', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: Date.now()
  });
});

app.listen(PORT, () => {
  console.log(`Major-project running on http://localhost:${PORT}`);
});
