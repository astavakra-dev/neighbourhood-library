const request = require("supertest");
jest.mock("../src/grpc/client", () => ({
  BorrowBook: jest.fn(),
  ReturnBook: jest.fn(),
  ListBorrowedBooks: jest.fn()
}));

const app = require("../src/index");
const client = require("../src/grpc/client");

describe("Borrow API", () => {
  test("POST /borrow borrows with valid payload", async () => {
    client.BorrowBook.mockImplementation((body, cb) => cb(null, { record_id: 1, ...body }));
    const res = await request(app).post("/borrow").send({ book_id: 1, member_id: 2 });
    expect(res.status).toBe(200);
    expect(res.body.record_id).toBe(1);
  });

  test("POST /borrow returns 400 on invalid payload", async () => {
    const res = await request(app).post("/borrow").send({ book_id: -1, member_id: "x" });
    expect(res.status).toBe(400);
  });

  test("POST /borrow/return returns book", async () => {
    client.ReturnBook.mockImplementation((body, cb) => cb(null, { success: true }));
    const res = await request(app).post("/borrow/return").send({ book_id: 1, member_id: 2 });
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
  });

  test("GET /borrow/:memberId lists borrowed books", async () => {
    client.ListBorrowedBooks.mockImplementation((query, cb) => cb(null, { books: [{ title: "DDD" }] }));
    const res = await request(app).get("/borrow/2");
    expect(res.status).toBe(200);
    expect(res.body.books[0].title).toBe("DDD");
  });

  test("Maps gRPC NOT_FOUND to 404", async () => {
    client.ListBorrowedBooks.mockImplementation((query, cb) =>
      cb({ code: 5, details: "Member not found" }, null)
    );
    const res = await request(app).get("/borrow/999");
    expect(res.status).toBe(404);
    expect(res.body.error).toBe("Not found");
  });
});