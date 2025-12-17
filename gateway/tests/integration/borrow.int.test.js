// tests/integration/borrow.int.test.js
const request = require("supertest");
const app = require("../../src/index");

jest.mock("../../src/grpc/client", () => ({
  BorrowBook: (body, cb) => cb(null, { record_id: 1, ...body }),
  ReturnBook: (body, cb) => cb(null, { success: true }),
  ListBorrowedBooks: (query, cb) => cb(null, { books: [{ title: "DDD" }] })
}));

describe("Borrow integration", () => {
  it("should borrow a book", async () => {
    const res = await request(app).post("/borrow").send({ book_id: 1, member_id: 2 });
    expect(res.status).toBe(200);
    expect(res.body.record_id).toBe(1);
  });

  it("should return a book", async () => {
    const res = await request(app).post("/borrow/return").send({ book_id: 1, member_id: 2 });
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
  });

  it("should list borrowed books", async () => {
    const res = await request(app).get("/borrow/2");
    expect(res.status).toBe(200);
    expect(res.body.books[0].title).toBe("DDD");
  });
});