// tests/integration/books.int.test.js
const request = require("supertest");
const app = require("../../src/index");

// Option A: mock gRPC client for integration at REST layer
jest.mock("../../src/grpc/client", () => ({
  AddBook: (body, cb) => cb(null, { id: 1, ...body, available_copies: 1 }),
  UpdateBook: (body, cb) => cb(null, { ...body })
}));

describe("Books integration", () => {
  it("should add a book successfully", async () => {
    const res = await request(app).post("/books").send({
      title: "Clean Code",
      author: "Robert C. Martin",
      published_year: 2008
    });
    expect(res.status).toBe(200);
    expect(res.body.title).toBe("Clean Code");
  });

  it("should reject invalid book payload", async () => {
    const res = await request(app).post("/books").send({
      title: "",
      author: "X",
      published_year: 1200
    });
    expect(res.status).toBe(400);
    expect(res.body.error).toBe("Invalid input");
  });
});