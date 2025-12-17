const client = require('./grpc_client');

// Example payload
const newBook = {
  title: "Clean Code",
  author: "Robert C. Martin",
  published_year: 2008
};

// Call AddBook RPC
client.AddBook(newBook, (err, response) => {
  if (err) {
    console.error("AddBook failed:", err.message);
    return;
  }
  console.log("AddBook response:", response);
});