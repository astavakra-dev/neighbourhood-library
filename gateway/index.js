require('dotenv').config();
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');

const books = require('./routes/books');
const members = require('./routes/members');
const loans = require('./routes/loans');

const app = express();
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.use('/api/books', books);
app.use('/api/members', members);
app.use('/api/loans', loans);

const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`API Gateway listening on ${port}`));