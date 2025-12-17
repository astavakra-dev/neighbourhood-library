const express = require("express");
const morgan = require("morgan");
const books = require("./routes/books");
const members = require("./routes/members");
const borrow = require("./routes/borrow");
const errorHandler = require("./middleware/errorHandler");

const app = express();
app.use(express.json());
app.use(morgan("dev"));

app.use("/books", books);
app.use("/members", members);
app.use("/borrow", borrow);

// Fallback error handler (after routes)
app.use(errorHandler);

const port = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(port, () => console.log(`Gateway running on http://localhost:${port}`));
}

module.exports = app; // exported for tests