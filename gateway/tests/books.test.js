const request = require("supertest");
jest.mock("../src/grpc/client", () => ({
  AddBook: jest.fn(),
  UpdateBook: jest.fn()
}));

const app = require("../src/index");
const client = require("../src/grpc/client");

describe("Books API", () => {
  test("POST /books validates payload and calls AddBook", async () => {
    client.AddBook.mockImplementation((body, cb) => cb(null, { id: 1, ...body, available_copies: 1 }));

    const res = await request(app).post("/books").send({
      title: "Clean Code",
      author: "Robert C. Martin",
      published_year: 2008
    });

    expect(res.status).toBe(200);
    expect(res.body.title).toBe("Clean Code");
    expect(client.AddBook).toHaveBeenCalledWith(expect.objectContaining({
      title: "Clean Code", author: "Robert C. Martin", published_year: 2008
    }), expect.any(Function));
  });

  test("POST /books rejects invalid payload", async () => {
    const res = await request(app).post("/books").send({
      title: "", author: "A", published_year: 1200
    });
    expect(res.status).toBe(400);
    expect(res.body.error).toBe("Invalid input");
  });

  test("PUT /books/:id updates book and maps response", async () => {
    client.UpdateBook.mockImplementation((body, cb) => cb(null, { ...body }));

    const res = await request(app).put("/books/5").send({
      title: "New Title",
      author: "Author",
      published_year: 2010
    });

    expect(res.status).toBe(200);
    expect(res.body.id).toBe(5);
    expect(client.UpdateBook).toHaveBeenCalled();
  });
});